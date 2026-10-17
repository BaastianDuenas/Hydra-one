from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.repuesto import Repuesto
from app.schemas.repuesto import (
    RepuestoCreate,
    RepuestoResponse,
    RepuestoUpdate,
)


router = APIRouter(
    prefix="/api/repuestos",
    tags=["Repuestos"]
)


@router.get("/", response_model=list[RepuestoResponse])
def listar_repuestos(db: Session = Depends(get_db)):
    return (
        db.query(Repuesto)
        .order_by(Repuesto.nombre)
        .all()
    )


@router.post(
    "/",
    response_model=RepuestoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_repuesto(
    datos: RepuestoCreate,
    db: Session = Depends(get_db)
):
    codigo_existente = (
        db.query(Repuesto)
        .filter(Repuesto.codigo == datos.codigo)
        .first()
    )

    if codigo_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un repuesto con ese código"
        )

    nuevo_repuesto = Repuesto(
        codigo=datos.codigo,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        categoria=datos.categoria,
        stock_actual=datos.stock_actual,
        stock_minimo=datos.stock_minimo,
        unidad_medida=datos.unidad_medida,
        ubicacion=datos.ubicacion,
    )

    db.add(nuevo_repuesto)
    db.commit()
    db.refresh(nuevo_repuesto)

    return nuevo_repuesto


@router.put("/{repuesto_id}", response_model=RepuestoResponse)
def actualizar_repuesto(
    repuesto_id: int,
    datos: RepuestoUpdate,
    db: Session = Depends(get_db)
):
    repuesto = (
        db.query(Repuesto)
        .filter(Repuesto.id == repuesto_id)
        .first()
    )

    if not repuesto:
        raise HTTPException(
            status_code=404,
            detail="Repuesto no encontrado"
        )

    codigo_existente = (
        db.query(Repuesto)
        .filter(
            Repuesto.codigo == datos.codigo,
            Repuesto.id != repuesto_id
        )
        .first()
    )

    if codigo_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe otro repuesto con ese código"
        )

    repuesto.codigo = datos.codigo
    repuesto.nombre = datos.nombre
    repuesto.descripcion = datos.descripcion
    repuesto.categoria = datos.categoria
    repuesto.stock_actual = datos.stock_actual
    repuesto.stock_minimo = datos.stock_minimo
    repuesto.unidad_medida = datos.unidad_medida
    repuesto.ubicacion = datos.ubicacion

    db.commit()
    db.refresh(repuesto)

    return repuesto


@router.delete("/{repuesto_id}")
def eliminar_repuesto(
    repuesto_id: int,
    db: Session = Depends(get_db)
):
    repuesto = (
        db.query(Repuesto)
        .filter(Repuesto.id == repuesto_id)
        .first()
    )

    if not repuesto:
        raise HTTPException(
            status_code=404,
            detail="Repuesto no encontrado"
        )

    db.delete(repuesto)
    db.commit()

    return {
        "mensaje": "Repuesto eliminado correctamente"
    }