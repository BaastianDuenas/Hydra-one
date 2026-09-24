from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.activo import Activo
from app.schemas.activo import ActivoCreate, ActivoResponse


router = APIRouter(
    prefix="/api/activos",
    tags=["Activos"]
)


@router.get("/", response_model=list[ActivoResponse])
def listar_activos(db: Session = Depends(get_db)):
    activos = db.query(Activo).order_by(Activo.id).all()

    return activos


@router.post(
    "/",
    response_model=ActivoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_activo(
    activo: ActivoCreate,
    db: Session = Depends(get_db)
):
    activo_existente = (
        db.query(Activo)
        .filter(Activo.codigo == activo.codigo)
        .first()
    )

    if activo_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un activo con ese código"
        )

    nuevo_activo = Activo(
        codigo=activo.codigo,
        nombre=activo.nombre,
        tipo=activo.tipo,
        estado=activo.estado,
        horometro=activo.horometro,
        kilometraje=activo.kilometraje
    )

    db.add(nuevo_activo)
    db.commit()
    db.refresh(nuevo_activo)

    return nuevo_activo