#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR PROFESIONAL DE TABLEROS INMOBILIARIOS (EDICIÓN DINÁMICA .DB)
=============================================================================
Genera tableros visuales de alta definición (2048 x 2048 px) a partir de la
base de datos SQLite ('tablero_datos.db'):
1. Lectura directa desde SQLite: Precios, nombres y rentas son 100% editables.
2. Maquetación realista con rotación simétrica de 4 lados hacia el centro.
3. Auto-ajuste de tipografía dinámico (sin desbordes).
4. Contraste inteligente: Texto blanco sobre fondos oscuros y negro sobre claros.
5. Iconografía vectorial nítida para estaciones, servicios, impuestos y eventos.
6. Mazos de cartas decorativos en el centro con ángulos clásicos.
7. Exportación cuádruple:
   - 'output/tablero_espana_color.png'
   - 'output/tablero_espana_byn.png'
   - 'output/tablero_datos.db'
   - 'output/tablero_datos.json'
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
    "FONDO_CENTRO": (216, 234, 220),
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
    Localiza fuentes tipográficas TrueType en el sistema.
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


def ajustar_lineas_y_fuente(draw, texto, max_ancho, max_alto, tamano_max=19):
    """
    Divide inteligentemente el texto en líneas y calcula el tamaño óptimo de fuente
    para que NUNCA desborde el ancho o alto disponible de la casilla.
    """
    palabras = texto.split(" ")

    for sz in range(tamano_max, 10, -1):
        fnt = obtener_fuente(sz, bold=True)
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
            alto_total = len(lineas) * (sz + 5)
            if alto_total <= max_alto:
                return fnt, lineas, sz

    fnt_fallback = obtener_fuente(11, bold=True)
    return fnt_fallback, palabras[:3], 11


# =============================================================================
# DIBUJO DE ICONOS: DATASET DE ALTA DEFINICIÓN CON FALLBACK PROCEDURAL
# =============================================================================
CACHE_ICONOS = {}

MAPA_ARCHIVOS_ICONOS = {
    "ESTACION": "tren_vapor_v1.png",
    "SERVICIO_LUZ": "servicio_bombilla_v1.png",
    "SERVICIO_AGUA": "servicio_grifo_v1.png",
    "SUERTE": "suerte_interrogante_v1.png",
    "COMUNIDAD": "comunidad_cofre_v2.png",
    "IMPUESTO_CAPITAL": "impuesto_saco_v1.png",
    "TASA_LUJO": "lujo_diamante_v1.png",
    "PARKING_COCHE": "parking_coche_v1.png",
    "IR_CARCEL_POLICIA": "ir_carcel_policia_v1.png",
    "SALIDA_FLECHA": "salida_flecha_v1.png"
}

