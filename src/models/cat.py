from decimal import Decimal

from sqlalchemy.orm import mapped_column, Mapped

from ..database import Base


class Cat(Base):
    __tablename__: str = "cats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    years_of_experience: Mapped[int] = mapped_column()
    breed: Mapped[str] = mapped_column()
    salary: Mapped[Decimal] = mapped_column()
