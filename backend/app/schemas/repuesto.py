from pydantic import BaseModel, ConfigDict, Field


class RepuestoBase(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: str = Field(min_length=2, max_length=500)
    categoria: str = Field(min_length=2, max_length=100)

    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)

    unidad_medida: str = Field(min_length=1, max_length=50)
    ubicacion: str = Field(min_length=1, max_length=150)


class RepuestoCreate(RepuestoBase):
    pass


class RepuestoUpdate(RepuestoBase):
    pass


class RepuestoResponse(RepuestoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)