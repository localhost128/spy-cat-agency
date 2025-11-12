from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Body
from starlette.status import HTTP_400_BAD_REQUEST

from ..database import DatabaseDep
from ..utils import chek_cat
from ..models.mission import Mission, Target
from ..schemas.mission import (
    MissionCreate,
    MissionDetail,
    MissionUpdateCat,
    TargetUpdateNotes,
)

router: APIRouter = APIRouter(prefix="/missions", tags=["missions"])


@router.get("", response_model=list[MissionDetail])
def get_missions(db: DatabaseDep) -> list[Mission]:
    return db.query(Mission).all()


@router.post("", response_model=MissionDetail)
def create_mission(db: DatabaseDep, new_mission: MissionCreate) -> Mission:
    targets: list[Target] = [Target(**x.model_dump()) for x in new_mission.targets]
    mission_data = new_mission.model_dump()
    del mission_data["targets"]
    mission: Mission = Mission(**mission_data, targets=targets)
    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.get("/{mission_id}", response_model=MissionDetail)
def get_mission(db: DatabaseDep, mission_id: int) -> Mission:
    mission: Mission | None = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mission not found")

    return mission


@router.delete("/{mission_id}", response_model=MissionDetail)
def delete_mission(db: DatabaseDep, mission_id: int) -> Mission:
    mission: Mission | None = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mission not found")
    if not mission.is_complete and mission.cat_id is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cat on the mission")
    db.delete(mission)
    db.commit()
    return mission


@router.patch("/{mission_id}/assign_cat", response_model=MissionDetail)
def update_mission_cat(
    db: DatabaseDep, mission_id: int, update_cat: MissionUpdateCat
) -> Mission:
    cat_id: int = update_cat.cat_id
    mission: Mission | None = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mission not found")

    try:
        chek_cat(cat_id)
    except ValueError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

    mission.cat_id = cat_id

    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


@router.patch("/{mission_id}/{target_id}/mark_complete", response_model=MissionDetail)
def mark_mission_target_complete(
    db: DatabaseDep, mission_id: int, target_id: int
) -> Mission:
    mission: Mission | None = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mission not found")
    targets: list[Target] = [x for x in mission.targets if x.id == target_id]
    if not targets:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Target not found")

    target: Target = targets[0]
    target.is_complete = True
    db.add(target)
    db.commit()
    db.refresh(mission)
    return mission


@router.patch("/{mission_id}/{target_id}/update_notes", response_model=MissionDetail)
def update_mission_target_notes(
    db: DatabaseDep, mission_id: int, target_id: int, notes_update: TargetUpdateNotes
) -> Mission:
    notes: str = notes_update.notes
    mission: Mission | None = db.query(Mission).get(mission_id)
    if not mission:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Mission not found")
    targets: list[Target] = [x for x in mission.targets if x.id == target_id]
    if not targets:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Target not found")

    target: Target = targets[0]
    if target.is_complete:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Target is complete")

    target.notes = notes
    db.add(target)
    db.commit()
    db.refresh(mission)
    return mission
