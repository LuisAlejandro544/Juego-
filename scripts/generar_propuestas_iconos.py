#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GENERADOR Y CATÁLOGO DE PROPUESTAS DE ICONOS PARA CAPITAL TYCOON
=============================================================================
Este script genera un catálogo visual de variantes para los iconos del juego:
1. Bolsa de Impuestos y Finanzas (Saco clásico, Maletín, Pila de monedas).
2. Tasa de Lujo (Diamante tallado, Anillo solitario, Corona real).
3. Estaciones de Tren (Locomotora de vapor, Tren bala frontal, Silueta clásica).
4. Servicio Eléctrico (Bombilla con filamento, Rayo de energía).
5. Servicio de Aguas (Grifo con gota de agua, Gota de agua dinámica).
6. Caja de Comunidad (Cofre de madera y hierro, Caja fuerte bancaria).
7. Suerte (Interrogante 3D dinámico, Trébol de cuatro hojas).

Características técnicas:
- Renderizado a cuádruple resolución (Supersampling 4x) y reescalado con
  filtro Lanczos para bordes ultra suaves sin dientes de sierra (antialiasing).
- Exportación de iconos individuales con canal alfa (transparencia RGBA).
- Exportación de una lámina/catálogo completo ('catalogo_propuestas_iconos.png')
  ideal para visualizar y comparar en la pantalla de un teléfono móvil.
- Archivo de selección activa ('config_iconos.json') para que 'generar_tablero.py'
  tome automáticamente los iconos elegidos.
