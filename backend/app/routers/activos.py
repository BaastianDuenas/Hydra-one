from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.mantencion import Mantencion
from app.models.repuesto import Repuesto

from app.database.connection import get_db
from app.models.activo import Activo
from app.schemas.activo import (
    ActivoCreate,
    ActivoResponse,
    ActivoUpdate,
)


router = APIRouter(
    prefix="/api/activos",
    tags=["Activos"]
)


@router.get("/", response_model=list[ActivoResponse])
def listar_activos(db: Session = Depends(get_db)):
    activos = db.query(Activo).order_by(Activo.id).all()

    return activos


@router.get("/{activo_id}", response_model=ActivoResponse)
def obtener_activo(
    activo_id: int,
    db: Session = Depends(get_db)
):
    activo = db.query(Activo).filter(Activo.id == activo_id).first()

    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    return activo


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

@router.put("/{activo_id}", response_model=ActivoResponse)
def actualizar_activo(
    activo_id: int,
    datos: ActivoUpdate,
    db: Session = Depends(get_db)
):
    activo = (
        db.query(Activo)
        .filter(Activo.id == activo_id)
        .first()
    )

    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    codigo_normalizado = datos.codigo.strip().upper()

    codigo_existente = (
        db.query(Activo)
        .filter(
            Activo.codigo == codigo_normalizado,
            Activo.id != activo_id
        )
        .first()
    )

    if codigo_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe otro activo con ese código"
        )

    activo.codigo = codigo_normalizado
    activo.nombre = datos.nombre.strip()
    activo.tipo = datos.tipo.strip()
    activo.estado = datos.estado
    activo.horometro = datos.horometro
    activo.kilometraje = datos.kilometraje

    try:
        db.commit()
        db.refresh(activo)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="El código del activo ya está registrado"
        )

    return activo

@router.delete("/{activo_id}")
def eliminar_activo(
    activo_id: int,
    db: Session = Depends(get_db)
):
    activo = db.query(Activo).filter(Activo.id == activo_id).first()

    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    db.delete(activo)
    db.commit()

    return {
        "mensaje": "Activo eliminado correctamente"
    }