import os
import importlib.util
from fastapi import FastAPI, APIRouter

app = FastAPI()
@app.get("/")
def on_route():
    return {"status": 200}


def registrar_rutas_desde_directorio(router, directorio):
    for nombre_archivo in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, nombre_archivo)
        if os.path.isdir(ruta_completa):
            registrar_rutas_desde_directorio(router, ruta_completa)
        elif nombre_archivo.endswith('.py') and nombre_archivo != '__init__.py':
            nombre_modulo = nombre_archivo[:-3]  # Elimina la extensión .py
            spec = importlib.util.spec_from_file_location(f"API.{nombre_modulo}", ruta_completa)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            if hasattr(modulo, 'router'):
                router.include_router(modulo.router)

carpeta_api = os.path.join(os.path.dirname(__file__), 'API')
router_principal = APIRouter()

registrar_rutas_desde_directorio(router_principal, carpeta_api)
app.include_router(router_principal)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1000)