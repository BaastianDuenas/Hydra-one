from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Repuesto(Base):
    __tablename__ = "repuestos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    categoria: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    stock_actual: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    stock_minimo: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    unidad_medida: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )