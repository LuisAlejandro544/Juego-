#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
GESTOR DE BASE DE DATOS DEL TABLERO INMOBILIARIO (SQLITE .DB)
=============================================================================
Crea y administra el archivo SQLite 'tablero_datos.db' que contiene toda la
información modificable de la partida:
1. 'casillas': Las 40 casillas con nombres, colores, precios, alquileres
   progresivos (1 a 4 casas, hotel), coste de edificación e hipoteca.
2. 'cartas_suerte': Las 16 cartas oficiales de Suerte en español.
3. 'cartas_comunidad': Las 16 cartas oficiales de Caja de Comunidad en español.
4. 'reglas_partida': Parámetros económicos configurables (dinero inicial,
   salario de salida, fianza de la cárcel, etc.).
"""

import sqlite3
import os
import json

# Definición de datos oficiales iniciales de las 40 casillas de España
CASILLAS_INICIALES = [
    # Esquina 0
    (0, 0, "¡SALIDA!", "SALIDA", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "➡️", "Cobra 200€ al pasar"),

    # Lado Inferior (1 a 9)
    (1, 1, "Ronda de Valencia", "CALLE", "MARRON", 60, 2, 10, 30, 90, 160, 250, 50, 30, "🏠", "Distrito Marrón"),
    (2, 2, "Caja de Comunidad", "COMUNIDAD", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "📦", "Saca una carta"),
    (3, 3, "Plaza Lavapiés", "CALLE", "MARRON", 60, 4, 20, 60, 180, 320, 450, 50, 30, "🏠", "Distrito Marrón"),
    (4, 4, "Impuesto Capital", "IMPUESTO", None, 0, 200, 0, 0, 0, 0, 0, 0, 0, "💰", "Paga 200€"),
    (5, 5, "Estación de Goya", "ESTACION", None, 200, 25, 50, 100, 200, 0, 0, 0, 100, "🚂", "Ferrocarril"),
    (6, 6, "Glorieta Cuatro Caminos", "CALLE", "CELESTE", 100, 6, 30, 90, 270, 400, 550, 50, 50, "🏠", "Distrito Celeste"),
    (7, 7, "Suerte", "SUERTE", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "❓", "Saca una carta"),
    (8, 8, "Calle Reina Victoria", "CALLE", "CELESTE", 100, 6, 30, 90, 270, 400, 550, 50, 50, "🏠", "Distrito Celeste"),
    (9, 9, "Calle Bravo Murillo", "CALLE", "CELESTE", 120, 8, 40, 100, 300, 450, 600, 50, 60, "🏠", "Distrito Celeste"),

    # Esquina 10
    (10, 10, "EN LA CÁRCEL", "CARCEL", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "⛓️", "Solo de visita"),

    # Lado Izquierdo (11 a 19)
    (11, 11, "Glorieta de Bilbao", "CALLE", "ROSA", 140, 10, 50, 150, 450, 625, 750, 100, 70, "🏠", "Distrito Rosa"),
    (12, 12, "Cía. Electricidad", "SERVICIO", None, 150, 4, 10, 0, 0, 0, 0, 0, 75, "💡", "Servicio Público"),
    (13, 13, "Calle Alberto Aguilera", "CALLE", "ROSA", 140, 10, 50, 150, 450, 625, 750, 100, 70, "🏠", "Distrito Rosa"),
    (14, 14, "Calle Fuencarral", "CALLE", "ROSA", 160, 12, 60, 180, 500, 700, 900, 100, 80, "🏠", "Distrito Rosa"),
    (15, 15, "Estación de Delicias", "ESTACION", None, 200, 25, 50, 100, 200, 0, 0, 0, 100, "🚂", "Ferrocarril"),
    (16, 16, "Avenida Felipe II", "CALLE", "NARANJA", 180, 14, 70, 200, 550, 750, 950, 100, 90, "🏠", "Distrito Naranja"),
    (17, 17, "Caja de Comunidad", "COMUNIDAD", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "📦", "Saca una carta"),
    (18, 18, "Calle Serrano", "CALLE", "NARANJA", 180, 14, 70, 200, 550, 750, 950, 100, 90, "🏠", "Distrito Naranja"),
    (19, 19, "Calle Velázquez", "CALLE", "NARANJA", 200, 16, 80, 220, 600, 800, 1000, 100, 100, "🏠", "Distrito Naranja"),

    # Esquina 20
    (20, 20, "PARKING GRATUITO", "PARKING", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "🚗", "Descanso / Bote"),

    # Lado Superior (21 a 29)
    (21, 21, "Avenida de América", "CALLE", "ROJO", 220, 18, 90, 250, 700, 875, 1050, 150, 110, "🏠", "Distrito Rojo"),
    (22, 22, "Suerte", "SUERTE", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "❓", "Saca una carta"),
    (23, 23, "Calle María de Molina", "CALLE", "ROJO", 220, 18, 90, 250, 700, 875, 1050, 150, 110, "🏠", "Distrito Rojo"),
    (24, 24, "Calle Cea Bermúdez", "CALLE", "ROJO", 240, 20, 100, 300, 750, 925, 1100, 150, 120, "🏠", "Distrito Rojo"),
    (25, 25, "Estación de Mediodía", "ESTACION", None, 200, 25, 50, 100, 200, 0, 0, 0, 100, "🚂", "Ferrocarril"),
    (26, 26, "Av. Reyes Católicos", "CALLE", "AMARILLO", 260, 22, 110, 330, 800, 975, 1150, 150, 130, "🏠", "Distrito Amarillo"),
    (27, 27, "Calle Bailén", "CALLE", "AMARILLO", 260, 22, 110, 330, 800, 975, 1150, 150, 130, "🏠", "Distrito Amarillo"),
    (28, 28, "Compañía de Aguas", "SERVICIO", None, 150, 4, 10, 0, 0, 0, 0, 0, 75, "🚰", "Servicio Público"),
    (29, 29, "Plaza de España", "CALLE", "AMARILLO", 280, 24, 120, 360, 850, 1025, 1200, 150, 140, "🏠", "Distrito Amarillo"),

    # Esquina 30
    (30, 30, "¡VAYA A LA CÁRCEL!", "IR_CARCEL", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "👮‍♂️", "Sin pasar por la Salida"),

    # Lado Derecho (31 a 39)
    (31, 31, "Puerta del Sol", "CALLE", "VERDE", 300, 26, 130, 390, 900, 1100, 1275, 200, 150, "🏠", "Distrito Verde"),
    (32, 32, "Calle Alcalá", "CALLE", "VERDE", 300, 26, 130, 390, 900, 1100, 1275, 200, 150, "🏠", "Distrito Verde"),
    (33, 33, "Caja de Comunidad", "COMUNIDAD", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "📦", "Saca una carta"),
    (34, 34, "Gran Vía", "CALLE", "VERDE", 320, 28, 150, 450, 1000, 1200, 1400, 200, 160, "🏠", "Distrito Verde"),
    (35, 35, "Estación del Norte", "ESTACION", None, 200, 25, 50, 100, 200, 0, 0, 0, 100, "🚂", "Ferrocarril"),
    (36, 36, "Suerte", "SUERTE", None, 0, 0, 0, 0, 0, 0, 0, 0, 0, "❓", "Saca una carta"),
    (37, 37, "Paseo de la Castellana", "CALLE", "AZUL", 350, 35, 175, 500, 1100, 1300, 1500, 200, 175, "🏠", "Distrito Azul Oscuro"),
    (38, 38, "Tasa de Lujo", "IMPUESTO", None, 0, 100, 0, 0, 0, 0, 0, 0, 0, "💍", "Paga 100€"),
    (39, 39, "Paseo del Prado", "CALLE", "AZUL", 400, 50, 200, 600, 1400, 1700, 2000, 200, 200, "🏠", "Distrito Azul Oscuro")
]

# 16 Cartas de Suerte tradicionales en español
CARTAS_SUERTE = [
    (1, "Avanza hasta la Salida", "AVANZAR", 0, "Cobra 200€ al instante."),
    (2, "Ve a la Cárcel", "CARCEL", 10, "Ve directamente a la cárcel sin pasar por la Salida."),
    (3, "Avanza hasta Gran Vía", "AVANZAR", 34, "Si pasas por la salida cobra 200€."),
    (4, "Avanza hasta la Estación más cercana", "ESTACION", 0, "Paga el doble al propietario."),
    (5, "El Banco te paga un dividendo de 50€", "COBRAR", 50, "Cobro de dividendos por inversiones."),
    (6, "Multa por exceso de velocidad: paga 15€", "PAGAR", 15, "Multa de tráfico en la ciudad."),
    (7, "Avanza hasta Paseo del Prado", "AVANZAR", 39, "La propiedad más exclusiva de la ciudad."),
    (8, "Has ganado el concurso de crucigramas: cobra 100€", "COBRAR", 100, "Premio de pasatiempos."),
    (9, "Reparaciones en tus propiedades", "REPARAR", 25, "Paga 25€ por cada casa y 100€ por hotel."),
    (10, "Tu préstamo inmobiliario madura: cobra 150€", "COBRAR", 150, "Vencimiento bancario."),
    (11, "Retrocede 3 casillas", "RETROCEDER", 3, "Retrocede 3 casillas inmediatamente."),
    (12, "Quedas libre de la cárcel", "LIBERTAD", 0, "Conserva esta carta hasta que la necesites."),
    (13, "Paga por gastos de escolaridad: 150€", "PAGAR", 150, "Matrícula escolar anual."),
    (14, "Avanza hasta la Glorieta de Bilbao", "AVANZAR", 11, "Si pasas por la salida cobra 200€."),
    (15, "Has sido elegido presidente del club: paga 50€ a cada jugador", "PAGAR_TODOS", 50, "Celebración de nombramiento."),
    (16, "Avanza hasta la Cía. de Electricidad", "AVANZAR", 12, "Si no tiene dueño puedes comprarla.")
]

# 16 Cartas de Caja de Comunidad tradicionales en español
CARTAS_COMUNIDAD = [
    (1, "Avanza hasta la Salida", "AVANZAR", 0, "Cobra 200€ inmediatamente."),
    (2, "Error de la banca a tu favor: cobra 200€", "COBRAR", 200, "Reclamación bancaria aprobada."),
    (3, "Gastos del médico: paga 50€", "PAGAR", 50, "Factura médica urgente."),
    (4, "Venta de acciones en bolsa: cobra 50€", "COBRAR", 50, "Beneficio por venta bursátil."),
    (5, "Quedas libre de la cárcel", "LIBERTAD", 0, "Carta oficial de indulto."),
    (6, "Ve a la Cárcel", "CARCEL", 10, "Directamente a prisión sin cobrar salario."),
    (7, "Hacienda te devuelve 20€", "COBRAR", 20, "Devolución de la declaración de la renta."),
    (8, "Es tu cumpleaños: cobra 10€ de cada jugador", "COBRAR_TODOS", 10, "Regalos de cumpleaños."),
    (9, "Póliza de seguro de vida vence: cobra 100€", "COBRAR", 100, "Cobro de seguro."),
    (10, "Factura del hospital: paga 100€", "PAGAR", 100, "Tratamiento y hospitalización."),
    (11, "Paga las tasas escolares: 50€", "PAGAR", 50, "Material y matrícula escolar."),
    (12, "Recibes 25€ por servicios de asesoría", "COBRAR", 25, "Honorarios profesionales."),
    (13, "Reparaciones de la comunidad", "REPARAR", 40, "Paga 40€ por casa y 115€ por hotel."),
    (14, "Segundo premio en certamen de belleza: cobra 10€", "COBRAR", 10, "Premio de la asociación vecinal."),
    (15, "Heredas una fortuna de 100€", "COBRAR", 100, "Herencia familiar."),
    (16, "Reembolso del fondo de pensiones: cobra 100€", "COBRAR", 100, "Rescate de aportaciones.")
]

# Reglas económicas modificables
REGLAS_INICIALES = [
    ("dinero_inicial", "1500", "Capital con el que inicia cada jugador al empezar la partida"),
    ("salario_salida", "200", "Cantidad cobrada al dar una vuelta completa o caer en la Salida"),
    ("fianza_carcel", "50", "Coste para salir inmediatamente de prisión"),
    ("turnos_max_carcel", "3", "Número máximo de turnos que se puede permanecer encerrado"),
    ("interes_hipoteca", "10", "Porcentaje de recargo para levantar una hipoteca"),
    ("max_casas_por_calle", "4", "Casas máximas antes de poder construir un hotel"),
    ("acumular_bote_parque", "true", "Si los impuestos y multas van al bote del Parking Gratuito")
]


def inicializar_base_datos(ruta_db):
    """
    Crea las tablas SQLite e inserta los datos iniciales si la base de datos
    no existe todavía.
    """
    os.makedirs(os.path.dirname(os.path.abspath(ruta_db)), exist_ok=True)
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Tabla 1: Casillas del tablero
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS casillas (
            id INTEGER PRIMARY KEY,
            posicion INTEGER UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            grupo TEXT,
            precio_compra INTEGER DEFAULT 0,
            alquiler_base INTEGER DEFAULT 0,
            alquiler_1_casa INTEGER DEFAULT 0,
            alquiler_2_casas INTEGER DEFAULT 0,
            alquiler_3_casas INTEGER DEFAULT 0,
            alquiler_4_casas INTEGER DEFAULT 0,
            alquiler_hotel INTEGER DEFAULT 0,
            coste_casa INTEGER DEFAULT 0,
            hipoteca INTEGER DEFAULT 0,
            icono TEXT DEFAULT '🏠',
            descripcion TEXT
        )
    """)

    # Tabla 2: Cartas de Suerte
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartas_suerte (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            tipo_accion TEXT NOT NULL,
            valor INTEGER DEFAULT 0,
            descripcion TEXT
        )
    """)

    # Tabla 3: Cartas de Caja de Comunidad
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartas_comunidad (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            tipo_accion TEXT NOT NULL,
            valor INTEGER DEFAULT 0,
            descripcion TEXT
        )
    """)

    # Tabla 4: Configuración y reglas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reglas_partida (
            clave TEXT PRIMARY KEY,
            valor TEXT NOT NULL,
            descripcion TEXT
        )
    """)

    # Verificar si ya tiene datos
    cursor.execute("SELECT COUNT(*) FROM casillas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO casillas (
                id, posicion, nombre, tipo, grupo, precio_compra, alquiler_base,
                alquiler_1_casa, alquiler_2_casas, alquiler_3_casas, alquiler_4_casas,
                alquiler_hotel, coste_casa, hipoteca, icono, descripcion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, CASILLAS_INICIALES)

        cursor.executemany("""
            INSERT INTO cartas_suerte (id, titulo, tipo_accion, valor, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, CARTAS_SUERTE)

        cursor.executemany("""
            INSERT INTO cartas_comunidad (id, titulo, tipo_accion, valor, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, CARTAS_COMUNIDAD)

        cursor.executemany("""
            INSERT INTO reglas_partida (clave, valor, descripcion)
            VALUES (?, ?, ?)
        """, REGLAS_INICIALES)

        conn.commit()
        print(f"✓ Base de datos SQLite creada e inicializada en: {ruta_db}")
    else:
        print(f"ℹ Conectado a la base de datos existente: {ruta_db}")

    conn.close()


def cargar_casillas_desde_db(ruta_db):
    """
    Lee todas las casillas desde el archivo .db para renderizar el tablero
    con los precios, nombres y alquileres actualizados.
    """
    conn = sqlite3.connect(ruta_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM casillas ORDER BY posicion ASC")
    filas = cursor.fetchall()
    casillas = [dict(fila) for fila in filas]
    conn.close()
    return casillas


def exportar_a_json(ruta_db, ruta_json):
    """
    Exporta una copia de la base de datos en JSON para que el usuario pueda
    abrirla, verla o editarla fácilmente desde su teléfono.
    """
    conn = sqlite3.connect(ruta_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM casillas ORDER BY posicion ASC")
    casillas = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM cartas_suerte")
    suerte = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM cartas_comunidad")
    comunidad = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT * FROM reglas_partida")
    reglas = {row["clave"]: row["valor"] for row in cursor.fetchall()}

    datos_completos = {
        "edicion": "España Oficial",
        "descripcion": "Datos modificables del tablero y las partidas",
        "reglas": reglas,
        "casillas": casillas,
        "cartas_suerte": suerte,
        "cartas_comunidad": comunidad
    }

    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos_completos, f, indent=2, ensure_ascii=False)

    conn.close()
    print(f"✓ Copia legible exportada a JSON: {ruta_json}")


if __name__ == "__main__":
    ruta_salida_db = os.path.join(os.path.dirname(__file__), "..", "output", "tablero_datos.db")
    ruta_salida_json = os.path.join(os.path.dirname(__file__), "..", "output", "tablero_datos.json")
    inicializar_base_datos(ruta_salida_db)
    exportar_a_json(ruta_salida_db, ruta_salida_json)
