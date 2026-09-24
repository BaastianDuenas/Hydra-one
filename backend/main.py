from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.activos import router as activos_router


app = FastAPI(
    title="Hydra One API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(activos_router)


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