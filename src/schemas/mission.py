from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from ..utils import chek_cat


class MissionBase(BaseModel):
    cat_id: int | None


class MissionCreate(MissionBase):
    targets: Annotated[list[TargetrCreate], Field(min_length=1, max_length=3)]

    @field_validator("cat_id", mode="after")
    @classmethod
    def validate_cat(cls, cat_id: int | None) -> int | None:
        if cat_id:
            chek_cat(cat_id)
        return cat_id


class MissionDetail(MissionBase):
    is_complete: bool
    targets: list[TarhetsDetail]


class TargetBase(BaseModel):
    name: str
    country: str
    notes: str
    mission_id: int


class TargetrCreate(TargetBase):
    pass


class TarhetsDetail(TargetBase):
    is_complete: bool
