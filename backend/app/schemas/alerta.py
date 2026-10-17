from pydantic import BaseModel


class AlertaResponse(BaseModel):
    id: str
    tipo: str
    prioridad: str
    titulo: str
    descripcion: str
    origen_id: int