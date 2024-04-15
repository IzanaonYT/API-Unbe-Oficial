import os
import json
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter


router = APIRouter()
DATA_FOLDER = "UnbelievaBoat-BDFD/Economy"
@router.get("/api/get_start/{server_id}/")
async def init_server(server_id: str):
    folder_path = f"{DATA_FOLDER}/{server_id}"

    if os.path.exists(folder_path):
        raise HTTPException(status_code=400, detail="El servidor ya está inicializado.")

    os.makedirs(folder_path)
    data = {
        "items": [],
        "min-max-payout": [{
            "minwork": 0,
            "maxwork": 20,
            "mincrime": 0,
            "maxcrime": 20,
            "minslut": 0,
            "maxslut": 20
        }],
        "min-max-fail": [{
            "mincrime": 0,
            "maxcrime": 20,
            "minslut": 0,
            "maxslut": 20
        }],
        "replys-win": [{
            "work": [],
            "crime": [],
            "slut": []
        }],
        "replys-fail": [{
            "crime": [],
            "slut": []
        }],
        "reply-count": 0,
        "users": [],
        "coin": ":pizza:"
    }

    with open(f"{folder_path}/data.json", "w") as file:
        json.dump(data, file, indent=4)

    return JSONResponse(content={"message": f"El servidor {server_id}, esta inicializado."}, status_code=200)