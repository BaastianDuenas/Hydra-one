from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.activo import Activo
from app.models.mantencion import Mantencion
from app.schemas.mantencion import (
    MantencionCreate,
    MantencionResponse,
    MantencionUpdate,
)


router = APIRouter(
    prefix="/api/mantenciones",
    tags=["Mantenciones"]
)


@router.get("/", response_model=list[MantencionResponse])
def listar_mantenciones(db: Session = Depends(get_db)):
    return (
        db.query(Mantencion)
        .order_by(Mantencion.fecha.desc())
        .all()
    )


@router.post(
    "/",
    response_model=MantencionResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_mantencion(
    datos: MantencionCreate,
    db: Session = Depends(get_db)
):
    activo = (
        db.query(Activo)
        .filter(Activo.id == datos.activo_id)
        .first()
    )

    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    nueva_mantencion = Mantencion(
        activo_id=datos.activo_id,
        tipo=datos.tipo,
        descripcion=datos.descripcion,
        fecha=datos.fecha,
        horometro=datos.horometro,
        estado=datos.estado,
    )

    db.add(nueva_mantencion)
    db.commit()
    db.refresh(nueva_mantencion)

    return nueva_mantencion

@router.get(
    "/activo/{activo_id}",
    response_model=list[MantencionResponse]
)
def listar_mantenciones_por_activo(
    activo_id: int,
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

    return (
        db.query(Mantencion)
        .filter(Mantencion.activo_id == activo_id)
        .order_by(Mantencion.fecha.desc())
        .all()
    )

@router.put("/{mantencion_id}", response_model=MantencionResponse)
def actualizar_mantencion(
    mantencion_id: int,
    datos: MantencionUpdate,
    db: Session = Depends(get_db)
):
    mantencion = (
        db.query(Mantencion)
        .filter(Mantencion.id == mantencion_id)
        .first()
    )

    if not mantencion:
        raise HTTPException(
            status_code=404,
            detail="Mantención no encontrada"
        )

    activo = (
        db.query(Activo)
        .filter(Activo.id == datos.activo_id)
        .first()
    )

    if not activo:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    mantencion.activo_id = datos.activo_id
    mantencion.tipo = datos.tipo
    mantencion.descripcion = datos.descripcion
    mantencion.fecha = datos.fecha
    mantencion.horometro = datos.horometro
    mantencion.estado = datos.estado

    db.commit()
    db.refresh(mantencion)

    return mantencion


@router.delete("/{mantencion_id}")
def eliminar_mantencion(
    mantencion_id: int,
    db: Session = Depends(get_db)
):
    mantencion = (
        db.query(Mantencion)
        .filter(Mantencion.id == mantencion_id)
        .first()
    )

    if not mantencion:
        raise HTTPException(
            status_code=404,
            detail="Mantención no encontrada"
        )

    db.delete(mantencion)
    db.commit()

    return {
        "mensaje": "Mantención eliminada correctamente"
    }