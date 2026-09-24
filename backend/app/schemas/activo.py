from pydantic import BaseModel, ConfigDict


class ActivoBase(BaseModel):
    codigo: str
    nombre: str
    tipo: str
    estado: str
    horometro: int = 0
    kilometraje: int = 0


class ActivoCreate(ActivoBase):
    pass


class ActivoResponse(ActivoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)