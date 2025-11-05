from typing import Annotated
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from ..utils import check_breed


class CatBase(BaseModel):
    name: str
    years_of_experience: Annotated[int, Field(ge=0)]
    breed: str
    salary: Annotated[Decimal, Field(ge=0, decimal_places=2)]


class CatCreate(CatBase):
    @field_validator("breed", mode="after")
    @classmethod
    def validate_breed(cls, value: str) -> str:
        check_breed(value)
        return value


class CatDetail(CatBase):
    id: int