def dibujar_icono(img_destino, draw, tipo, x_cen, y_cen, tam, paleta):
    """
    Dibuja un icono en la casilla. Prioriza cargar el PNG en alta definición
    generado por 'generar_propuestas_iconos.py'. Si no estuviera disponible,
    utiliza el generador vectorial procedural como respaldo (fallback).
    """
    nombre_archivo = MAPA_ARCHIVOS_ICONOS.get(tipo)
    directorio_iconos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "iconos_propuestas")

    if nombre_archivo:
        ruta_archivo = os.path.join(directorio_iconos, nombre_archivo)
        if not os.path.exists(ruta_archivo):
            # Si aún no se generaron, ejecutamos el generador de propuestas automáticamente
            try:
                from generar_propuestas_iconos import compilar_catalogo_propuestas
                compilar_catalogo_propuestas(os.path.dirname(directorio_iconos))
            except Exception:
                pass

        if os.path.exists(ruta_archivo):
            clave_cache = (nombre_archivo, tam, paleta == PALETA_BYN)
            if clave_cache not in CACHE_ICONOS:
                try:
                    ico = Image.open(ruta_archivo).convert("RGBA")
                    if paleta == PALETA_BYN:
                        # Convertir a escala de grises con preservación de canal alfa
                        r, g, b, a = ico.split()
                        gris = ico.convert("L")
                        ico = Image.merge("RGBA", (gris, gris, gris, a))
                    ico_redim = ico.resize((tam, tam), resample=Image.Resampling.LANCZOS)
                    CACHE_ICONOS[clave_cache] = ico_redim
                except Exception:
                    CACHE_ICONOS[clave_cache] = None

            icono_listo = CACHE_ICONOS.get(clave_cache)
            if icono_listo:
                x_pos = int(x_cen - (tam // 2))
                y_pos = int(y_cen - (tam // 2))
                img_destino.paste(icono_listo, (x_pos, y_pos), icono_listo)
                return

    # -------------------------------------------------------------------------
    # FALLBACK PROCEDURAL (Si no se encuentra el archivo gráfico)
    # -------------------------------------------------------------------------
    color_linea = paleta["LINEA_BORDE"]
    color_relleno = paleta["TEXTO_NEGRO"]

    if tipo == "ESTACION":
        draw.rectangle([x_cen - 22, y_cen - 10, x_cen + 22, y_cen + 12], fill=color_relleno)
        draw.rectangle([x_cen - 15, y_cen - 22, x_cen + 15, y_cen - 10], fill=color_relleno)
        draw.rectangle([x_cen + 8, y_cen - 28, x_cen + 14, y_cen - 22], fill=color_relleno)
        draw.ellipse([x_cen - 18, y_cen + 10, x_cen - 6, y_cen + 22], fill=color_linea)
        draw.ellipse([x_cen + 6, y_cen + 10, x_cen + 18, y_cen + 22], fill=color_linea)
    elif tipo == "SERVICIO_LUZ":
        draw.ellipse([x_cen - 16, y_cen - 20, x_cen + 16, y_cen + 8], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.rectangle([x_cen - 8, y_cen + 8, x_cen + 8, y_cen + 18], fill=color_relleno)
    elif tipo == "SERVICIO_AGUA":
        draw.rectangle([x_cen - 16, y_cen - 16, x_cen + 10, y_cen - 6], fill=color_relleno)
        draw.rectangle([x_cen + 4, y_cen - 6, x_cen + 14, y_cen + 4], fill=color_relleno)
        draw.ellipse([x_cen + 6, y_cen + 10, x_cen + 12, y_cen + 18], fill=(66, 165, 245) if paleta == PALETA_COLOR else color_relleno)
    elif tipo == "SUERTE":
        fnt_interrogacion = obtener_fuente(46, bold=True)
        draw.text((x_cen - 14, y_cen - 26), "?", fill=paleta["ROJO_ALERTA"], font=fnt_interrogacion)
    elif tipo == "COMUNIDAD":
        draw.rectangle([x_cen - 22, y_cen - 8, x_cen + 22, y_cen + 16], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.arc([x_cen - 22, y_cen - 20, x_cen + 22, y_cen + 4], start=180, end=0, fill=color_linea, width=3)
    elif tipo == "IMPUESTO_CAPITAL":
        draw.ellipse([x_cen - 18, y_cen - 6, x_cen + 18, y_cen + 20], fill=paleta["DORADO"], outline=color_linea, width=2)
        fnt_euro = obtener_fuente(16, bold=True)
        draw.text((x_cen - 5, y_cen - 1), "€", fill=color_linea, font=fnt_euro)
    elif tipo == "TASA_LUJO":
        draw.ellipse([x_cen - 16, y_cen - 4, x_cen + 16, y_cen + 20], outline=paleta["DORADO"], width=3)
    elif tipo == "SALIDA_FLECHA":
        # Flecha apuntando a la IZQUIERDA (⬅)
        draw.polygon([(x_cen - 60, y_cen), (x_cen - 10, y_cen - 30), (x_cen - 10, y_cen - 12),
                      (x_cen + 60, y_cen - 12), (x_cen + 60, y_cen + 12), (x_cen - 10, y_cen + 12),
                      (x_cen - 10, y_cen + 30)], fill=paleta["ROJO_ALERTA"], outline=color_linea, width=2)
    elif tipo == "PARKING_COCHE":
        draw.rectangle([x_cen - 35, y_cen - 10, x_cen + 35, y_cen + 15], fill=(211, 47, 47), outline=color_linea, width=2)
        draw.polygon([(x_cen - 25, y_cen - 10), (x_cen - 15, y_cen - 25), (x_cen + 15, y_cen - 25), (x_cen + 25, y_cen - 10)], fill=(211, 47, 47), outline=color_linea)
        draw.ellipse([x_cen - 28, y_cen + 10, x_cen - 12, y_cen + 26], fill=color_linea)
        draw.ellipse([x_cen + 12, y_cen + 10, x_cen + 28, y_cen + 26], fill=color_linea)
    elif tipo == "IR_CARCEL_POLICIA":
        draw.ellipse([x_cen - 20, y_cen - 20, x_cen + 20, y_cen + 20], fill=paleta["DORADO"], outline=color_linea, width=2)
        draw.line([x_cen, y_cen, x_cen - 35, y_cen + 25], fill=color_linea, width=4)


# =============================================================================
# RENDERIZADOR DE CASILLA INDIVIDUAL (VERTICAL ESTÁNDAR)
# =============================================================================
def renderizar_casilla_estandar(casilla, ancho, alto, paleta):
    img = Image.new("RGB", (ancho, alto), paleta["CASILLA_FONDO"])
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, ancho - 1, alto - 1], outline=paleta["LINEA_BORDE"], width=2)

    alto_franja = 58
    c_tipo = casilla["tipo"]

    # 1. Franja de color
    if c_tipo == "CALLE" and casilla["grupo"] and casilla["grupo"] in paleta:
        color_grupo = paleta[casilla["grupo"]]
        draw.rectangle([0, 0, ancho - 1, alto_franja], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)

    # 2. Iconos vectoriales de alta definición
    tam_icono = 58
    if c_tipo == "ESTACION":
        dibujar_icono(img, draw, "ESTACION", ancho // 2, 70, tam_icono, paleta)
    elif c_tipo == "SERVICIO":
        if "Electricidad" in casilla["nombre"]:
            dibujar_icono(img, draw, "SERVICIO_LUZ", ancho // 2, 70, tam_icono, paleta)
        else:
            dibujar_icono(img, draw, "SERVICIO_AGUA", ancho // 2, 70, tam_icono, paleta)
    elif c_tipo == "SUERTE":
        dibujar_icono(img, draw, "SUERTE", ancho // 2, 85, 64, paleta)
    elif c_tipo == "COMUNIDAD":
        dibujar_icono(img, draw, "COMUNIDAD", ancho // 2, 85, 64, paleta)
    elif c_tipo == "IMPUESTO":
        if "Capital" in casilla["nombre"]:
            dibujar_icono(img, draw, "IMPUESTO_CAPITAL", ancho // 2, 75, tam_icono, paleta)
        else:
            dibujar_icono(img, draw, "TASA_LUJO", ancho // 2, 75, tam_icono, paleta)

    # 3. Nombre con auto-ajuste
    y_min_texto = alto_franja + 10 if c_tipo == "CALLE" else 115
    alto_disp_texto = alto - y_min_texto - 45
    max_ancho_texto = ancho - 16

    fnt_calle, lineas_texto, tam_fuente = ajustar_lineas_y_fuente(
        draw, casilla["nombre"], max_ancho_texto, alto_disp_texto, tamano_max=18
    )

    altura_linea = tam_fuente + 4
    altura_bloque = len(lineas_texto) * altura_linea
    y_offset = y_min_texto + max(0, (alto_disp_texto - altura_bloque) // 2)

    for linea in lineas_texto:
        bbox = draw.textbbox((0, 0), linea, font=fnt_calle)
        ancho_l = bbox[2] - bbox[0]
        x_pos = (ancho - ancho_l) // 2
        draw.text((x_pos, y_offset), linea, fill=paleta["TEXTO_NEGRO"], font=fnt_calle)
        y_offset += altura_linea

    # 4. Precio
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
    img = Image.new("RGB", (tamano, tamano), paleta["CASILLA_FONDO"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, tamano - 1, tamano - 1], outline=paleta["LINEA_BORDE"], width=3)

    if tipo == "SALIDA":
        # 1. Rótulo superior "¡SALIDA!" en rojo vibrante centrado
        fnt_salida = obtener_fuente(36, bold=True)
        fnt_sub = obtener_fuente(18, bold=True)
        txt_salida = "¡SALIDA!"
        bbox_s = draw.textbbox((0, 0), txt_salida, font=fnt_salida)
        draw.text(((tamano - (bbox_s[2] - bbox_s[0])) // 2, 22), txt_salida, fill=paleta["ROJO_ALERTA"], font=fnt_salida)

        # 2. Flecha apuntando obligatoriamente a la IZQUIERDA (⬅) en alta definición
        dibujar_icono(img, draw, "SALIDA_FLECHA", tamano // 2, 120, 150, paleta)

        # 3. Textos inferiores centrados
        txt_c = "COBRA 200 €"
        txt_p = "AL PASAR"
        bbox_c = draw.textbbox((0, 0), txt_c, font=fnt_sub)
        bbox_p = draw.textbbox((0, 0), txt_p, font=fnt_sub)
        draw.text(((tamano - (bbox_c[2] - bbox_c[0])) // 2, 192), txt_c, fill=paleta["TEXTO_NEGRO"], font=fnt_sub)
        draw.text(((tamano - (bbox_p[2] - bbox_p[0])) // 2, 220), txt_p, fill=paleta["TEXTO_NEGRO"], font=fnt_sub)

    elif tipo == "CARCEL":
        # Estructura oficial en "L":
        # Celda de prisión en el cuadrante interior (hacia el centro del tablero)
        # Pasillos de visita en ángulo en los bordes exteriores (izquierda y abajo)
        ancho_pasillo = 78
        x_celda = ancho_pasillo
        y_celda = 0
        w_celda = tamano - ancho_pasillo
        h_celda = tamano - ancho_pasillo

        # Fondo de la celda en grafito penitenciario de alto contraste
        color_fondo_celda = (45, 52, 58) if paleta == PALETA_COLOR else (50, 50, 50)
        draw.rectangle([x_celda, y_celda, tamano - 1, h_celda], fill=color_fondo_celda, outline=paleta["LINEA_BORDE"], width=3)

        # Barrotes de acero cilíndrico verticales con brillo volumétrico
        num_barrotes = 6
        espacio_b = w_celda // num_barrotes
        for i in range(1, num_barrotes):
            bx = x_celda + (i * espacio_b)
            # Sombra del barrote
            draw.line([bx - 2, y_celda, bx - 2, h_celda], fill=(20, 20, 20), width=3)
            # Núcleo de acero
            draw.line([bx, y_celda, bx, h_celda], fill=(176, 190, 197), width=4)
            # Reflejo de luz central
            draw.line([bx + 1, y_celda, bx + 1, h_celda], fill=(245, 245, 245), width=1)

        # Placa central enmarcada "EN LA CÁRCEL"
        pw = 140
        ph = 42
        px = x_celda + (w_celda - pw) // 2
        py = (h_celda - ph) // 2
        draw.rectangle([px, py, px + pw, py + ph], fill=(239, 108, 0) if paleta == PALETA_COLOR else (120, 120, 120),
                       outline=paleta["LINEA_BORDE"], width=2)
        fnt_celda = obtener_fuente(16, bold=True)
        txt_en_carcel = "EN LA CÁRCEL"
        bbox_ec = draw.textbbox((0, 0), txt_en_carcel, font=fnt_celda)
        draw.text((px + (pw - (bbox_ec[2] - bbox_ec[0])) // 2, py + 11), txt_en_carcel, fill=(255, 255, 255), font=fnt_celda)

        # Pasillo de visita: línea de separación nítida en "L"
        draw.line([ancho_pasillo, 0, ancho_pasillo, tamano - 1], fill=paleta["LINEA_BORDE"], width=3)
        draw.line([0, tamano - ancho_pasillo, tamano - 1, tamano - ancho_pasillo], fill=paleta["LINEA_BORDE"], width=3)

        # Rótulos en los pasillos de visita
        fnt_visita = obtener_fuente(20, bold=True)
        # Pasillo vertical izquierdo: "SOLO DE"
        txt_solo = "SOLO"
        txt_de = "DE"
        bbox_s = draw.textbbox((0, 0), txt_solo, font=fnt_visita)
        bbox_d = draw.textbbox((0, 0), txt_de, font=fnt_visita)
        draw.text(((ancho_pasillo - (bbox_s[2] - bbox_s[0])) // 2, 60), txt_solo, fill=paleta["TEXTO_NEGRO"], font=fnt_visita)
        draw.text(((ancho_pasillo - (bbox_d[2] - bbox_d[0])) // 2, 95), txt_de, fill=paleta["TEXTO_NEGRO"], font=fnt_visita)

        # Pasillo horizontal inferior: "VISITA"
        txt_vis = "VISITA"
        bbox_v = draw.textbbox((0, 0), txt_vis, font=fnt_visita)
        draw.text((ancho_pasillo + (w_celda - (bbox_v[2] - bbox_v[0])) // 2, tamano - 52), txt_vis, fill=paleta["TEXTO_NEGRO"], font=fnt_visita)

    elif tipo == "PARKING":
        fnt_parking = obtener_fuente(28, bold=True)
        txt_p1 = "PARKING"
        txt_p2 = "GRATUITO"
        bbox_p1 = draw.textbbox((0, 0), txt_p1, font=fnt_parking)
        bbox_p2 = draw.textbbox((0, 0), txt_p2, font=fnt_parking)
        draw.text(((tamano - (bbox_p1[2] - bbox_p1[0])) // 2, 18), txt_p1, fill=paleta["ROJO_ALERTA"], font=fnt_parking)
        draw.text(((tamano - (bbox_p2[2] - bbox_p2[0])) // 2, 48), txt_p2, fill=paleta["ROJO_ALERTA"], font=fnt_parking)

        # Icono de coche vintage en alta definición
        dibujar_icono(img, draw, "PARKING_COCHE", tamano // 2, 142, 130, paleta)

        # Rótulo inferior
        fnt_sub = obtener_fuente(16, bold=True)
        txt_sub = "DESCANSO / BOTE"
        bbox_sub = draw.textbbox((0, 0), txt_sub, font=fnt_sub)
        draw.text(((tamano - (bbox_sub[2] - bbox_sub[0])) // 2, tamano - 45), txt_sub, fill=paleta["TEXTO_NEGRO"], font=fnt_sub)

    elif tipo == "IR_CARCEL":
        fnt_alerta = obtener_fuente(28, bold=True)
        txt_i1 = "¡VAYA A LA"
        txt_i2 = "CÁRCEL!"
        bbox_i1 = draw.textbbox((0, 0), txt_i1, font=fnt_alerta)
        bbox_i2 = draw.textbbox((0, 0), txt_i2, font=fnt_alerta)
        draw.text(((tamano - (bbox_i1[2] - bbox_i1[0])) // 2, 18), txt_i1, fill=paleta["ROJO_ALERTA"], font=fnt_alerta)
        draw.text(((tamano - (bbox_i2[2] - bbox_i2[0])) // 2, 48), txt_i2, fill=paleta["ROJO_ALERTA"], font=fnt_alerta)

        # Icono del oficial de policía con dedo acusador en alta definición
        dibujar_icono(img, draw, "IR_CARCEL_POLICIA", tamano // 2, 142, 135, paleta)

        # Rótulo inferior
        fnt_sub = obtener_fuente(16, bold=True)
        txt_sub = "DIRECTO A PRISIÓN"
        bbox_sub = draw.textbbox((0, 0), txt_sub, font=fnt_sub)
        draw.text(((tamano - (bbox_sub[2] - bbox_sub[0])) // 2, tamano - 45), txt_sub, fill=paleta["TEXTO_NEGRO"], font=fnt_sub)

    return img


# =============================================================================
# ENSAMBLAJE MAESTRO DEL TABLERO (2048 x 2048 px)
# =============================================================================
def generar_tablero_completo(casillas, modo_byn=False):
    paleta = PALETA_BYN if modo_byn else PALETA_COLOR
    tamano_total = 2048
    ancho_esquina = 280
    num_casillas_lado = 9
    espacio_central = tamano_total - (2 * ancho_esquina)
    ancho_casilla = int(espacio_central / num_casillas_lado)

    img_maestra = Image.new("RGB", (tamano_total, tamano_total), paleta["FONDO_CENTRO"])
    draw = ImageDraw.Draw(img_maestra)

    # 1. Marco central doble decorativo
    draw.rectangle([0, 0, tamano_total - 1, tamano_total - 1], outline=paleta["LINEA_BORDE"], width=6)
    draw.rectangle([ancho_esquina, ancho_esquina, tamano_total - ancho_esquina, tamano_total - ancho_esquina],
                   outline=paleta["LINEA_BORDE"], width=4)
    draw.rectangle([ancho_esquina + 15, ancho_esquina + 15, tamano_total - ancho_esquina - 15, tamano_total - ancho_esquina - 15],
                   outline=paleta["LINEA_BORDE"], width=1)

    centro_x = tamano_total // 2
    centro_y = tamano_total // 2

    # Mazos de cartas decorativos diagonales
    ancho_mazo = 300
    alto_mazo = 180

    # Tarjeta de Suerte (arriba a la derecha)
    card_suerte = Image.new("RGBA", (ancho_mazo, alto_mazo), (0, 0, 0, 0))
    d_cs = ImageDraw.Draw(card_suerte)
    d_cs.rectangle([0, 0, ancho_mazo - 1, alto_mazo - 1], fill=paleta["CASILLA_FONDO"], outline=paleta["LINEA_BORDE"], width=3)
    dibujar_icono(card_suerte, d_cs, "SUERTE", 50, alto_mazo // 2, 52, paleta)
    d_cs.text((90, alto_mazo // 2 - 18), "SUERTE", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(28, bold=True))
    card_suerte_rot = card_suerte.rotate(-15, expand=True, resample=Image.BICUBIC)
    img_maestra.paste(card_suerte_rot, (centro_x + 90, centro_y - 290), card_suerte_rot)

    # Tarjeta de Caja de Comunidad (abajo a la izquierda)
    card_com = Image.new("RGBA", (ancho_mazo, alto_mazo), (0, 0, 0, 0))
    d_cc = ImageDraw.Draw(card_com)
    d_cc.rectangle([0, 0, ancho_mazo - 1, alto_mazo - 1], fill=paleta["CASILLA_FONDO"], outline=paleta["LINEA_BORDE"], width=3)
    dibujar_icono(card_com, d_cc, "COMUNIDAD", 50, alto_mazo // 2, 52, paleta)
    d_cc.text((85, alto_mazo // 2 - 28), "CAJA DE", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(22, bold=True))
    d_cc.text((85, alto_mazo // 2 + 2), "COMUNIDAD", fill=paleta["TEXTO_NEGRO"], font=obtener_fuente(22, bold=True))
    card_com_rot = card_com.rotate(-15, expand=True, resample=Image.BICUBIC)
    img_maestra.paste(card_com_rot, (centro_x - ancho_mazo - 90, centro_y + 100), card_com_rot)

    # Logotipo y título central
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

    img_maestra.paste(esquina_0, (tamano_total - ancho_esquina, tamano_total - ancho_esquina))
    img_maestra.paste(esquina_10, (0, tamano_total - ancho_esquina))
    img_maestra.paste(esquina_20, (0, 0))
    img_maestra.paste(esquina_30, (tamano_total - ancho_esquina, 0))

    mapa_casillas = {c["posicion"]: c for c in casillas}

    # 3. Lado Inferior (Casillas 1 a 9, de derecha a izquierda)
    # Franja arriba (hacia el interior), erguidas (0°)
    for idx, pos in enumerate(range(1, 10)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            x_pos = tamano_total - ancho_esquina - ((idx + 1) * ancho_casilla)
            y_pos = tamano_total - ancho_esquina
            img_maestra.paste(c_img, (x_pos, y_pos))

    # 4. Lado Izquierdo (Casillas 11 a 19, de abajo hacia arriba)
    # Franja a la derecha (hacia el centro), texto leído desde fuera hacia dentro: rotate(90)
    for idx, pos in enumerate(range(11, 20)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            c_rotada = c_img.rotate(270, expand=True)
            x_pos = 0
            y_pos = tamano_total - ancho_esquina - ((idx + 1) * ancho_casilla)
            img_maestra.paste(c_rotada, (x_pos, y_pos))

    # 5. Lado Superior (Casillas 21 a 29, de izquierda a derecha)
    # Franja abajo (hacia el centro), rotate(180)
    for idx, pos in enumerate(range(21, 30)):
        c_data = mapa_casillas.get(pos)
        if c_data:
            c_img = renderizar_casilla_estandar(c_data, ancho_casilla, ancho_esquina, paleta)
            c_rotada = c_img.rotate(180, expand=True)
            x_pos = ancho_esquina + (idx * ancho_casilla)
            y_pos = 0
            img_maestra.paste(c_rotada, (x_pos, y_pos))

    # 6. Lado Derecho (Casillas 31 a 39, de arriba hacia abajo)
    # Franja a la izquierda (hacia el centro), rotate(90)
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
    print(f"  -> {len(casillas)} casillas cargadas.")

    print("[3/4] Generando 'tablero_espana_color.png' pulido...")
    img_color = generar_tablero_completo(casillas, modo_byn=False)
    img_color.save(ruta_color, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_color}")

    print("[4/4] Generando 'tablero_espana_byn.png' pulido...")
    img_byn = generar_tablero_completo(casillas, modo_byn=True)
    img_byn.save(ruta_byn, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_byn}")

    print("\n✓ ¡Tableros y base de datos actualizados con éxito!")


if __name__ == "__main__":
    main()
