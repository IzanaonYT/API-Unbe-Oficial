import os
import sqlite3
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import json

router = APIRouter()
BASE_FOLDER = "BASE"

# Función para inicializar la base de datos
def init_db():
    db_path = os.path.join(BASE_FOLDER, "datos.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS servers (
                        server_id TEXT PRIMARY KEY,
                        items TEXT,
                        min_max_payout TEXT,
                        min_max_fail TEXT,
                        replys_win TEXT,
                        replys_fail TEXT,
                        reply_count INTEGER,
                        users TEXT,
                        coin TEXT
                    )''')
    conn.commit()
    conn.close()

@router.get("/api/get_start/{server_id}/")
async def init_server(server_id: str):
    init_db()  # Inicializar la base de datos si no existe

    db_path = os.path.join(BASE_FOLDER, "datos.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si el servidor ya está inicializado
    cursor.execute("SELECT * FROM servers WHERE server_id=?", (server_id,))
    existing_server = cursor.fetchone()
    if existing_server:
        conn.close()
        raise HTTPException(status_code=400, detail="El servidor ya está inicializado.")

    # Insertar datos del servidor en la base de datos
    data = {
        "items": [],
        "min_max_payout": '[{"minwork": 0, "maxwork": 20, "mincrime": 0, "maxcrime": 20, "minslut": 0, "maxslut": 20}]',
        "min_max_fail": '[{"mincrime": 0, "maxcrime": 20, "minslut": 0, "maxslut": 20}]',
        "replys_win": '[{"work": [], "crime": [], "slut": []}]',
        "replys_fail": '[{"crime": [], "slut": []}]',
        "reply_count": 0,
        "users": [],
        "coin": ":pizza:"
    }

    cursor.execute('''INSERT INTO servers (server_id, items, min_max_payout, min_max_fail, replys_win, replys_fail, reply_count, users, coin)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (server_id, json.dumps(data['items']), data['min_max_payout'], data['min_max_fail'], data['replys_win'],
                    data['replys_fail'], data['reply_count'], json.dumps(data['users']), data['coin']))
    conn.commit()
    conn.close()

    return JSONResponse(content={"message": f"El servidor {server_id} ha sido inicializado."}, status_code=200)