"""

import os
import sys
import json
import math

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("Error: Se requiere Pillow. Instálala con: pip install Pillow")
    sys.exit(1)


# =============================================================================
# UTILIDADES DE TIPOGRAFÍA Y DIBUJO CON SUPERSAMPLING
# =============================================================================

def obtener_fuente_sistema(tamano, bold=False):
    """Localiza fuentes TrueType en el entorno Linux/Android o usa fallback."""
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


def crear_lienzo_hi_res(tamano_final=256, escala=4):
    """
    Crea un lienzo transparente a cuádruple resolución (1024x1024) para
    dibujar con precisión matemática y luego reducir con filtro Lanczos.
    """
    tam_hi = tamano_final * escala
    img_hi = Image.new("RGBA", (tam_hi, tam_hi), (0, 0, 0, 0))
    draw_hi = ImageDraw.Draw(img_hi)
    return img_hi, draw_hi, tam_hi, escala


def finalizar_hi_res(img_hi, tamano_final=256):
    """Reduce la imagen con antialiasing de alta calidad Lanczos."""
    return img_hi.resize((tamano_final, tamano_final), resample=Image.Resampling.LANCZOS)


# =============================================================================
# GENERADORES DE VARIANTES: 1. BOLSA DE IMPUESTOS (IMPUESTO SOBRE EL CAPITAL)
# =============================================================================

def generar_bolsa_v1_saco(tamano=256):
    """Variante 1: Saco de dinero clásico de lino con lazo atado, pliegues y símbolo €."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (20 * S)

    # 1. Cuerpo redondeado de la bolsa (perfil de campana)
    color_saco = (218, 165, 32)      # Dorado ocre clásico
    color_sombra = (184, 134, 11)     # Sombra ocre
    color_borde = (40, 40, 40)        # Contorno oscuro nítido
    w_borde = 6 * S

    # Cuerpo base
    draw.ellipse([cx - (75 * S), cy - (40 * S), cx + (75 * S), cy + (75 * S)], fill=color_saco, outline=color_borde, width=w_borde)
    # Sombra volumétrica lateral derecha
    draw.chord([cx - (75 * S), cy - (40 * S), cx + (75 * S), cy + (75 * S)], start=0, end=90, fill=color_sombra)

    # 2. Cuello recogido del saco
    y_cuello = cy - (45 * S)
    draw.rectangle([cx - (35 * S), y_cuello - (10 * S), cx + (35 * S), y_cuello + (10 * S)], fill=color_saco, outline=color_borde, width=w_borde)

    # 3. Pliegues superiores (boca del saco fruncida)
    boca_pts = [
        (cx - (45 * S), y_cuello - (35 * S)),
        (cx - (20 * S), y_cuello - (20 * S)),
        (cx, y_cuello - (38 * S)),
        (cx + (20 * S), y_cuello - (20 * S)),
        (cx + (45 * S), y_cuello - (35 * S)),
        (cx + (30 * S), y_cuello - (8 * S)),
        (cx - (30 * S), y_cuello - (8 * S)),
    ]
    draw.polygon(boca_pts, fill=color_saco, outline=color_borde)
    draw.line(boca_pts + [boca_pts[0]], fill=color_borde, width=w_borde)

    # 4. Cuerda / lazo rojo con nudo decorativo
    color_lazo = (211, 47, 47)
    draw.ellipse([cx - (38 * S), y_cuello - (8 * S), cx + (38 * S), y_cuello + (8 * S)], fill=color_lazo, outline=color_borde, width=4 * S)
    # Cabos colgantes de la cuerda
    draw.line([cx - (5 * S), y_cuello + (6 * S), cx - (20 * S), y_cuello + (32 * S)], fill=color_lazo, width=6 * S)
    draw.line([cx + (5 * S), y_cuello + (6 * S), cx + (15 * S), y_cuello + (36 * S)], fill=color_lazo, width=6 * S)

    # 5. Símbolo del Euro (€) en el centro de la bolsa
    fnt_euro = obtener_fuente_sistema(56 * S, bold=True)
    txt = "€"
    bbox = draw.textbbox((0, 0), txt, font=fnt_euro)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # Sombra del euro
    draw.text((cx - tw // 2 + (2 * S), cy + (5 * S) - th // 2 + (2 * S)), txt, fill=(60, 40, 10), font=fnt_euro)
    # Euro principal
    draw.text((cx - tw // 2, cy + (5 * S) - th // 2), txt, fill=(255, 255, 255), font=fnt_euro)

    return finalizar_hi_res(img_hi, tamano)


def generar_bolsa_v2_maletin(tamano=256):
    """Variante 2: Maletín ejecutivo de piel marrón con cantoneras y cerradura de oro."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (15 * S)

    w_borde = 5 * S
    color_piel = (101, 67, 33)       # Marrón cuero
    color_piel_clara = (139, 90, 43)
    color_oro = (255, 215, 0)
    color_borde = (35, 35, 35)

    # 1. Asa del maletín
    draw.arc([cx - (35 * S), cy - (75 * S), cx + (35 * S), cy - (25 * S)], start=180, end=0, fill=color_borde, width=8 * S)
    draw.arc([cx - (35 * S), cy - (75 * S), cx + (35 * S), cy - (25 * S)], start=180, end=0, fill=color_oro, width=4 * S)

    # 2. Cuerpo del maletín
    x0, y0 = cx - (85 * S), cy - (35 * S)
    x1, y1 = cx + (85 * S), cy + (65 * S)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10 * S, fill=color_piel, outline=color_borde, width=w_borde)
    # Tapa divisoria horizontal
    draw.line([x0, cy + (5 * S), x1, cy + (5 * S)], fill=color_borde, width=4 * S)
    draw.rectangle([x0 + 4 * S, y0 + 4 * S, x1 - 4 * S, cy + (3 * S)], fill=color_piel_clara)

    # 3. Broches y cerradura de oro
    draw.rectangle([cx - (15 * S), cy - (5 * S), cx + (15 * S), cy + (15 * S)], fill=color_oro, outline=color_borde, width=3 * S)
    draw.rectangle([cx - (65 * S), cy - (2 * S), cx - (45 * S), cy + (12 * S)], fill=color_oro, outline=color_borde, width=3 * S)
    draw.rectangle([cx + (45 * S), cy - (2 * S), cx + (65 * S), cy + (12 * S)], fill=color_oro, outline=color_borde, width=3 * S)

    # Ojo de la cerradura
    draw.ellipse([cx - (3 * S), cy, cx + (3 * S), cy + (6 * S)], fill=color_borde)
    draw.polygon([(cx - 2 * S, cy + 5 * S), (cx + 2 * S, cy + 5 * S), (cx, cy + 10 * S)], fill=color_borde)

    # Detalle € en la tapa
    fnt_euro = obtener_fuente_sistema(28 * S, bold=True)
    draw.text((cx - 10 * S, y0 + 8 * S), "€", fill=color_oro, font=fnt_euro)

    return finalizar_hi_res(img_hi, tamano)


def generar_bolsa_v3_monedas(tamano=256):
    """Variante 3: Pilas de monedas de oro con relieve y brillo."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (20 * S)

    color_oro = (255, 193, 7)
    color_oro_claro = (255, 236, 179)
    color_oro_oscuro = (255, 143, 0)
    color_borde = (35, 35, 35)
    w_borde = 4 * S

    def dibujar_moneda(mx, my, ancho, alto):
        # Cuerpo cilíndrico
        draw.rectangle([mx - ancho // 2, my, mx + ancho // 2, my + alto // 2], fill=color_oro_oscuro, outline=color_borde, width=w_borde)
        # Borde inferior
        draw.ellipse([mx - ancho // 2, my + alto // 4, mx + ancho // 2, my + alto], fill=color_oro_oscuro, outline=color_borde, width=w_borde)
        # Cara superior elíptica
        draw.ellipse([mx - ancho // 2, my - alto // 2, mx + ancho // 2, my + alto // 2], fill=color_oro, outline=color_borde, width=w_borde)
        # Brillo interno
        draw.ellipse([mx - ancho // 3, my - alto // 3, mx + ancho // 3, my + alto // 3], fill=color_oro_claro)

    # Columna izquierda
    for i in range(4):
        dibujar_moneda(cx - (42 * S), cy + (25 * S) - (i * 18 * S), 65 * S, 28 * S)

    # Columna derecha
    for i in range(3):
        dibujar_moneda(cx + (42 * S), cy + (35 * S) - (i * 18 * S), 65 * S, 28 * S)

    # Columna central más alta
    for i in range(6):
        dibujar_moneda(cx, cy + (25 * S) - (i * 18 * S), 75 * S, 30 * S)

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 2. TASA DE LUJO
# =============================================================================

def generar_lujo_v1_diamante(tamano=256):
    """Variante 1: Diamante tallado de alto brillo con facetas cristalinas en azul y blanco."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_borde = (30, 30, 30)
    w_borde = 5 * S

    # Coordenadas de los vértices del diamante
    top_y = cy - (55 * S)
    mid_y = cy - (15 * S)
    bot_y = cy + (65 * S)

    x_c = cx
    x_l1, x_r1 = cx - (35 * S), cx + (35 * S)
    x_l2, x_r2 = cx - (75 * S), cx + (75 * S)

    # Mesa superior y corona
    # Faceta central superior
    draw.polygon([(x_l1, top_y), (x_r1, top_y), (x_c, mid_y)], fill=(227, 242, 253), outline=color_borde, width=w_borde)
    # Faceta lateral izq superior
    draw.polygon([(x_l1, top_y), (x_l2, mid_y), (x_c, mid_y)], fill=(187, 222, 251), outline=color_borde, width=w_borde)
    # Faceta lateral der superior
    draw.polygon([(x_r1, top_y), (x_r2, mid_y), (x_c, mid_y)], fill=(144, 202, 249), outline=color_borde, width=w_borde)

    # Pabellón inferior (cono que baja al vértice inferior)
    draw.polygon([(x_l2, mid_y), (x_c, mid_y), (x_c, bot_y)], fill=(100, 181, 246), outline=color_borde, width=w_borde)
    draw.polygon([(x_r2, mid_y), (x_c, mid_y), (x_c, bot_y)], fill=(33, 150, 243), outline=color_borde, width=w_borde)

    # Destello de brillo estelar (brillante blanco)
    draw.polygon([(x_l1 - 10 * S, top_y - 10 * S), (x_l1, top_y - 25 * S), (x_l1 + 10 * S, top_y - 10 * S), (x_l1 + 25 * S, top_y), (x_l1 + 10 * S, top_y + 10 * S), (x_l1, top_y + 25 * S), (x_l1 - 10 * S, top_y + 10 * S), (x_l1 - 25 * S, top_y)], fill=(255, 255, 255))

    return finalizar_hi_res(img_hi, tamano)


def generar_lujo_v2_anillo(tamano=256):
    """Variante 2: Anillo de compromiso solitario de oro pulido con diamante."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (15 * S)

    color_oro = (255, 193, 7)
    color_borde = (30, 30, 30)
    w_borde = 5 * S

    # Aro del anillo
    draw.ellipse([cx - (60 * S), cy - (40 * S), cx + (60 * S), cy + (60 * S)], fill=color_oro, outline=color_borde, width=w_borde)
    draw.ellipse([cx - (38 * S), cy - (18 * S), cx + (38 * S), cy + (38 * S)], fill=(0, 0, 0, 0), outline=color_borde, width=w_borde)

    # Montura del diamante
    y_m = cy - (48 * S)
    draw.polygon([(cx - (20 * S), y_m), (cx + (20 * S), y_m), (cx + (10 * S), y_m + (18 * S)), (cx - (10 * S), y_m + (18 * S))], fill=(220, 220, 220), outline=color_borde, width=w_borde)

    # Piedra preciosa diamante
    y_d = y_m - (25 * S)
    draw.polygon([(cx - (16 * S), y_d), (cx + (16 * S), y_d), (cx + (24 * S), y_d + (12 * S)), (cx, y_d + (30 * S)), (cx - (24 * S), y_d + (12 * S))], fill=(179, 229, 252), outline=color_borde, width=w_borde)
    draw.polygon([(cx - (8 * S), y_d), (cx + (8 * S), y_d), (cx, y_d + (30 * S))], fill=(255, 255, 255))

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 3. ESTACIÓN DE TREN
# =============================================================================

def generar_tren_v1_vapor(tamano=256):
    """Variante 1: Locomotora de vapor clásica con chimenea, faro, cabina y nubes de humo."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (15 * S)

    color_cuerpo = (35, 35, 35)
    color_borde = (15, 15, 15)
    color_rojo = (211, 47, 47)
    color_oro = (255, 193, 7)
    color_vapor = (220, 220, 220)
    w_borde = 4 * S

    # Nubes de vapor saliendo de la chimenea
    draw.ellipse([cx + (20 * S), cy - (75 * S), cx + (45 * S), cy - (55 * S)], fill=color_vapor)
    draw.ellipse([cx + (35 * S), cy - (90 * S), cx + (70 * S), cy - (65 * S)], fill=color_vapor)

    # Cabina trasera (izquierda)
    draw.rectangle([cx - (75 * S), cy - (45 * S), cx - (20 * S), cy + (25 * S)], fill=color_cuerpo, outline=color_borde, width=w_borde)
    # Ventana cabina
    draw.rectangle([cx - (65 * S), cy - (35 * S), cx - (30 * S), cy - (15 * S)], fill=(179, 229, 252), outline=color_borde, width=3 * S)
    # Techo curvado cabina
    draw.arc([cx - (78 * S), cy - (55 * S), cx - (17 * S), cy - (35 * S)], start=180, end=0, fill=color_borde, width=6 * S)

    # Caldera horizontal cilíndrica (derecha)
    draw.rectangle([cx - (20 * S), cy - (25 * S), cx + (55 * S), cy + (25 * S)], fill=color_cuerpo, outline=color_borde, width=w_borde)

    # Chimenea frontal
    draw.polygon([(cx + (25 * S), cy - (25 * S)), (cx + (45 * S), cy - (25 * S)), (cx + (50 * S), cy - (55 * S)), (cx + (20 * S), cy - (55 * S))], fill=color_cuerpo, outline=color_borde, width=w_borde)

    # Faro delantero
    draw.rectangle([cx + (55 * S), cy - (15 * S), cx + (68 * S), cy], fill=color_oro, outline=color_borde, width=3 * S)

    # Quitapiedras / defensa delantera (cuña roja)
    draw.polygon([(cx + (55 * S), cy + (15 * S)), (cx + (78 * S), cy + (35 * S)), (cx + (55 * S), cy + (35 * S))], fill=color_rojo, outline=color_borde, width=3 * S)

    # Ruedas motrices con radios
    # Rueda trasera grande
    r_cx1, r_cy1 = cx - (45 * S), cy + (30 * S)
    draw.ellipse([r_cx1 - (22 * S), r_cy1 - (22 * S), r_cx1 + (22 * S), r_cy1 + (22 * S)], fill=(70, 70, 70), outline=color_borde, width=w_borde)
    draw.ellipse([r_cx1 - (6 * S), r_cy1 - (6 * S), r_cx1 + (6 * S), r_cy1 + (6 * S)], fill=color_oro)

    # Ruedas delanteras medianas
    for off in [0, 38]:
        r_cx = cx - (10 * S) + (off * S)
        r_cy = cy + (33 * S)
        draw.ellipse([r_cx - (16 * S), r_cy - (16 * S), r_cx + (16 * S), r_cy + (16 * S)], fill=(70, 70, 70), outline=color_borde, width=w_borde)
        draw.ellipse([r_cx - (4 * S), r_cy - (4 * S), r_cx + (4 * S), r_cy + (4 * S)], fill=color_oro)

    # Biela de acoplamiento de ruedas
    draw.line([r_cx1, r_cy1 + 4 * S, cx + 28 * S, cy + 35 * S], fill=color_oro, width=4 * S)

    return finalizar_hi_res(img_hi, tamano)


def generar_tren_v2_moderno(tamano=256):
    """Variante 2: Frontal estilizado de tren rápido / metro moderno."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_cuerpo = (245, 245, 245)
    color_franja = (211, 47, 47)
    color_borde = (30, 30, 30)
    w_borde = 5 * S

    # Perfil aerodinámico frontal
    pts_tren = [
        (cx - (45 * S), cy - (65 * S)),
        (cx + (45 * S), cy - (65 * S)),
        (cx + (60 * S), cy + (10 * S)),
        (cx + (55 * S), cy + (65 * S)),
        (cx - (55 * S), cy + (65 * S)),
        (cx - (60 * S), cy + (10 * S)),
    ]
    draw.polygon(pts_tren, fill=color_cuerpo, outline=color_borde)
    draw.line(pts_tren + [pts_tren[0]], fill=color_borde, width=w_borde)

    # Parabrisas tintado
    draw.polygon([(cx - 38 * S, cy - 45 * S), (cx + 38 * S, cy - 45 * S), (cx + 48 * S, cy - 10 * S), (cx - 48 * S, cy - 10 * S)], fill=(55, 71, 79), outline=color_borde, width=3 * S)

    # Franja de velocidad roja
    draw.rectangle([cx - 52 * S, cy + 2 * S, cx + 52 * S, cy + 18 * S], fill=color_franja)

    # Faros LED frontales
    draw.ellipse([cx - 42 * S, cy + 28 * S, cx - 24 * S, cy + 42 * S], fill=(255, 235, 59), outline=color_borde, width=3 * S)
    draw.ellipse([cx + 24 * S, cy + 28 * S, cx + 42 * S, cy + 42 * S], fill=(255, 235, 59), outline=color_borde, width=3 * S)

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 4. SERVICIO DE ELECTRICIDAD (BOMBILLA)
# =============================================================================

def generar_luz_v1_bombilla(tamano=256):
    """Variante 1: Bombilla de incandescencia detallada con filamento brillante y casquillo roscado."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 - (10 * S)

    color_cristal = (255, 238, 88)     # Amarillo radiante
    color_borde = (35, 35, 35)
    color_metal = (158, 158, 158)
    w_borde = 5 * S

    # Rayos luminosos alrededor de la ampolla
    for angulo_deg in [220, 250, 270, 290, 320]:
        rad = math.radians(angulo_deg)
        r0 = 70 * S
        r1 = 88 * S
        x0 = cx + int(r0 * math.cos(rad))
        y0 = cy + int(r0 * math.sin(rad))
        x1 = cx + int(r1 * math.cos(rad))
        y1 = cy + int(r1 * math.sin(rad))
        draw.line([x0, y0, x1, y1], fill=(255, 179, 0), width=5 * S)

    # Ampolla de cristal superior (esfera que se estrecha)
    draw.ellipse([cx - (55 * S), cy - (55 * S), cx + (55 * S), cy + (45 * S)], fill=color_cristal, outline=color_borde, width=w_borde)
    # Cuello de la bombilla
    draw.polygon([(cx - (30 * S), cy + (35 * S)), (cx + (30 * S), cy + (35 * S)), (cx + (22 * S), cy + (65 * S)), (cx - (22 * S), cy + (65 * S))], fill=color_cristal, outline=color_borde, width=w_borde)

    # Filamento de tungsteno interior (doble espiral)
    draw.line([cx - (15 * S), cy + (25 * S), cx - (12 * S), cy - (10 * S)], fill=color_borde, width=3 * S)
    draw.line([cx + (15 * S), cy + (25 * S), cx + (12 * S), cy - (10 * S)], fill=color_borde, width=3 * S)
    draw.arc([cx - (15 * S), cy - (25 * S), cx + (15 * S), cy - (5 * S)], start=180, end=0, fill=(211, 47, 47), width=4 * S)

    # Casquillo roscado metálico
    y_c = cy + (65 * S)
    for r in range(3):
        draw.rounded_rectangle([cx - (20 * S), y_c + (r * 10 * S), cx + (20 * S), y_c + ((r + 1) * 10 * S)], radius=3 * S, fill=color_metal, outline=color_borde, width=3 * S)
    # Contacto inferior redondeado
    draw.ellipse([cx - (12 * S), y_c + (26 * S), cx + (12 * S), y_c + (36 * S)], fill=(66, 66, 66))

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 5. SERVICIO DE AGUAS (GRIFO)
# =============================================================================

def generar_agua_v1_grifo(tamano=256):
    """Variante 1: Grifo clásico con llave de mariposa y gota de agua cristalina cayendo."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2 - (10 * S), T // 2 - (15 * S)

    color_grifo = (78, 93, 108)       # Metal azul acero
    color_borde = (30, 30, 30)
    color_agua = (33, 150, 243)
    color_agua_brillo = (187, 222, 251)
    w_borde = 5 * S

    # Tubería horizontal
    draw.rectangle([cx - (55 * S), cy - (15 * S), cx + (25 * S), cy + (15 * S)], fill=color_grifo, outline=color_borde, width=w_borde)

    # Llave de paso superior (volante / mariposa)
    draw.rectangle([cx - (15 * S), cy - (32 * S), cx - (5 * S), cy - (15 * S)], fill=color_grifo, outline=color_borde, width=3 * S)
    draw.rounded_rectangle([cx - (32 * S), cy - (42 * S), cx + (12 * S), cy - (30 * S)], radius=4 * S, fill=(211, 47, 47), outline=color_borde, width=w_borde)

    # Boca curvada hacia abajo
    draw.rectangle([cx + (10 * S), cy + (12 * S), cx + (32 * S), cy + (35 * S)], fill=color_grifo, outline=color_borde, width=w_borde)
    draw.rectangle([cx + (8 * S), cy + (33 * S), cx + (34 * S), cy + (40 * S)], fill=(120, 144, 156), outline=color_borde, width=3 * S)

    # Gota de agua cristalina cayendo
    gx = cx + (21 * S)
    gy = cy + (65 * S)
    draw.ellipse([gx - (14 * S), gy, gx + (14 * S), gy + (26 * S)], fill=color_agua, outline=color_borde, width=3 * S)
    draw.polygon([(gx - (12 * S), gy + (8 * S)), (gx + (12 * S), gy + (8 * S)), (gx, gy - (10 * S))], fill=color_agua, outline=color_borde)
    draw.ellipse([gx - (6 * S), gy + (4 * S), gx, gy + (12 * S)], fill=color_agua_brillo)

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 6. CAJA DE COMUNIDAD (COFRES Y CAJA FUERTE)
# =============================================================================

def generar_comunidad_v1_cofre(tamano=256):
    """Variante 1: Cofre del tesoro de madera noble cerrado con herrajes de forja."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_madera = (121, 85, 72)
    color_hierro = (55, 71, 79)
    color_oro = (255, 193, 7)
    color_borde = (30, 30, 30)
    w_borde = 5 * S

    # Tapa redondeada del cofre
    draw.chord([cx - (65 * S), cy - (55 * S), cx + (65 * S), cy + (5 * S)], start=180, end=0, fill=color_madera, outline=color_borde, width=w_borde)
    # Bandas de hierro en la tapa
    draw.arc([cx - (65 * S), cy - (55 * S), cx + (65 * S), cy + (5 * S)], start=180, end=0, fill=color_hierro, width=12 * S)
    draw.arc([cx - (65 * S), cy - (55 * S), cx + (65 * S), cy + (5 * S)], start=180, end=0, fill=color_borde, width=w_borde)

    # Cuerpo principal rectangular
    draw.rectangle([cx - (65 * S), cy, cx + (65 * S), cy + (55 * S)], fill=color_madera, outline=color_borde, width=w_borde)
    # Esquinas y refuerzos de hierro
    draw.rectangle([cx - (65 * S), cy, cx - (45 * S), cy + (55 * S)], fill=color_hierro, outline=color_borde, width=3 * S)
    draw.rectangle([cx + (45 * S), cy, cx + (65 * S), cy + (55 * S)], fill=color_hierro, outline=color_borde, width=3 * S)

    # Cerradura central de oro
    draw.rounded_rectangle([cx - (15 * S), cy - (8 * S), cx + (15 * S), cy + (20 * S)], radius=4 * S, fill=color_oro, outline=color_borde, width=3 * S)
    draw.ellipse([cx - (4 * S), cy - (2 * S), cx + (4 * S), cy + (6 * S)], fill=color_borde)
    draw.polygon([(cx - 2 * S, cy + 4 * S), (cx + 2 * S, cy + 4 * S), (cx, cy + 12 * S)], fill=color_borde)

    return finalizar_hi_res(img_hi, tamano)


def generar_comunidad_v2_cofre_oro(tamano=256):
    """
    Variante 2 (NUEVA): Cofre del tesoro entreabierto rebosante de monedas de oro brillantes.
    Diseñado específicamente para tener un contraste ultra alto y silueta abierta
    que nunca se empaste al reducirse de tamaño.
    """
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (15 * S)

    color_madera = (139, 69, 19)      # Caoba cálida
    color_madera_oscura = (92, 45, 12)
    color_oro_monedas = (255, 215, 0)  # Oro brillante
    color_oro_sombra = (218, 165, 32)
    color_oro_brillo = (255, 249, 196)
    color_hierro = (55, 71, 79)
    color_borde = (25, 20, 15)
    w_borde = 5 * S

    # 1. Resplandor dorado de fondo detrás de la tapa
    draw.ellipse([cx - (75 * S), cy - (90 * S), cx + (75 * S), cy + (10 * S)], fill=(255, 236, 179, 180))

    # 2. Tapa abierta inclinada hacia atrás
    pts_tapa = [
        (cx - (70 * S), cy - (40 * S)),
        (cx + (70 * S), cy - (40 * S)),
        (cx + (60 * S), cy - (85 * S)),
        (cx - (60 * S), cy - (85 * S))
    ]
    draw.polygon(pts_tapa, fill=color_madera, outline=color_borde)
    draw.line(pts_tapa + [pts_tapa[0]], fill=color_borde, width=w_borde)

    # Forro interior de terciopelo carmesí visible en la tapa
    pts_forro = [
        (cx - (55 * S), cy - (46 * S)),
        (cx + (55 * S), cy - (46 * S)),
        (cx + (48 * S), cy - (78 * S)),
        (cx - (48 * S), cy - (78 * S))
    ]
    draw.polygon(pts_forro, fill=(183, 28, 28), outline=color_borde, width=2 * S)

    # 3. Montaña de monedas de oro en el interior del cofre (resaltan intensamente)
    draw.ellipse([cx - (60 * S), cy - (45 * S), cx + (60 * S), cy + (5 * S)], fill=color_oro_monedas, outline=color_borde, width=w_borde)
    
    # Textura de monedas superpuestas con brillos individuales
    posiciones_monedas = [
        (cx - 35 * S, cy - 25 * S), (cx - 15 * S, cy - 32 * S), (cx + 10 * S, cy - 30 * S), (cx + 35 * S, cy - 22 * S),
        (cx - 25 * S, cy - 12 * S), (cx, cy - 18 * S), (cx + 25 * S, cy - 10 * S),
        (cx - 40 * S, cy - 5 * S), (cx + 40 * S, cy - 2 * S)
    ]
    for mx, my in posiciones_monedas:
        draw.ellipse([mx - (10 * S), my - (6 * S), mx + (10 * S), my + (6 * S)], fill=color_oro_sombra, outline=color_borde, width=2 * S)
        draw.ellipse([mx - (8 * S), my - (5 * S), mx + (8 * S), my + (4 * S)], fill=color_oro_monedas)
        draw.ellipse([mx - (4 * S), my - (4 * S), mx + (2 * S), my], fill=color_oro_brillo)

    # Destello estelar de brillo (4 puntas) saliendo del tesoro
    dx, dy = cx - (20 * S), cy - (40 * S)
    draw.polygon([(dx, dy - 18 * S), (dx + 4 * S, dy - 4 * S), (dx + 18 * S, dy), (dx + 4 * S, dy + 4 * S),
                  (dx, dy + 18 * S), (dx - 4 * S, dy + 4 * S), (dx - 18 * S, dy), (dx - 4 * S, dy - 4 * S)], fill=(255, 255, 255))

    # 4. Cuerpo frontal del cofre de caoba
    draw.rectangle([cx - (68 * S), cy - (8 * S), cx + (68 * S), cy + (52 * S)], fill=color_madera, outline=color_borde, width=w_borde)

    # Tablones de madera con hendidura
    draw.line([cx - (68 * S), cy + (22 * S), cx + (68 * S), cy + (22 * S)], fill=color_madera_oscura, width=3 * S)

    # Herrajes y esquinas reforzadas de hierro con remaches
    draw.rectangle([cx - (68 * S), cy - (8 * S), cx - (48 * S), cy + (52 * S)], fill=color_hierro, outline=color_borde, width=3 * S)
    draw.rectangle([cx + (48 * S), cy - (8 * S), cx + (68 * S), cy + (52 * S)], fill=color_hierro, outline=color_borde, width=3 * S)

    # Remaches circulares en los herrajes
    for ry in [cy + (2 * S), cy + (40 * S)]:
        draw.ellipse([cx - (60 * S), ry - (3 * S), cx - (54 * S), ry + (3 * S)], fill=color_oro_monedas)
        draw.ellipse([cx + (54 * S), ry - (3 * S), cx + (60 * S), ry + (3 * S)], fill=color_oro_monedas)

    # Gran cerradura dorada en el centro
    draw.rounded_rectangle([cx - (16 * S), cy - (4 * S), cx + (16 * S), cy + (26 * S)], radius=4 * S, fill=color_oro_monedas, outline=color_borde, width=3 * S)
    draw.ellipse([cx - (5 * S), cy + (4 * S), cx + (5 * S), cy + (12 * S)], fill=color_borde)
    draw.polygon([(cx - 3 * S, cy + 10 * S), (cx + 3 * S, cy + 10 * S), (cx, cy + 20 * S)], fill=color_borde)

    return finalizar_hi_res(img_hi, tamano)


def generar_comunidad_v3_caja_fuerte(tamano=256):
    """Variante 3: Caja fuerte blindada de acero bancario con timón giratorio dorado."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_acero = (69, 90, 100)
    color_acero_claro = (96, 125, 139)
    color_oro = (255, 215, 0)
    color_borde = (33, 33, 33)
    w_borde = 5 * S

    # Cuerpo cuadrado con bisel
    draw.rounded_rectangle([cx - (65 * S), cy - (65 * S), cx + (65 * S), cy + (65 * S)], radius=8 * S, fill=color_acero, outline=color_borde, width=w_borde)
    draw.rounded_rectangle([cx - (52 * S), cy - (52 * S), cx + (52 * S), cy + (52 * S)], radius=6 * S, fill=color_acero_claro, outline=color_borde, width=3 * S)

    # Rueda / Timón giratorio central de apertura
    draw.ellipse([cx - (28 * S), cy - (28 * S), cx + (28 * S), cy + (28 * S)], fill=color_acero, outline=color_borde, width=4 * S)
    draw.ellipse([cx - (12 * S), cy - (12 * S), cx + (12 * S), cy + (12 * S)], fill=color_oro, outline=color_borde, width=2 * S)

    # Manijas del timón (4 radios)
    for angulo in [0, 90, 180, 270]:
        rad = math.radians(angulo)
        r0 = 12 * S
        r1 = 34 * S
        x0 = cx + int(r0 * math.cos(rad))
        y0 = cy + int(r0 * math.sin(rad))
        x1 = cx + int(r1 * math.cos(rad))
        y1 = cy + int(r1 * math.sin(rad))
        draw.line([x0, y0, x1, y1], fill=color_oro, width=4 * S)
        draw.ellipse([x1 - 3 * S, y1 - 3 * S, x1 + 3 * S, y1 + 3 * S], fill=color_borde)

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 7. SUERTE (INTERROGANTE DINÁMICO)
# =============================================================================

def generar_suerte_v1_interrogante(tamano=256):
    """Variante 1: Signo de interrogación vibrante en rojo fuego con relieve y destello."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 - (5 * S)

    fnt_q = obtener_fuente_sistema(135 * S, bold=True)
    txt = "?"
    bbox = draw.textbbox((0, 0), txt, font=fnt_q)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Sombra volumétrica oscura
    draw.text((cx - tw // 2 + (6 * S), cy - th // 2 + (8 * S)), txt, fill=(120, 10, 10), font=fnt_q)
    # Cuerpo principal rojo intenso
    draw.text((cx - tw // 2, cy - th // 2), txt, fill=(229, 57, 53), font=fnt_q)
    # Relieve superior brillante
    draw.text((cx - tw // 2 - (2 * S), cy - th // 2 - (2 * S)), txt, fill=(255, 138, 128), font=fnt_q)
    draw.text((cx - tw // 2, cy - th // 2), txt, fill=(211, 47, 47), font=fnt_q)

    return finalizar_hi_res(img_hi, tamano)


# =============================================================================
# GENERADORES DE VARIANTES: 8. ESQUINAS DEL TABLERO (PARKING, POLICÍA, SALIDA)
# =============================================================================

def generar_parking_v1_coche_vintage(tamano=256):
    """Variante 1: Coche clásico descapotable de colección en rojo vivo con detalles cromados."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2 + (5 * S)

    color_coche = (211, 47, 47)        # Rojo deportivo clásico
    color_coche_sombra = (183, 28, 28)
    color_cromo = (236, 239, 241)       # Cromo pulido
    color_faros = (255, 238, 88)       # Amarillo luz
    color_ruedas = (33, 33, 33)        # Neumáticos negros
    color_borde = (25, 25, 25)
    w_borde = 5 * S

    # Sombra del coche sobre el suelo
    draw.ellipse([cx - (80 * S), cy + (45 * S), cx + (80 * S), cy + (65 * S)], fill=(0, 0, 0, 80))

    # Carrocería principal (silueta redondeada vintage)
    pts_cuerpo = [
        (cx - (75 * S), cy + (35 * S)),
        (cx - (80 * S), cy + (15 * S)),
        (cx - (70 * S), cy),
        (cx - (55 * S), cy - (10 * S)),
        (cx - (30 * S), cy - (28 * S)),   # Parabrisas
        (cx + (15 * S), cy - (28 * S)),
        (cx + (35 * S), cy - (10 * S)),
        (cx + (75 * S), cy + (10 * S)),
        (cx + (78 * S), cy + (35 * S)),
    ]
    draw.polygon(pts_cuerpo, fill=color_coche, outline=color_borde)
    draw.line(pts_cuerpo + [pts_cuerpo[0]], fill=color_borde, width=w_borde)

    # Parabrisas de cristal tintado con marco cromado
    pts_vidrio = [
        (cx - (26 * S), cy - (24 * S)),
        (cx + (12 * S), cy - (24 * S)),
        (cx + (28 * S), cy - (8 * S)),
        (cx - (42 * S), cy - (8 * S))
    ]
    draw.polygon(pts_vidrio, fill=(179, 229, 252), outline=color_borde, width=3 * S)

    # Volante visible
    draw.arc([cx - (15 * S), cy - (15 * S), cx + (5 * S), cy + (5 * S)], start=180, end=360, fill=(33, 33, 33), width=4 * S)

    # Parrilla delantera cromada
    draw.rounded_rectangle([cx + (65 * S), cy + (12 * S), cx + (77 * S), cy + (36 * S)], radius=4 * S, fill=color_cromo, outline=color_borde, width=3 * S)

    # Faros circulares con haz de luz
    draw.ellipse([cx + (50 * S), cy + (5 * S), cx + (68 * S), cy + (23 * S)], fill=color_faros, outline=color_borde, width=3 * S)
    draw.ellipse([cx + (54 * S), cy + (9 * S), cx + (64 * S), cy + (19 * S)], fill=(255, 255, 255))

    # Ruedas con tapacubos cromados
    # Rueda delantera
    rx1 = cx + (45 * S)
    draw.ellipse([rx1 - (20 * S), cy + (20 * S), rx1 + (20 * S), cy + (60 * S)], fill=color_ruedas, outline=color_borde, width=3 * S)
    draw.ellipse([rx1 - (10 * S), cy + (30 * S), rx1 + (10 * S), cy + (50 * S)], fill=color_cromo, outline=color_borde, width=2 * S)
    # Rueda trasera
    rx2 = cx - (48 * S)
    draw.ellipse([rx2 - (20 * S), cy + (20 * S), rx2 + (20 * S), cy + (60 * S)], fill=color_ruedas, outline=color_borde, width=3 * S)
    draw.ellipse([rx2 - (10 * S), cy + (30 * S), rx2 + (10 * S), cy + (50 * S)], fill=color_cromo, outline=color_borde, width=2 * S)

    return finalizar_hi_res(img_hi, tamano)


def generar_parking_v2_escudo_p(tamano=256):
    """Variante 2: Insignia heráldica de lujo con corona de laureles y letra 'P' en relieve 3D."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_oro = (255, 215, 0)
    color_oro_oscuro = (218, 165, 32)
    color_azul = (21, 101, 192)
    color_borde = (25, 25, 25)
    w_borde = 5 * S

    # Escudo circular azul zafiro con borde dorado
    draw.ellipse([cx - (75 * S), cy - (75 * S), cx + (75 * S), cy + (75 * S)], fill=color_azul, outline=color_oro, width=8 * S)
    draw.ellipse([cx - (75 * S), cy - (75 * S), cx + (75 * S), cy + (75 * S)], outline=color_borde, width=2 * S)

    # Letra "P" de Parking en gran formato con relieve blanco
    fnt_p = obtener_fuente_sistema(115 * S, bold=True)
    txt_p = "P"
    bbox = draw.textbbox((0, 0), txt_p, font=fnt_p)
    pw, ph = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px = cx - pw // 2
    py = cy - ph // 2 - (5 * S)

    # Sombra volumétrica de la "P"
    draw.text((px + 5 * S, py + 6 * S), txt_p, fill=(10, 40, 90), font=fnt_p)
    # Cuerpo blanco nítido
    draw.text((px, py), txt_p, fill=(255, 255, 255), font=fnt_p)

    return finalizar_hi_res(img_hi, tamano)


def generar_ir_carcel_v1_policia(tamano=256):
    """Variante 1: Oficial de policía con gorra de plato, silbato y dedo acusador apuntando a la cárcel."""
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_uniforme = (26, 35, 126)     # Azul marino policial
    color_piel = (255, 204, 128)       # Tono piel
    color_gorra = (13, 71, 161)
    color_placa = (255, 215, 0)
    color_borde = (20, 20, 20)
    w_borde = 5 * S

    # 1. Brazo derecho extendido apuntando con el dedo índice hacia la izquierda/abajo
    pts_brazo = [
        (cx - (15 * S), cy + (15 * S)),
        (cx - (85 * S), cy + (45 * S)),
        (cx - (75 * S), cy + (65 * S)),
        (cx - (5 * S), cy + (40 * S))
    ]
    draw.polygon(pts_brazo, fill=color_uniforme, outline=color_borde)
    draw.line(pts_brazo + [pts_brazo[0]], fill=color_borde, width=w_borde)

    # Mano con guante blanco y dedo índice apuntando
    gx, gy = cx - (82 * S), cy + (50 * S)
    draw.ellipse([gx - (12 * S), gy - (8 * S), gx + (12 * S), gy + (8 * S)], fill=(255, 255, 255), outline=color_borde, width=3 * S)
    # Dedo índice extendido
    draw.polygon([(gx - 10 * S, gy - 6 * S), (gx - 26 * S, gy + 8 * S), (gx - 18 * S, gy + 14 * S), (gx - 4 * S, gy)], fill=(255, 255, 255), outline=color_borde)

    # 2. Torso del oficial
    pts_torso = [
        (cx - (35 * S), cy + (10 * S)),
        (cx + (50 * S), cy + (10 * S)),
        (cx + (60 * S), cy + (80 * S)),
        (cx - (45 * S), cy + (80 * S))
    ]
    draw.polygon(pts_torso, fill=color_uniforme, outline=color_borde)
    draw.line(pts_torso + [pts_torso[0]], fill=color_borde, width=w_borde)

    # Cuello de camisa blanca y corbata
    draw.polygon([(cx - 8 * S, cy + 10 * S), (cx + 12 * S, cy + 10 * S), (cx + 2 * S, cy + 28 * S)], fill=(255, 255, 255))
    draw.polygon([(cx, cy + 18 * S), (cx + 4 * S, cy + 18 * S), (cx + 6 * S, cy + 50 * S), (cx - 2 * S, cy + 50 * S)], fill=(20, 20, 20))

    # Botones dorados
    for by in [cy + (35 * S), cy + (55 * S)]:
        draw.ellipse([cx + (15 * S), by, cx + (23 * S), by + (8 * S)], fill=color_placa, outline=color_borde, width=2 * S)

    # 3. Cabeza y rostro
    draw.ellipse([cx - (22 * S), cy - (32 * S), cx + (26 * S), cy + (16 * S)], fill=color_piel, outline=color_borde, width=w_borde)

    # Bigote policial clásico
    draw.polygon([(cx - (15 * S), cy - (2 * S)), (cx + (5 * S), cy - (2 * S)), (cx + (15 * S), cy + (6 * S)), (cx - (20 * S), cy + (6 * S))], fill=(50, 40, 30))

    # Silbato plateado cromado con cadenita
    draw.rectangle([cx - (24 * S), cy - (2 * S), cx - (12 * S), cy + (4 * S)], fill=(207, 216, 220), outline=color_borde, width=2 * S)

    # 4. Gorra de plato policial
    # Visera negra curvada
    draw.chord([cx - (36 * S), cy - (32 * S), cx + (38 * S), cy - (12 * S)], start=180, end=0, fill=(33, 33, 33), outline=color_borde, width=3 * S)
    # Corona / plato de la gorra azul marino
    pts_gorra = [
        (cx - (38 * S), cy - (28 * S)),
        (cx + (40 * S), cy - (28 * S)),
        (cx + (48 * S), cy - (58 * S)),
        (cx - (46 * S), cy - (58 * S))
    ]
    draw.polygon(pts_gorra, fill=color_gorra, outline=color_borde)
    draw.line(pts_gorra + [pts_gorra[0]], fill=color_borde, width=w_borde)

    # Insignia dorada en la gorra
    draw.polygon([(cx - 2 * S, cy - 54 * S), (cx + 8 * S, cy - 44 * S), (cx + 3 * S, cy - 36 * S), (cx - 7 * S, cy - 36 * S), (cx - 12 * S, cy - 44 * S)], fill=color_placa, outline=color_borde, width=2 * S)

    return finalizar_hi_res(img_hi, tamano)


def generar_salida_v1_flecha_dinamica(tamano=256):
    """
    Variante 1: Flecha monumental de ¡SALIDA! orientada obligatoriamente hacia la IZQUIERDA (⬅),
    guiando al jugador en la dirección correcta de avance por el tablero.
    """
    img_hi, draw, T, S = crear_lienzo_hi_res(tamano)
    cx, cy = T // 2, T // 2

    color_flecha = (211, 47, 47)       # Rojo intenso vibrante
    color_borde = (30, 30, 30)
    w_borde = 6 * S

    # Polígono de flecha apuntando a la IZQUIERDA (⬅)
    # Punta en (cx - 75*S, cy), base del vástago en (cx + 75*S)
    pts_flecha = [
        (cx - (80 * S), cy),               # Punta izquierda
        (cx - (15 * S), cy - (48 * S)),    # Aleta superior
        (cx - (15 * S), cy - (22 * S)),    # Quiebre superior del vástago
        (cx + (75 * S), cy - (22 * S)),    # Fin vástago superior
        (cx + (75 * S), cy + (22 * S)),    # Fin vástago inferior
        (cx - (15 * S), cy + (22 * S)),    # Quiebre inferior del vástago
        (cx - (15 * S), cy + (48 * S)),    # Aleta inferior
    ]
    # Sombra proyectada suave
    pts_sombra = [(x + 4 * S, y + 6 * S) for x, y in pts_flecha]
    draw.polygon(pts_sombra, fill=(0, 0, 0, 90))

    # Cuerpo principal de la flecha roja
    draw.polygon(pts_flecha, fill=color_flecha, outline=color_borde)
    draw.line(pts_flecha + [pts_flecha[0]], fill=color_borde, width=w_borde)

    # Brillo biselado en la mitad superior de la flecha
    draw.polygon([
        (cx - (75 * S), cy),
        (cx - (15 * S), cy - (44 * S)),
        (cx - (15 * S), cy - (20 * S)),
        (cx + (72 * S), cy - (20 * S)),
        (cx + (72 * S), cy),
    ], fill=(239, 83, 80))

    return finalizar_hi_res(img_hi, tamano)



# =============================================================================
# CATÁLOGO VISUAL MAESTRO (LÁMINA DE PROPUESTAS PARA SMARTPHONE)
# =============================================================================

def compilar_catalogo_propuestas(directorio_salida):
    """
    Genera una hoja gráfica ordenada con todas las propuestas generadas,
    organizadas por casillas con etiquetas legibles en español.
    """
    os.makedirs(directorio_salida, exist_ok=True)
    dir_iconos = os.path.join(directorio_salida, "iconos_propuestas")
    os.makedirs(dir_iconos, exist_ok=True)

    # Catálogo de elementos y variantes
    propuestas = [
        {
            "categoria": "IMPUESTO SOBRE EL CAPITAL (Casilla 4)",
            "variantes": [
                ("Opción 1: Saco Tradicional", "impuesto_saco_v1.png", generar_bolsa_v1_saco(256), True),
                ("Opción 2: Maletín Ejecutivo", "impuesto_maletin_v2.png", generar_bolsa_v2_maletin(256), False),
                ("Opción 3: Pila de Monedas", "impuesto_monedas_v3.png", generar_bolsa_v3_monedas(256), False),
            ]
        },
        {
            "categoria": "TASA DE LUJO (Casilla 38)",
            "variantes": [
                ("Opción 1: Diamante Cristalino", "lujo_diamante_v1.png", generar_lujo_v1_diamante(256), True),
                ("Opción 2: Anillo Solitario", "lujo_anillo_v2.png", generar_lujo_v2_anillo(256), False),
            ]
        },
        {
            "categoria": "ESTACIONES DE TREN (Atocha, Chamartín, Delicias, Norte)",
            "variantes": [
                ("Opción 1: Locomotora Vapor", "tren_vapor_v1.png", generar_tren_v1_vapor(256), True),
                ("Opción 2: Alta Velocidad", "tren_moderno_v2.png", generar_tren_v2_moderno(256), False),
            ]
        },
        {
            "categoria": "SERVICIOS PÚBLICOS (Luz y Aguas)",
            "variantes": [
                ("Opción 1: Bombilla de Filamento", "servicio_bombilla_v1.png", generar_luz_v1_bombilla(256), True),
                ("Opción 1: Grifo con Gota", "servicio_grifo_v1.png", generar_agua_v1_grifo(256), True),
            ]
        },
        {
            "categoria": "CAJA DE COMUNIDAD (Casillas 2, 17, 33)",
            "variantes": [
                ("Opción 1: Cofre Madera Cerrado", "comunidad_cofre_v1.png", generar_comunidad_v1_cofre(256), False),
                ("Opción 2: Cofre Abierto con Oro", "comunidad_cofre_v2.png", generar_comunidad_v2_cofre_oro(256), True),
                ("Opción 3: Caja Fuerte Blindada", "comunidad_caja_fuerte_v3.png", generar_comunidad_v3_caja_fuerte(256), False),
            ]
        },
        {
            "categoria": "SUERTE (Casillas 7, 22, 36)",
            "variantes": [
                ("Opción 1: Interrogante Relieve 3D", "suerte_interrogante_v1.png", generar_suerte_v1_interrogante(256), True),
            ]
        },
        {
            "categoria": "PARKING GRATUITO (Casilla 20 - Esquina Superior Izquierda)",
            "variantes": [
                ("Opción 1: Coche Vintage Clásico", "parking_coche_v1.png", generar_parking_v1_coche_vintage(256), True),
                ("Opción 2: Insignia Escudo P Real", "parking_escudo_v2.png", generar_parking_v2_escudo_p(256), False),
            ]
        },
        {
            "categoria": "¡VAYA A LA CÁRCEL! Y ¡SALIDA! (Esquinas)",
            "variantes": [
                ("Oficial de Policía Apuntando", "ir_carcel_policia_v1.png", generar_ir_carcel_v1_policia(256), True),
                ("Flecha Dinámica Izquierda (⬅)", "salida_flecha_v1.png", generar_salida_v1_flecha_dinamica(256), True),
            ]
        }
    ]

    # Guardar cada icono individual transparente
    config_activa = {}
    for p in propuestas:
        for nombre_op, archivo, img_icono, es_activa in p["variantes"]:
            ruta_icono = os.path.join(dir_iconos, archivo)
            img_icono.save(ruta_icono, "PNG", optimize=True)
            if es_activa:
                clave_cat = p["categoria"].split(" ")[0].lower()
                config_activa[archivo.split(".")[0]] = archivo

    ruta_config = os.path.join(dir_iconos, "config_activa.json")
    with open(ruta_config, "w", encoding="utf-8") as f:
        json.dump(config_activa, f, indent=2, ensure_ascii=False)

    # Dimensiones de la lámina de catálogo
    ancho_lamina = 1400
    alto_lamina = 2650
    img_catalogo = Image.new("RGB", (ancho_lamina, alto_lamina), (245, 247, 250))
    draw = ImageDraw.Draw(img_catalogo)

    # Encabezado del catálogo
    draw.rectangle([0, 0, ancho_lamina, 160], fill=(26, 35, 126))
    fnt_header = obtener_fuente_sistema(44, bold=True)
    fnt_sub = obtener_fuente_sistema(22, bold=False)

    draw.text((50, 35), "PROPUESTAS DE ICONOS - CAPITAL TYCOON", fill=(255, 255, 255), font=fnt_header)
    draw.text((50, 95), "Catálogo de alta definición optimizado para pantalla móvil (Dataset v2 Expandido)", fill=(207, 216, 220), font=fnt_sub)

    y_cursor = 190
    for p in propuestas:
        # Título de categoría
        fnt_cat = obtener_fuente_sistema(24, bold=True)
        draw.rectangle([40, y_cursor, ancho_lamina - 40, y_cursor + 42], fill=(227, 232, 240), outline=(176, 190, 197), width=1)
        draw.text((55, y_cursor + 8), p["categoria"], fill=(38, 50, 56), font=fnt_cat)
        y_cursor += 55

        # Fila de tarjetas para cada variante
        num_v = len(p["variantes"])
        ancho_tarjeta = (ancho_lamina - 100 - ((num_v - 1) * 30)) // num_v
        alto_tarjeta = 220

        for idx, (nombre_op, archivo, img_icono, es_activa) in enumerate(p["variantes"]):
            tx = 50 + idx * (ancho_tarjeta + 30)
            ty = y_cursor

            # Tarjeta de fondo blanco
            color_borde = (33, 150, 243) if es_activa else (200, 210, 220)
            grosor_borde = 3 if es_activa else 1
            draw.rectangle([tx, ty, tx + ancho_tarjeta, ty + alto_tarjeta], fill=(255, 255, 255), outline=color_borde, width=grosor_borde)

            # Etiqueta de la opción
            fnt_op = obtener_fuente_sistema(16, bold=True)
            draw.text((tx + 12, ty + 10), nombre_op, fill=(21, 101, 192) if es_activa else (60, 60, 60), font=fnt_op)

            # Indicador de selección activa
            if es_activa:
                draw.rectangle([tx + ancho_tarjeta - 75, ty + 8, tx + ancho_tarjeta - 10, ty + 30], fill=(76, 175, 80))
                draw.text((tx + ancho_tarjeta - 70, ty + 10), "ACTIVA", fill=(255, 255, 255), font=obtener_fuente_sistema(13, bold=True))

            # Pegado del icono en el centro de la tarjeta
            tam_icono_preview = 140
            icono_p = img_icono.resize((tam_icono_preview, tam_icono_preview), resample=Image.Resampling.LANCZOS)
            ix = tx + (ancho_tarjeta - tam_icono_preview) // 2
            iy = ty + 45
            img_catalogo.paste(icono_p, (ix, iy), icono_p)

        y_cursor += alto_tarjeta + 30

    ruta_catalogo = os.path.join(directorio_salida, "catalogo_propuestas_iconos.png")
    img_catalogo.save(ruta_catalogo, "PNG", optimize=True)
    print(f"✓ Catálogo de propuestas generado: {ruta_catalogo}")
    print(f"✓ {len(propuestas)} categorías y sus archivos individuales exportados en: {dir_iconos}")
    return ruta_catalogo


def main():
    directorio_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
    print("--- INICIANDO GENERACIÓN DE PROPUESTAS DE ICONOS ---")
    compilar_catalogo_propuestas(directorio_salida)
    print("--- PROCESO COMPLETADO SATISFACTORIAMENTE ---")


if __name__ == "__main__":
    main()
