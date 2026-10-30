from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ActivoBase(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    nombre: str = Field(min_length=2, max_length=150)
    tipo: str = Field(min_length=2, max_length=100)
    estado: str = Field(min_length=2, max_length=50)
    horometro: Decimal = Field(default=Decimal("0"), ge=0)
    kilometraje: Decimal = Field(default=Decimal("0"), ge=0)


class ActivoCreate(ActivoBase):
    pass


class ActivoUpdate(ActivoBase):
    pass


class ActivoResponse(ActivoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)