#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR DEL TABLERO DE BIENES RAÍCES - EDICIÓN ESPAÑA
=============================================================================
Este script genera de forma automatizada 2 versiones del tablero oficial
estándar de España (con sus 40 casillas tradicionales):
1. Versión a todo color ('tablero_espana_color.png')
2. Versión en blanco y negro / escala de grises ('tablero_espana_byn.png')

Diseñado para ejecutarse tanto localmente como dentro de un workflow de
GitHub Actions activado bajo demanda (workflow_dispatch).
"""

import os
import sys
import math

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Se requiere la librería Pillow. Instálala con: pip install Pillow")
    sys.exit(1)


# =============================================================================
# DEFINICIÓN DE LAS 40 CASILLAS OFICIALES (EDICIÓN ESTÁNDAR ESPAÑA)
# =============================================================================
# El tablero se compone de 40 casillas en sentido de las agujas del reloj,
# comenzando por la esquina inferior derecha (Salida = 0):
# - Casillas 0 a 10: Lado inferior (de derecha a izquierda)
# - Casillas 10 a 20: Lado izquierdo (de abajo hacia arriba)
# - Casillas 20 a 30: Lado superior (de izquierda a derecha)
# - Casillas 30 a 0: Lado derecho (de arriba hacia abajo)

CASILLAS_ESPANA = [
    # ESQUINA INFERIOR DERECHA
    {"id": 0, "nombre": "¡SALIDA!\nCOBRA 200€\nAL PASAR", "tipo": "SALIDA", "precio": ""},

    # LADO INFERIOR (1 a 9)
    {"id": 1, "nombre": "Ronda de\nValencia", "tipo": "CALLE", "grupo": "MARRON", "precio": "60€"},
    {"id": 2, "nombre": "Caja de\nComunidad", "tipo": "COMUNIDAD", "precio": ""},
    {"id": 3, "nombre": "Plaza\nLavapiés", "tipo": "CALLE", "grupo": "MARRON", "precio": "60€"},
    {"id": 4, "nombre": "Impuesto sobre\nel Capital", "tipo": "IMPUESTO", "precio": "PAGA 200€"},
    {"id": 5, "nombre": "Estación\nde Goya", "tipo": "ESTACION", "precio": "200€"},
    {"id": 6, "nombre": "Glorieta Cuatro\nCaminos", "tipo": "CALLE", "grupo": "CELESTE", "precio": "100€"},
    {"id": 7, "nombre": "Suerte", "tipo": "SUERTE", "precio": ""},
    {"id": 8, "nombre": "Calle Reina\nVictoria", "tipo": "CALLE", "grupo": "CELESTE", "precio": "100€"},
    {"id": 9, "nombre": "Calle Bravo\nMurillo", "tipo": "CALLE", "grupo": "CELESTE", "precio": "120€"},

    # ESQUINA INFERIOR IZQUIERDA
    {"id": 10, "nombre": "EN LA CÁRCEL\n(SOLO VISITA)", "tipo": "CARCEL", "precio": ""},

    # LADO IZQUIERDO (11 a 19)
    {"id": 11, "nombre": "Glorieta de\nBilbao", "tipo": "CALLE", "grupo": "ROSA", "precio": "140€"},
    {"id": 12, "nombre": "Compañía de\nElectricidad", "tipo": "SERVICIO", "precio": "150€"},
    {"id": 13, "nombre": "Calle Alberto\nAguilera", "tipo": "CALLE", "grupo": "ROSA", "precio": "140€"},
    {"id": 14, "nombre": "Calle\nFuencarral", "tipo": "CALLE", "grupo": "ROSA", "precio": "160€"},
    {"id": 15, "nombre": "Estación de\nlas Delicias", "tipo": "ESTACION", "precio": "200€"},
    {"id": 16, "nombre": "Avenida\nFelipe II", "tipo": "CALLE", "grupo": "NARANJA", "precio": "180€"},
    {"id": 17, "nombre": "Caja de\nComunidad", "tipo": "COMUNIDAD", "precio": ""},
    {"id": 18, "nombre": "Calle\nSerrano", "tipo": "CALLE", "grupo": "NARANJA", "precio": "180€"},
    {"id": 19, "nombre": "Calle\nVelázquez", "tipo": "CALLE", "grupo": "NARANJA", "precio": "200€"},

    # ESQUINA SUPERIOR IZQUIERDA
    {"id": 20, "nombre": "PARKING\nGRATUITO", "tipo": "PARKING", "precio": ""},

    # LADO SUPERIOR (21 a 29)
    {"id": 21, "nombre": "Avenida de\nAmérica", "tipo": "CALLE", "grupo": "ROJO", "precio": "220€"},
    {"id": 22, "nombre": "Suerte", "tipo": "SUERTE", "precio": ""},
    {"id": 23, "nombre": "Calle María\nde Molina", "tipo": "CALLE", "grupo": "ROJO", "precio": "220€"},
    {"id": 24, "nombre": "Calle Cea\nBermúdez", "tipo": "CALLE", "grupo": "ROJO", "precio": "240€"},
    {"id": 25, "nombre": "Estación de\nMediodía", "tipo": "ESTACION", "precio": "200€"},
    {"id": 26, "nombre": "Av. de los Reyes\nCatólicos", "tipo": "CALLE", "grupo": "AMARILLO", "precio": "260€"},
    {"id": 27, "nombre": "Calle\nBailén", "tipo": "CALLE", "grupo": "AMARILLO", "precio": "260€"},
    {"id": 28, "nombre": "Compañía\nde Aguas", "tipo": "SERVICIO", "precio": "150€"},
    {"id": 29, "nombre": "Plaza de\nEspaña", "tipo": "CALLE", "grupo": "AMARILLO", "precio": "280€"},

    # ESQUINA SUPERIOR DERECHA
    {"id": 30, "nombre": "¡VAYA A LA\nCÁRCEL!", "tipo": "IR_CARCEL", "precio": ""},

    # LADO DERECHO (31 a 39)
    {"id": 31, "nombre": "Puerta\ndel Sol", "tipo": "CALLE", "grupo": "VERDE", "precio": "300€"},
    {"id": 32, "nombre": "Calle\nAlcalá", "tipo": "CALLE", "grupo": "VERDE", "precio": "300€"},
    {"id": 33, "nombre": "Caja de\nComunidad", "tipo": "COMUNIDAD", "precio": ""},
    {"id": 34, "nombre": "Gran\nVía", "tipo": "CALLE", "grupo": "VERDE", "precio": "320€"},
    {"id": 35, "nombre": "Estación\ndel Norte", "tipo": "ESTACION", "precio": "200€"},
    {"id": 36, "nombre": "Suerte", "tipo": "SUERTE", "precio": ""},
    {"id": 37, "nombre": "Paseo de la\nCastellana", "tipo": "CALLE", "grupo": "AZUL", "precio": "350€"},
    {"id": 38, "nombre": "Tasa de\nLujo", "tipo": "IMPUESTO", "precio": "PAGA 100€"},
    {"id": 39, "nombre": "Paseo\ndel Prado", "tipo": "CALLE", "grupo": "AZUL", "precio": "400€"}
]

# Paleta de colores estándar para las propiedades y casillas
PALETA_COLOR = {
    "MARRON": (139, 69, 19),      # Ronda de Valencia, Lavapiés
    "CELESTE": (135, 206, 235),   # Cuatro Caminos, Reina Victoria, Bravo Murillo
    "ROSA": (255, 105, 180),      # Bilbao, Alberto Aguilera, Fuencarral
    "NARANJA": (255, 140, 0),     # Felipe II, Serrano, Velázquez
    "ROJO": (220, 20, 60),        # Av. de América, María de Molina, Cea Bermúdez
    "AMARILLO": (255, 215, 0),    # Reyes Católicos, Bailén, Plaza de España
    "VERDE": (34, 139, 34),       # Puerta del Sol, Alcalá, Gran Vía
    "AZUL": (25, 25, 112),        # Castellana, Prado
    "FONDO_CENTRO": (218, 232, 220), # Tono verde suave clásico del tablero
    "CASILLA_FONDO": (255, 255, 255),
    "LINEA_BORDE": (30, 30, 30),
    "TEXTO_NEGRO": (20, 20, 20),
    "ROJO_ALERTA": (180, 0, 0)
}

# Paleta monocromática de alto contraste para la versión Blanco y Negro
PALETA_BYN = {
    "MARRON": (80, 80, 80),
    "CELESTE": (210, 210, 210),
    "ROSA": (160, 160, 160),
    "NARANJA": (120, 120, 120),
    "ROJO": (60, 60, 60),
    "AMARILLO": (230, 230, 230),
    "VERDE": (100, 100, 100),
    "AZUL": (40, 40, 40),
    "FONDO_CENTRO": (245, 245, 245),
    "CASILLA_FONDO": (255, 255, 255),
    "LINEA_BORDE": (0, 0, 0),
    "TEXTO_NEGRO": (0, 0, 0),
    "ROJO_ALERTA": (30, 30, 30)
}


def obtener_fuente(tamano):
    """
    Intenta cargar fuentes TrueType estándar del sistema; si no existen,
    utiliza la fuente de mapa de bits por defecto de Pillow.
    """
    fuentes_candidatas = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "Arial.ttf",
        "Helvetica.ttf"
    ]
    for ruta in fuentes_candidatas:
        if os.path.exists(ruta):
            try:
                return ImageFont.truetype(ruta, tamano)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def dibujar_tablero(modo_byn=False):
    """
    Genera una imagen en alta definición (2048 x 2048 px) del tablero.
    Si modo_byn es True, utiliza escala de grises / blanco y negro.
    """
    paleta = PALETA_BYN if modo_byn else PALETA_COLOR
    tamano_total = 2048
    ancho_borde_casilla = 280
    num_casillas_lado = 9
    espacio_central = tamano_total - (2 * ancho_borde_casilla)
    ancho_casilla_normal = espacio_central / num_casillas_lado

    img = Image.new("RGB", (tamano_total, tamano_total), paleta["FONDO_CENTRO"])
    draw = ImageDraw.Draw(img)

    # Cargar diferentes tamaños de tipografía
    font_titulo = obtener_fuente(52)
    font_subtitulo = obtener_fuente(28)
    font_calle = obtener_fuente(22)
    font_precio = obtener_fuente(20)
    font_esquina = obtener_fuente(30)

    # =========================================================================
    # 1. DIBUJAR CENTRO Y ESPACIOS DECORATIVOS DEL TABLERO
    # =========================================================================
    # Borde perimetral exterior
    draw.rectangle([0, 0, tamano_total - 1, tamano_total - 1], outline=paleta["LINEA_BORDE"], width=6)

    # Línea divisoria del patio central
    draw.rectangle(
        [ancho_borde_casilla, ancho_borde_casilla, tamano_total - ancho_borde_casilla, tamano_total - ancho_borde_casilla],
        outline=paleta["LINEA_BORDE"],
        width=4
    )

    # Decoración central: Título del tablero en el centro
    centro_x = tamano_total // 2
    centro_y = tamano_total // 2

    # Espacio para mazo de cartas "CAJA DE COMUNIDAD" y "SUERTE"
    ancho_mazo = 340
    alto_mazo = 200

    # Mazo de Suerte (arriba derecha)
    draw.rectangle(
        [centro_x + 60, centro_y - 300, centro_x + 60 + ancho_mazo, centro_y - 300 + alto_mazo],
        fill=paleta["CASILLA_FONDO"],
        outline=paleta["LINEA_BORDE"],
        width=3
    )
    draw.text((centro_x + 60 + 100, centro_y - 300 + 75), "SUERTE 🍀", fill=paleta["TEXTO_NEGRO"], font=font_subtitulo)

    # Mazo de Comunidad (abajo izquierda)
    draw.rectangle(
        [centro_x - 60 - ancho_mazo, centro_y + 100, centro_x - 60, centro_y + 100 + alto_mazo],
        fill=paleta["CASILLA_FONDO"],
        outline=paleta["LINEA_BORDE"],
        width=3
    )
    draw.text((centro_x - 60 - ancho_mazo + 40, centro_y + 100 + 75), "CAJA DE COMUNIDAD ⭐", fill=paleta["TEXTO_NEGRO"], font=font_subtitulo)

    # Título central
    titulo_texto = "EDICIÓN ESPAÑA" if modo_byn else "CAPITAL TYCOON - ESPAÑA"
    sub_texto = "TABLERO INMOBILIARIO ESTÁNDAR"
    draw.text((centro_x - 240, centro_y - 40), titulo_texto, fill=paleta["TEXTO_NEGRO"], font=font_titulo)
    draw.text((centro_x - 230, centro_y + 25), sub_texto, fill=paleta["TEXTO_NEGRO"], font=font_subtitulo)

    # =========================================================================
    # 2. DIBUJAR CADA UNA DE LAS 40 CASILLAS
    # =========================================================================
    for casilla in CASILLAS_ESPANA:
        cid = casilla["id"]

        # Determinar coordenadas según la posición en el perímetro
        if cid == 0:
            # Esquina inferior derecha (SALIDA)
            x0 = tamano_total - ancho_borde_casilla
            y0 = tamano_total - ancho_borde_casilla
            x1 = tamano_total
            y1 = tamano_total
            orientacion = "ESQUINA"

        elif 1 <= cid <= 9:
            # Lado inferior (de derecha a izquierda)
            paso = cid - 1
            x1 = tamano_total - ancho_borde_casilla - (paso * ancho_casilla_normal)
            x0 = x1 - ancho_casilla_normal
            y0 = tamano_total - ancho_borde_casilla
            y1 = tamano_total
            orientacion = "SUR"

        elif cid == 10:
            # Esquina inferior izquierda (CÁRCEL)
            x0 = 0
            y0 = tamano_total - ancho_borde_casilla
            x1 = ancho_borde_casilla
            y1 = tamano_total
            orientacion = "ESQUINA"

        elif 11 <= cid <= 19:
            # Lado izquierdo (de abajo hacia arriba)
            paso = cid - 11
            y1 = tamano_total - ancho_borde_casilla - (paso * ancho_casilla_normal)
            y0 = y1 - ancho_casilla_normal
            x0 = 0
            x1 = ancho_borde_casilla
            orientacion = "OESTE"

        elif cid == 20:
            # Esquina superior izquierda (PARKING)
            x0 = 0
            y0 = 0
            x1 = ancho_borde_casilla
            y1 = ancho_borde_casilla
            orientacion = "ESQUINA"

        elif 21 <= cid <= 29:
            # Lado superior (de izquierda a derecha)
            paso = cid - 21
            x0 = ancho_borde_casilla + (paso * ancho_casilla_normal)
            x1 = x0 + ancho_casilla_normal
            y0 = 0
            y1 = ancho_borde_casilla
            orientacion = "NORTE"

        elif cid == 30:
            # Esquina superior derecha (VAYA A LA CÁRCEL)
            x0 = tamano_total - ancho_borde_casilla
            y0 = 0
            x1 = tamano_total
            y1 = ancho_borde_casilla
            orientacion = "ESQUINA"

        else: # 31 <= cid <= 39
            # Lado derecho (de arriba hacia abajo)
            paso = cid - 31
            y0 = ancho_borde_casilla + (paso * ancho_casilla_normal)
            y1 = y0 + ancho_casilla_normal
            x0 = tamano_total - ancho_borde_casilla
            x1 = tamano_total
            orientacion = "ESTE"

        # Dibujar fondo blanco de la casilla y su contorno
        draw.rectangle([x0, y0, x1, y1], fill=paleta["CASILLA_FONDO"], outline=paleta["LINEA_BORDE"], width=2)

        # Franja de color para las calles
        alto_franja = 52
        if casilla["tipo"] == "CALLE" and "grupo" in casilla:
            color_grupo = paleta[casilla["grupo"]]
            if orientacion == "SUR":
                # Franja arriba de la casilla
                draw.rectangle([x0, y0, x1, y0 + alto_franja], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)
            elif orientacion == "NORTE":
                # Franja abajo de la casilla
                draw.rectangle([x0, y1 - alto_franja, x1, y1], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)
            elif orientacion == "OESTE":
                # Franja a la derecha de la casilla
                draw.rectangle([x1 - alto_franja, y0, x1, y1], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)
            elif orientacion == "ESTE":
                # Franja a la izquierda de la casilla
                draw.rectangle([x0, y0, x0 + alto_franja, y1], fill=color_grupo, outline=paleta["LINEA_BORDE"], width=2)

        # Dibujar texto de la casilla
        lineas_nombre = casilla["nombre"].split("\n")
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2

        if orientacion == "ESQUINA":
            # Formato especial para esquinas
            y_offset = y0 + 50
            for linea in lineas_nombre:
                draw.text((x0 + 35, y_offset), linea, fill=paleta["TEXTO_NEGRO"], font=font_esquina)
                y_offset += 38

        elif orientacion in ["SUR", "NORTE"]:
            # Casillas horizontales (Norte y Sur)
            y_inicio = y0 + alto_franja + 12 if orientacion == "SUR" else y0 + 16
            for idx, linea in enumerate(lineas_nombre):
                draw.text((x0 + 12, y_inicio + (idx * 26)), linea, fill=paleta["TEXTO_NEGRO"], font=font_calle)

            if casilla["precio"]:
                draw.text((x0 + 16, y1 - 32), casilla["precio"], fill=paleta["TEXTO_NEGRO"], font=font_precio)

        elif orientacion in ["ESTE", "OESTE"]:
            # Casillas verticales (Este y Oeste)
            x_inicio = x0 + 16 if orientacion == "ESTE" else x0 + 16
            y_inicio = y0 + 20
            for idx, linea in enumerate(lineas_nombre):
                draw.text((x_inicio, y_inicio + (idx * 26)), linea, fill=paleta["TEXTO_NEGRO"], font=font_calle)

            if casilla["precio"]:
                draw.text((x_inicio, y1 - 32), casilla["precio"], fill=paleta["TEXTO_NEGRO"], font=font_precio)

    return img


def main():
    directorio_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    os.makedirs(directorio_salida, exist_ok=True)

    ruta_color = os.path.join(directorio_salida, "tablero_espana_color.png")
    ruta_byn = os.path.join(directorio_salida, "tablero_espana_byn.png")

    print("[1/2] Generando tablero oficial España a todo color...")
    img_color = dibujar_tablero(modo_byn=False)
    img_color.save(ruta_color, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_color}")

    print("[2/2] Generando tablero oficial España en Blanco y Negro...")
    img_byn = dibujar_tablero(modo_byn=True)
    img_byn.save(ruta_byn, "PNG", optimize=True)
    print(f"  -> Guardado exitosamente: {ruta_byn}")

    print("\n✓ ¡Ambos archivos PNG generados correctamente!")


if __name__ == "__main__":
    main()
