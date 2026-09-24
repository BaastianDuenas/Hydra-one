from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

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

    horometro: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    kilometraje: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )