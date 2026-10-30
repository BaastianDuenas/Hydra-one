
from decimal import Decimal

from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Activo(Base):
    __tablename__ = "activos"

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

    tipo: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    horometro: Mapped[Decimal] = mapped_column(
        Numeric(14, 4),
        default=0,
        nullable=False
    )

    kilometraje: Mapped[Decimal] = mapped_column(
        Numeric(14, 4),
        default=0,
        nullable=False
    )

    mantenciones = relationship(
        "Mantencion",
        back_populates="activo",
        cascade="all, delete-orphan"
    )
