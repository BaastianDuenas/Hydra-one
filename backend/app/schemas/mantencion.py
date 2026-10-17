from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MantencionBase(BaseModel):
    activo_id: int
    tipo: str = Field(min_length=2, max_length=50)
    descripcion: str = Field(min_length=2, max_length=500)
    fecha: date
    horometro: int = Field(default=0, ge=0)
    estado: str = Field(min_length=2, max_length=50)


class MantencionCreate(MantencionBase):
    pass


class MantencionUpdate(MantencionBase):
    pass


class MantencionResponse(MantencionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)