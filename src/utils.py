import requests
from fastapi import HTTPException, status

from . import config
from .database import get_db
from .models.cat import Cat


def check_breed(breed_name: str) -> None:
    try:
        response = requests.get(config.CAT_API_URL, timeout=5)
        response.raise_for_status()
        breeds = [b["name"].lower() for b in response.json()]
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
    db = get_db()
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise ValueError(f"Cat {cat_id} does not exist")
    if any(x.is_complete for x in cat.missions):
        raise ValueError(f"Cat {cat_id} is on the mission")
