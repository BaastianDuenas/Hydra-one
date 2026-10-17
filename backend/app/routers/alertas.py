from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.activo import Activo
from app.models.mantencion import Mantencion
from app.models.repuesto import Repuesto
from app.schemas.alerta import AlertaResponse


router = APIRouter(
    prefix="/api/alertas",
    tags=["Alertas"]
)


@router.get("/", response_model=list[AlertaResponse])
def listar_alertas(db: Session = Depends(get_db)):
    alertas = []

    # -------------------------
    # ALERTAS DE INVENTARIO
    # -------------------------

    repuestos = db.query(Repuesto).all()

    for repuesto in repuestos:
        if repuesto.stock_actual <= repuesto.stock_minimo:

            if repuesto.stock_actual == 0:
                prioridad = "Critica"
                titulo = "Repuesto sin stock"
            else:
                prioridad = "Alta"
                titulo = "Stock bajo"

            alertas.append({
                "id": f"stock-{repuesto.id}",
                "tipo": "Inventario",
                "prioridad": prioridad,
                "titulo": titulo,
                "descripcion": (
                    f"{repuesto.nombre}: "
                    f"{repuesto.stock_actual} disponibles "
                    f"(mínimo {repuesto.stock_minimo})"
                ),
                "origen_id": repuesto.id,
            })

    # -------------------------
    # ALERTAS DE MANTENCIONES
    # -------------------------

    hoy = date.today()
    proximos_dias = hoy + timedelta(days=7)

    mantenciones = (
        db.query(Mantencion, Activo)
        .join(Activo, Mantencion.activo_id == Activo.id)
        .filter(Mantencion.estado == "Programada")
        .all()
    )

    for mantencion, activo in mantenciones:

        if mantencion.fecha < hoy:
            alertas.append({
                "id": f"mantencion-{mantencion.id}",
                "tipo": "Mantencion",
                "prioridad": "Critica",
                "titulo": "Mantención vencida",
                "descripcion": (
                    f"{activo.codigo} - {activo.nombre}: "
                    f"mantención programada para "
                    f"{mantencion.fecha}"
                ),
                "origen_id": mantencion.id,
            })

        elif mantencion.fecha <= proximos_dias:
            alertas.append({
                "id": f"mantencion-{mantencion.id}",
                "tipo": "Mantencion",
                "prioridad": "Media",
                "titulo": "Mantención próxima",
                "descripcion": (
                    f"{activo.codigo} - {activo.nombre}: "
                    f"mantención programada para "
                    f"{mantencion.fecha}"
                ),
                "origen_id": mantencion.id,
            })

    return alertas