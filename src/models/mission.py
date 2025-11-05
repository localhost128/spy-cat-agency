from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Mission(Base):
    __tablename__: str = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int | None] = mapped_column(ForeignKey("cats.id"), default=None)
    is_complete: Mapped[bool] = mapped_column(default=False)

    cat: Mapped[Cat | None] = relationship(back_populates="missions")
    targets: Mapped[list["Target"]] = relationship(
        back_populates="mission", cascade="all, delete-orphan"
    )


class Target(Base):
    __tablename__: str = "targets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    notes: Mapped[str] = mapped_column()
    is_complete: Mapped[bool] = mapped_column(default=False)
    mission_id: Mapped[int] = mapped_column(ForeignKey("missions.id"))

    mission: Mapped[Mission] = relationship(back_populates="targets")
