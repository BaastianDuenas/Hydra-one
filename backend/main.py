import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.activos import router as activos_router
from app.routers.mantenciones import router as mantenciones_router
from app.routers.repuestos import router as repuestos_router
from app.routers.alertas import router as alertas_router


load_dotenv()


app = FastAPI(
    title="Hydra One API",
    version="0.1.0"
)


cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173"
)

allowed_origins = [
    origin.strip()
    for origin in cors_origins.split(",")
    if origin.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(activos_router)
app.include_router(mantenciones_router)
app.include_router(repuestos_router)
app.include_router(alertas_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Hydra One API funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }