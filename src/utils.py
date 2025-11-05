import requests
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import config
from .database import SessionLocal
from .models.cat import Cat


def check_breed(breed_name: str) -> None:
    try:
        response = requests.get(config.CAT_API_URL, timeout=5)
        response.raise_for_status()
        breeds = [x["name"].lower() for x in response.json()]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not verify breed with TheCatAPI",
        )
    if breed_name.lower() not in breeds:
        raise ValueError(
            f"Invalid breed '{breed_name}'. Check TheCatAPI for valid options."
        )


def chek_cat(cat_id: int) -> None:
    db: Session = SessionLocal()
    cat: Cat | None = db.query(Cat).get(cat_id)
    if not cat:
        db.close()
        raise ValueError(f"Cat {cat_id} does not exist")
    if any(not x.is_complete for x in cat.missions):
        db.close()
        raise ValueError(f"Cat {cat_id} is on the mission")
    db.close()
