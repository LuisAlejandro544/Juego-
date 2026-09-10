#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
HERRAMIENTA PARA MODIFICAR LA BASE DE DATOS (PRECIOS, ALQUILERES Y REGLAS)
=============================================================================
Permite modificar los valores de la base de datos 'output/tablero_datos.db':
1. Cambiar precio o alquiler de cualquier casilla por su ID o nombre.
2. Sincronizar cambios desde 'output/tablero_datos.json' hacia el archivo .db.
3. Listar todas las casillas y sus valores actuales.
"""

import sys
import os
import sqlite3
import json

RUTA_DB = os.path.join(os.path.dirname(__file__), "..", "output", "tablero_datos.db")
RUTA_JSON = os.path.join(os.path.dirname(__file__), "..", "output", "tablero_datos.json")


def sincronizar_desde_json():
    """
    Lee 'output/tablero_datos.json' y actualiza la base de datos .db con los
    cambios que el usuario haya hecho en el archivo JSON desde su teléfono.
    """
    if not os.path.exists(RUTA_JSON):
        print(f"Error: No se encontró {RUTA_JSON}")
        return

    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        datos = json.load(f)

    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    for c in datos.get("casillas", []):
        cursor.execute("""
            UPDATE casillas SET
                nombre = ?,
                precio_compra = ?,
                alquiler_base = ?,
                alquiler_1_casa = ?,
                alquiler_2_casas = ?,
                alquiler_3_casas = ?,
                alquiler_4_casas = ?,
                alquiler_hotel = ?,
                coste_casa = ?,
                hipoteca = ?
            WHERE id = ?
        """, (
            c.get("nombre"),
            c.get("precio_compra", 0),
            c.get("alquiler_base", 0),
            c.get("alquiler_1_casa", 0),
            c.get("alquiler_2_casas", 0),
            c.get("alquiler_3_casas", 0),
            c.get("alquiler_4_casas", 0),
            c.get("alquiler_hotel", 0),
            c.get("coste_casa", 0),
            c.get("hipoteca", 0),
            c.get("id")
        ))

    conn.commit()
    conn.close()
    print("✓ Base de datos .db actualizada con los cambios de tablero_datos.json")


def modificar_precio_casilla(id_o_nombre, nuevo_precio):
    """
    Modifica el precio de compra de una casilla específica en la base de datos.
    """
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    try:
        cid = int(id_o_nombre)
        cursor.execute("UPDATE casillas SET precio_compra = ? WHERE id = ?", (nuevo_precio, cid))
    except ValueError:
        cursor.execute("UPDATE casillas SET precio_compra = ? WHERE nombre LIKE ?", (nuevo_precio, f"%{id_o_nombre}%"))

    filas = cursor.rowcount
    conn.commit()
    conn.close()

    if filas > 0:
        print(f"✓ Precio actualizado a {nuevo_precio}€ para la casilla '{id_o_nombre}'.")
    else:
        print(f"No se encontró ninguna casilla que coincida con '{id_o_nombre}'.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--importar-json":
        sincronizar_desde_json()
    elif len(sys.argv) >= 3:
        modificar_precio_casilla(sys.argv[1], int(sys.argv[2]))
    else:
        print("Uso:")
        print("  python scripts/modificar_db.py --importar-json")
        print("  python scripts/modificar_db.py <id_o_nombre> <nuevo_precio>")
