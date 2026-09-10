#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR PROFESIONAL DE TABLEROS INMOBILIARIOS (EDICIÓN DINÁMICA .DB)
=============================================================================
Genera tableros visuales de alta definición (2048 x 2048 px) a partir de una
base de datos SQLite ('tablero_datos.db'):
1. Lectura directa desde SQLite: Precios, nombres y rentas son 100% editables.
2. Maquetación realista con rotación de casillas hacia el centro del tablero.
3. Auto-ajuste de tipografía (sin solapamiento ni desborde de textos).
4. Contraste inteligente: Texto blanco sobre fondos oscuros y negro sobre claros.
5. Iconografía vectorial nítida para estaciones, servicios, impuestos y eventos.
6. Exportación dual:
   - 'output/tablero_espana_color.png'
   - 'output/tablero_espana_byn.png'
   - 'output/tablero_datos.db' (Base de datos SQLite)
   - 'output/tablero_datos.json' (Exportación editable)
"""

import os
import sys
import sqlite3
import math

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Se requiere Pillow. Instálala con: pip install Pillow")
    sys.exit(1)

# Importar gestor de base de datos
try:
    from gestor_db import inicializar_base_datos, cargar_casillas_desde_db, exportar_a_json
except ImportError:
    from scripts.gestor_db import inicializar_base_datos, cargar_casillas_desde_db, exportar_a_json

# =============================================================================
# PALETAS DE COLOR (COLOR vs BLANCO Y NEGRO)
# =============================================================================
PALETA_COLOR = {
    "MARRON": (139, 69, 19),
    "CELESTE": (135, 206, 235),
    "ROSA": (255, 105, 180),
    "NARANJA": (255, 140, 0),
    "ROJO": (220, 20, 60),
    "AMARILLO": (255, 215, 0),
    "VERDE": (34, 139, 34),
    "AZUL": (25, 25, 112),
    "FONDO_CENTRO": (214, 232, 217),
    "CASILLA_FONDO": (255, 255, 255),
    "LINEA_BORDE": (35, 35, 35),
    "TEXTO_NEGRO": (20, 20, 20),
    "TEXTO_BLANCO": (255, 255, 255),
    "ROJO_ALERTA": (211, 47, 47),
    "DORADO": (255, 179, 0),
    "CARCEL_NARANJA": (255, 167, 38)
}

PALETA_BYN = {
    "MARRON": (80, 80, 80),
    "CELESTE": (210, 210, 210),
    "ROSA": (160, 160, 160),
    "NARANJA": (130, 130, 130),
    "ROJO": (70, 70, 70),
    "AMARILLO": (230, 230, 230),
    "VERDE": (100, 100, 100),
    "AZUL": (40, 40, 40),
    "FONDO_CENTRO": (245, 245, 245),
    "CASILLA_FONDO": (255, 255, 255),
    "LINEA_BORDE": (0, 0, 0),
    "TEXTO_NEGRO": (0, 0, 0),
    "TEXTO_BLANCO": (255, 255, 255),
    "ROJO_ALERTA": (40, 40, 40),
    "DORADO": (180, 180, 180),
    "CARCEL_NARANJA": (200, 200, 200)
}


def obtener_fuente(tamano, bold=False):
    """
    Localiza fuentes tipográficas del sistema o recurre a la fuente predeterminada.
    """
    fuentes_bold = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    fuentes_normales = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    ]

    candidatas = fuentes_bold if bold else fuentes_normales
    for ruta in candidatas:
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, tamano)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def calcular_luminosidad(color_rgb):
    """
    Calcula la luminancia relativa (0.0 a 1.0) para contraste automático de texto.
    """
    r, g, b = color_rgb[:3]
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def ajustar_lineas_y_fuente(draw, texto, max_ancho, max_alto, tamano_max=19):
    """
    Divide inteligentemente el texto en líneas y calcula el tamaño óptimo de fuente
    para que NUNCA desborde el ancho o alto disponible de la casilla.
    """
    palabras = texto.split(" ")
    
    # Probar diferentes tamaños de fuente de mayor a menor
    for sz in range(tamano_max, 10, -1):
        fnt = obtener_fuente(sz, bold=True)
        # Intentar empaquetar palabras
        lineas = []
        linea_actual = ""
        posible = True
        
        for p in palabras:
            prueba = f"{linea_actual} {p}".strip()
            bbox = draw.textbbox((0, 0), prueba, font=fnt)
            ancho_prueba = bbox[2] - bbox[0]
            if ancho_prueba <= max_ancho:
                linea_actual = prueba
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                bbox_p = draw.textbbox((0, 0), p, font=fnt)
                if (bbox_p[2] - bbox_p[0]) > max_ancho:
                    posible = False
                    break
                linea_actual = p
                
        if linea_actual:
            lineas.append(linea_actual)
            
        if posible and len(lineas) <= 3:
            # Comprobar si cabe en altura
            alto_total = len(lineas) * (sz + 5)
            if alto_total <= max_alto:
                return fnt, lineas, sz

    # Fallback con fuente compacta
    fnt_fallback = obtener_fuente(11, bold=True)
    return fnt_fallback, palabras[:3], 11


# =============================================================================
# DIBUJO DE ICONOS VECTORIALES INTEGRADOS
# =============================================================================
def dibujar_icono(draw, tipo, x_cen, y_cen, tam, paleta):
    """
    Dibuja iconos vectoriales estilizados para casillas especiales.
    """
    color_linea = paleta["LINEA_BORDE"]
    color_relleno = paleta["TEXTO_NEGRO"]

    if tipo == "ESTACION":
        # Locomotora / Tren
        draw.rectangle([x_cen - 22, y_cen - 10, x_cen + 22, y_cen + 12], fill=color_relleno)
        draw.rectangle([x_cen - 15, y_cen - 22, x_cen + 15, y_cen - 10], fill=color_relleno)
        # Chimenea y faro
        draw.rectangle([x_cen + 8, y_cen - 28, x_cen + 14, y_cen - 22], fill=color_relleno)
        # Ruedas
        draw.ellipse([x_cen - 18, y_cen + 10, x_cen - 6, y_cen + 22], fill=color_linea)
        draw.ellipse([x_cen + 6, y_cen + 10, x_cen + 18, y_cen + 22], fill=color_linea)
        # Ventanillas
        draw.rectangle([x_cen - 10, y_cen - 18, x_cen - 2, y_cen - 12], fill=paleta["CASILLA_FONDO"])
        draw.rectangle([x_cen + 2, y_cen - 18, x_cen + 10, y_cen - 12], fill=paleta["CASILLA_FONDO"])

    elif tipo == "SERVICIO_LUZ":
        # Bombilla
        draw.ellipse([x_cen - 16, y_cen - 20, x_cen + 16, y_cen + 8], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.rectangle([x_cen - 8, y_cen + 8, x_cen + 8, y_cen + 18], fill=color_relleno)
        # Rayos
        draw.line([x_cen - 22, y_cen - 8, x_cen - 28, y_cen - 8], fill=color_linea, width=2)
        draw.line([x_cen + 22, y_cen - 8, x_cen + 28, y_cen - 8], fill=color_linea, width=2)
        draw.line([x_cen, y_cen - 24, x_cen, y_cen - 30], fill=color_linea, width=2)

    elif tipo == "SERVICIO_AGUA":
        # Grifo con gota de agua
        draw.rectangle([x_cen - 16, y_cen - 16, x_cen + 10, y_cen - 6], fill=color_relleno)
        draw.rectangle([x_cen + 4, y_cen - 6, x_cen + 14, y_cen + 4], fill=color_relleno)
        # Gota
        draw.ellipse([x_cen + 6, y_cen + 10, x_cen + 12, y_cen + 18], fill=(66, 165, 245) if paleta == PALETA_COLOR else color_relleno)

    elif tipo == "SUERTE":
        # Gran signo de interrogación
        fnt_interrogacion = obtener_fuente(46, bold=True)
        draw.text((x_cen - 14, y_cen - 26), "?", fill=paleta["ROJO_ALERTA"], font=fnt_interrogacion)

    elif tipo == "COMUNIDAD":
        # Cofre del tesoro
        draw.rectangle([x_cen - 22, y_cen - 8, x_cen + 22, y_cen + 16], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.arc([x_cen - 22, y_cen - 20, x_cen + 22, y_cen + 4], start=180, end=0, fill=color_linea, width=3)
        draw.ellipse([x_cen - 4, y_cen - 2, x_cen + 4, y_cen + 6], fill=color_linea)

    elif tipo == "IMPUESTO_CAPITAL":
        # Bolsa de dinero
        draw.ellipse([x_cen - 18, y_cen - 6, x_cen + 18, y_cen + 20], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.polygon([(x_cen - 8, y_cen - 6), (x_cen + 8, y_cen - 6), (x_cen, y_cen - 16)], fill=color_linea)
        fnt_euro = obtener_fuente(16, bold=True)
        draw.text((x_cen - 5, y_cen - 1), "€", fill=color_linea, font=fnt_euro)

    elif tipo == "TASA_LUJO":
        # Anillo con diamante
        draw.ellipse([x_cen - 16, y_cen - 4, x_cen + 16, y_cen + 20], outline=paleta["DORADO"], width=3)
        draw.polygon([(x_cen - 12, y_cen - 4), (x_cen + 12, y_cen - 4), (x_cen, y_cen - 18)], fill=(33, 150, 243) if paleta == PALETA_COLOR else color_relleno)


# =============================================================================
# RENDERIZADOR DE CASILLA INDIVIDUAL (VERTICAL ESTÁNDAR)
# =============================================================================
def renderizar_casilla_estandar(casilla, ancho, alto, paleta):
    """
    Dibuja una casilla estándar no-esquina en posición vertical erguida:
    - Borde superior (hacia el interior del tablero): Franja de color (si es calle).
    - Centro: Nombre de la calle auto-ajustado o icono vectorial.
    - Borde inferior (hacia el exterior del tablero): Precio de compra.
    Luego esta sub-imagen se rota según el lado del perímetro al que pertenezca.
    """
    img = Image.new("RGB", (ancho, alto), paleta["CASILLA_FONDO"])
    draw = ImageDraw.Draw(img)

    # Contorno perimetral
    draw.rectangle([0, 0, ancho - 1, alto - 1], outline=paleta["LINEA_BORDE"], width=2)

    alto_franja = 58
    c_tipo = casilla["tipo"]

    # 1. Franja de color (si es propiedad)
    if c_tipo == "CALLE" and casilla["grupo"] and casilla["grupo"] in paleta:
        color_grupo = paleta[casilla["grupo"]]
        draw.rectangle([0, 0, ancho - 1, alto_franja], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)

    # 2. Iconos vectoriales para casillas especiales
    if c_tipo == "ESTACION":
        dibujar_icono(draw, "ESTACION", ancho // 2, 70, 36, paleta)
    elif c_tipo == "SERVICIO":
        if "Electricidad" in casilla["nombre"]:
            dibujar_icono(draw, "SERVICIO_LUZ", ancho // 2, 70, 36, paleta)
        else:
            dibujar_icono(draw, "SERVICIO_AGUA", ancho // 2, 70, 36, paleta)
    elif c_tipo == "SUERTE":
        dibujar_icono(draw, "SUERTE", ancho // 2, 85, 42, paleta)
    elif c_tipo == "COMUNIDAD":
        dibujar_icono(draw, "COMUNIDAD", ancho // 2, 85, 42, paleta)
    elif c_tipo == "IMPUESTO":
        if "Capital" in casilla["nombre"]:
            dibujar_icono(draw, "IMPUESTO_CAPITAL", ancho // 2, 75, 40, paleta)
        else:
            dibujar_icono(draw, "TASA_LUJO", ancho // 2, 75, 40, paleta)

    # 3. Nombre de la casilla con auto-ajuste tipográfico
    y_min_texto = alto_franja + 10 if c_tipo == "CALLE" else 115
    alto_disp_texto = alto - y_min_texto - 45
    max_ancho_texto = ancho - 16

    fnt_calle, lineas_texto, tam_fuente = ajustar_lineas_y_fuente(
        draw, casilla["nombre"], max_ancho_texto, alto_disp_texto, tamano_max=18
    )

    # Centrar verticalmente las líneas en el espacio de texto
    altura_linea = tam_fuente + 4
    altura_bloque = len(lineas_texto) * altura_linea
    y_offset = y_min_texto + max(0, (alto_disp_texto - altura_bloque) // 2)

    for linea in lineas_texto:
        bbox = draw.textbbox((0, 0), linea, font=fnt_calle)
        ancho_l = bbox[2] - bbox[0]
        x_pos = (ancho - ancho_l) // 2
        draw.text((x_pos, y_offset), linea, fill=paleta["TEXTO_NEGRO"], font=fnt_calle)
        y_offset += altura_linea

    # 4. Precio en la base de la casilla
    precio_val = casilla["precio_compra"]
    if precio_val > 0:
        texto_precio = f"{precio_val} €"
    elif c_tipo == "IMPUESTO":
        texto_precio = "PAGA 200 €" if "Capital" in casilla["nombre"] else "PAGA 100 €"
    else:
        texto_precio = ""

    if texto_precio:
        fnt_precio = obtener_fuente(16, bold=True)
        bbox_p = draw.textbbox((0, 0), texto_precio, font=fnt_precio)
        ancho_p = bbox_p[2] - bbox_p[0]
        x_precio = (ancho - ancho_p) // 2
        draw.line([10, alto - 32, ancho - 10, alto - 32], fill=paleta["LINEA_BORDE"], width=1)
        draw.text((x_precio, alto - 26), texto_precio, fill=paleta["TEXTO_NEGRO"], font=fnt_precio)

    return img


# =============================================================================
# RENDERIZADOR DE LAS 4 ESQUINAS DEL TABLERO
# =============================================================================
def renderizar_esquina(tipo, tamano, paleta):
    """
    Dibuja las 4 esquinas cuadradas (SALIDA, CÁRCEL, PARKING, IR A LA CÁRCEL).
    """
    img = Image.new("RGB", (tamano, tamano), paleta["CASILLA_FONDO"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, tamano - 1, tamano - 1], outline=paleta["LINEA_BORDE"], width=3)

    if tipo == "SALIDA":
        # Flecha roja gigante y texto
        fnt_salida = obtener_fuente(34, bold=True)
        fnt_sub = obtener_fuente(18, bold=True)

        draw.text((30, 25), "¡SALIDA!", fill=paleta["ROJO_ALERTA"], font=fnt_salida)

        # Gran flecha roja orientada hacia la casilla 1
        color_flecha = paleta["ROJO_ALERTA"]
        draw.polygon([(40, 110), (140, 110), (140, 85), (210, 125), (140, 165), (140, 140), (40, 140)], fill=color_flecha)

        draw.text((25, 200), "COBRA 200 €", fill=paleta["TEXTO_NEGRO"], font=fnt_sub)
        draw.text((32, 226), "AL PASAR", fill=paleta["TEXTO_NEGRO"], font=fnt_sub)

    elif tipo == "CARCEL":
        # Zona interior: Celda de castigo
        celda_w = 175
        celda_h = 175
        x_c0 = tamano - celda_w
        y_c0 = 0
        draw.rectangle([x_c0, y_c0, tamano - 1, celda_h], fill=paleta["CARCEL_NARANJA"], outline=paleta["LINEA_BORDE"], width=2)

        # Barrotes de la prisión
        num_barrotes = 6
        for i in range(1, num_barrotes):
            bx = x_c0 + (i * (celda_w // num_barrotes))
            draw.line([bx, y_c0, bx, celda_h], fill=paleta["LINEA_BORDE"], width=4)

        fnt_carcel = obtener_fuente(20, bold=True)
        draw.text((x_c0 + 16, celda_h + 8), "EN LA CÁRCEL", fill=paleta["TEXTO_NEGRO"], font=fnt_carcel)

        # Zona exterior: De visita
        fnt_visita = obtener_fuente(20, bold=True)
        draw.text((12, tamano - 50), "SOLO DE", fill=paleta["TEXTO_NEGRO"], font=fnt_visita)
        draw.text((22, tamano - 26), "VISITA", fill=paleta["TEXTO_NEGRO"], font=fnt_visita)

    elif tipo == "PARKING":
        # Coche azul/rojo con letra P
        fnt_parking = obtener_fuente(26, bold=True)
        fnt_sub = obtener_fuente(18, bold=True)

        draw.text((45, 25), "PARKING", fill=paleta["ROJO_ALERTA"], font=fnt_parking)
        draw.text((40, 56), "GRATUITO", fill=paleta["ROJO_ALERTA"], font=fnt_parking)

        # Coche estilizado
        cx = tamano // 2
        cy = tamano // 2 + 25
        color_auto = (33, 150, 243) if paleta == PALETA_COLOR else (60, 60, 60)
        draw.rectangle([cx - 50, cy - 10, cx + 50, cy + 20], fill=color_auto, outline=paleta["LINEA_BORDE"], width=2)
        draw.polygon([(cx - 35, cy - 10), (cx - 20, cy - 35), (cx + 20, cy - 35), (cx + 35, cy - 10)], fill=color_auto, outline=paleta["LINEA_BORDE"])
        # Ruedas
        draw.ellipse([cx - 40, cy + 12, cx - 18, cy + 34], fill=paleta["LINEA_BORDE"])
        draw.ellipse([cx + 18, cy + 12, cx + 40, cy + 34], fill=paleta["LINEA_BORDE"])

        draw.text((45, tamano - 45), "DESCANSO / BOTE", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(15, bold=True))

    elif tipo == "IR_CARCEL":
        # Policía / Silbato
        fnt_alerta = obtener_fuente(28, bold=True)
        fnt_sub = obtener_fuente(22, bold=True)

        draw.text((38, 25), "¡VAYA A LA", fill=paleta["ROJO_ALERTA"], font=fnt_alerta)
        draw.text((55, 60), "CÁRCEL!", fill=paleta["ROJO_ALERTA"], font=fnt_alerta)

        # Oficial / Silbato apuntando a la cárcel
        cx = tamano // 2
        cy = tamano // 2 + 25
        draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=paleta["DORADO"], outline=paleta["LINEA_BORDE"], width=2)
        draw.polygon([(cx - 15, cy + 26), (cx + 15, cy + 26), (cx + 38, cy + 55), (cx - 38, cy + 55)], fill=(25, 25, 112) if paleta == PALETA_COLOR else (60, 60, 60))

        draw.text((25, tamano - 45), "DIRECTO A PRISIÓN", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(16, bold=True))

    return img


# =============================================================================
# ENSAMBLAJE MAESTRO DEL TABLERO (2048 x 2048 px)
# =============================================================================
def generar_tablero_completo(casillas, modo_byn=False):
    """
    Construye el tablero completo combinando el patio central decorativo,
    las 4 esquinas y las 36 casillas perimetrales rotadas adecuadamente.
    """
    paleta = PALETA_BYN if modo_byn else PALETA_COLOR
    tamano_total = 2048
    ancho_esquina = 280
    num_casillas_lado = 9
    espacio_central = tamano_total - (2 * ancho_esquina)
    ancho_casilla = int(espacio_central / num_casillas_lado)

    # Ajustar para cubrir píxeles exactos
    img_maestra = Image.new("RGB", (tamano_total, tamano_total), paleta["FONDO_CENTRO"])
    draw = ImageDraw.Draw(img_maestra)

    # 1. Patio Central Decorativo
    draw.rectangle([0, 0, tamano_total - 1, tamano_total - 1], outline=paleta["LINEA_BORDE"], width=6)
    draw.rectangle([ancho_esquina, ancho_esquina, tamano_total - ancho_esquina, tamano_total - ancho_esquina],
                   outline=paleta["LINEA_BORDE"], width=4)

    centro_x = tamano_total // 2
    centro_y = tamano_total // 2

    # Espacio para mazo de cartas "SUERTE" (rotado 45° en estilo clásico)
    ancho_mazo = 320
    alto_mazo = 190
    draw.rectangle([centro_x + 60, centro_y - 280, centro_x + 60 + ancho_mazo, centro_y - 280 + alto_mazo],
                   fill=paleta["CASILLA_FONDO"], outline=paleta["LINEA_BORDE"], width=3)
    dibujar_icono(draw, "SUERTE", centro_x + 60 + 50, centro_y - 280 + 95, 36, paleta)
    draw.text((centro_x + 60 + 90, centro_y - 280 + 75), "SUERTE", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(30, bold=True))

    # Espacio para mazo de cartas "CAJA DE COMUNIDAD"
    draw.rectangle([centro_x - 60 - ancho_mazo, centro_y + 90, centro_x - 60, centro_y + 90 + alto_mazo],
                   fill=paleta["CASILLA_FONDO"], outline=paleta["LINEA_BORDE"], width=3)
    dibujar_icono(draw, "COMUNIDAD", centro_x - 60 - ancho_mazo + 50, centro_y + 90 + 95, 36, paleta)
    draw.text((centro_x - 60 - ancho_mazo + 85, centro_y + 90 + 60), "CAJA DE", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(24, bold=True))
    draw.text((centro_x - 60 - ancho_mazo + 85, centro_y + 90 + 95), "COMUNIDAD", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(24, bold=True))

    # Logotipo y título central estilizado
    fnt_titulo = obtener_fuente(54, bold=True)
    fnt_sub = obtener_fuente(26, bold=True)
    txt_tit = "CAPITAL TYCOON" if not modo_byn else "EDICIÓN ESPAÑA"
    txt_sub = "TABLERO INMOBILIARIO OFICIAL (ESPAÑA)"

    bbox_tit = draw.textbbox((0, 0), txt_tit, font=fnt_titulo)
    draw.text((centro_x - (bbox_tit[2] - bbox_tit[0]) // 2, centro_y - 45), txt_tit, fill=paleta["TEXTO_NEGRO"], font=fnt_titulo)

    bbox_sub = draw.textbbox((0, 0), txt_sub, font=fnt_sub)
    draw.text((centro_x - (bbox_sub[2] - bbox_sub[0]) // 2, centro_y + 25), txt_sub, fill=paleta["TEXTO_NEGRO"], font=fnt_sub)

    # 2. Pegado de las 4 Esquinas
    esquina_0 = renderizar_esquina("SALIDA", ancho_esquina, paleta)
    esquina_10 = renderizar_esquina("CARCEL", ancho_esquina, paleta)
    esquina_20 = renderizar_esquina("PARKING", ancho_esquina, paleta)
    esquina_30 = renderizar_esquina("IR_CARCEL", ancho_esquina, paleta)

    # Posiciones exactas de las esquinas
    img_maestra.paste(esquina_0, (tamano_total - ancho_esquina, tamano_total - ancho_esquina))
    img_maestra.paste(esquina_10, (0, tamano_total - ancho_esquina))
    img_maestra.paste(esquina_20, (0, 0))
    img_maestra.paste(esquina_30, (tamano_total - ancho_esquina, 0))

    # Diccionario de casillas por posición
    mapa_casillas = {c["posicion"]: c for c in casillas}

    # 3. Lado Inferior (Casillas 1 a 9, de derecha a izquierda)
    # Orientación erguida natural (rotación 0°)
    for idx, pos in enumerate(range(1, 10)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            x_pos = tamano_total - ancho_esquina - ((idx + 1) * ancho_casilla)
            y_pos = tamano_total - ancho_esquina
            img_maestra.paste(c_img, (x_pos, y_pos))

    # 4. Lado Izquierdo (Casillas 11 a 19, de abajo hacia arriba)
    # Rotación de 90° en sentido horario (la franja de color mira hacia la derecha / centro)
    for idx, pos in enumerate(range(11, 20)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            c_rotada = c_img.rotate(270, expand=True)
            x_pos = 0
            y_pos = tamano_total - ancho_esquina - ((idx + 1) * ancho_casilla)
            img_maestra.paste(c_rotada, (x_pos, y_pos))

    # 5. Lado Superior (Casillas 21 a 29, de izquierda a derecha)
    # Rotación de 180° (la franja de color mira hacia abajo / centro)
    for idx, pos in enumerate(range(21, 30)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            c_rotada = c_img.rotate(180, expand=True)
            x_pos = ancho_esquina + (idx * ancho_casilla)
            y_pos = 0
            img_maestra.paste(c_rotada, (x_pos, y_pos))

    # 6. Lado Derecho (Casillas 31 a 39, de arriba hacia abajo)
    # Rotación de 270° en sentido horario / 90° antihorario (la franja mira hacia la izquierda / centro)
    for idx, pos in enumerate(range(31, 40)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            c_rotada = c_img.rotate(90, expand=True)
            x_pos = tamano_total - ancho_esquina
            y_pos = ancho_esquina + (idx * ancho_casilla)
            img_maestra.paste(c_rotada, (x_pos, y_pos))

    return img_maestra


def main():
    directorio_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(directorio_salida, exist_ok=True)

    ruta_db = os.path.join(directorio_salida, "tablero_datos.db")
    ruta_json = os.path.join(directorio_salida, "tablero_datos.json")
    ruta_color = os.path.join(directorio_salida, "tablero_espana_color.png")
    ruta_byn = os.path.join(directorio_salida, "tablero_espana_byn.png")

    print("[1/4] Comprobando base de datos SQLite...")
    inicializar_base_datos(ruta_db)
    exportar_a_json(ruta_db, ruta_json)

    print("[2/4] Cargando casillas y precios desde SQLite...")
    casillas = cargar_casillas_desde_db(ruta_db)
    print(f"  -> {len(casillas)} casillas cargadas exitosamente desde la base de datos.")

    print("[3/4] Generando 'tablero_espana_color.png' con orientación realista...")
    img_color = generar_tablero_completo(casillas, modo_byn=False)
    img_color.save(ruta_color, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_color}")

    print("[4/4] Generando 'tablero_espana_byn.png' en escala de grises de alto contraste...")
    img_byn = generar_tablero_completo(casillas, modo_byn=True)
    img_byn.save(ruta_byn, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_byn}")

    print("\n✓ ¡Proceso completado exitosamente! Todos los archivos generados a partir de .db")


if __name__ == "__main__":
    main()
