#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import requests
import argparse
import sys
import os
import glob
from typing import Optional, Tuple

# ----- Configuración de la API -----
API_BASE_URL   = 'https://collar-link-production.up.railway.app'
UPDATE_ENDPOINT = '/api/v1/collar/updateLocation'

# ----- Funciones de acceso a datos -----

def connect_db(path: str) -> sqlite3.Connection:
    """Abre la conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo conectar a la BD en '{path}': {e}")
        sys.exit(1)

def fetch_devices(conn: sqlite3.Connection) -> list[Tuple[str, str]]:
    cur = conn.cursor()
    cur.execute("SELECT device_id, api_key FROM devices")
    return cur.fetchall()

def fetch_latest_location(conn: sqlite3.Connection, device_id: str) -> Optional[Tuple[float, float]]:
    cur = conn.cursor()
    cur.execute("""
        SELECT latitude, longitude
          FROM location_records
         WHERE device_id = ?
      ORDER BY created_at DESC
         LIMIT 1
    """, (device_id,))
    row = cur.fetchone()
    return (row['latitude'], row['longitude']) if row else None

def upload_location(device_id: str, api_key: str, latitude: float, longitude: float) -> None:
    url = f"{API_BASE_URL}{UPDATE_ENDPOINT}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "serialNumber": device_id,
        "lastLatitude": latitude,
        "lastLongitude": longitude
    }
    try:
        resp = requests.put(url, headers=headers, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"[ERROR] Falló request para {device_id}: {e}")
        return

    if resp.ok:
        print(f"[OK] Dispositivo {device_id} → ({latitude}, {longitude})")
    else:
        print(f"[FAIL] Dispositivo {device_id}: {resp.status_code} {resp.text}")

# ----- Main -----

def main():
    # Determina carpeta del script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(
        description="Sube al backend la última ubicación de cada dispositivo."
    )
    parser.add_argument(
        "db_path",
        nargs="?",
        default=None,
        help="(Opcional) Ruta al archivo .sqlite o .db. " +
             "Si no se indica, busca en el mismo directorio del script."
    )
    args = parser.parse_args()

    # Si no pasaron db_path, buscamos un .sqlite/.db en la carpeta
    if args.db_path is None:
        candidates = glob.glob(os.path.join(script_dir, "*.sqlite")) + \
                     glob.glob(os.path.join(script_dir, "*.db"))
        if not candidates:
            print(f"[ERROR] No encontré ningún .sqlite/.db en {script_dir}.")
            sys.exit(1)
        if len(candidates) > 1:
            print("[WARNING] Encontré varios archivos de BD, usaré el primero:")
            for c in candidates:
                print("   -", os.path.basename(c))
        args.db_path = candidates[0]

    print(f"Usando base de datos: {args.db_path}")
    conn = connect_db(args.db_path)
    devices = fetch_devices(conn)

    if not devices:
        print("No se encontraron dispositivos en la tabla `devices`.")
        return

    for device in devices:
        device_id = device["device_id"]
        api_key   = device["api_key"]

        loc = fetch_latest_location(conn, device_id)
        if loc:
            latitude, longitude = loc
            upload_location(device_id, api_key, latitude, longitude)
        else:
            print(f"[SKIP] Sin registros de ubicación para {device_id}")

if __name__ == "__main__":
    main()
