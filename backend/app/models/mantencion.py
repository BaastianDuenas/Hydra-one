from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Mantencion(Base):
    __tablename__ = "mantenciones"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    activo_id: Mapped[int] = mapped_column(
        ForeignKey("activos.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    horometro: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    activo = relationship(
        "Activo",
        back_populates="mantenciones"
    )