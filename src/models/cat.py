from typing import Annotated

from sqlalchemy.orm import mapped_column, Mapped

from ..database import Base


class Cat(Base):
    __tablename__ = "cats"

    id: Annotated[int, mapped_column(primary_key=True)]
    name: str
    years_of_experience: int
    breed: str
    salary: float
