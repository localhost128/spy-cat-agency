from fastapi import APIRouter, HTTPException, status

from ..database import DatabaseDep
from ..models.cat import Cat
from ..schemas.cat import CatDetail, CatCreate

router = APIRouter(prefix="/cats", tags=["cats"])


@router.get("", response_model=list[CatDetail])
def get_cats(db: DatabaseDep) -> list[Cat]:
    return db.query(Cat).all()


@router.post("", response_model=CatDetail)
def create_cat(db: DatabaseDep, new_cat: CatCreate) -> Cat:
    cat = Cat(**new_cat.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get("/{cat_id}", response_model=CatDetail)
def get_cat(db: DatabaseDep, cat_id: int) -> Cat:
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cat not found")
    return cat


@router.put("/{cat_id}", response_model=CatDetail)
def update_cat(db: DatabaseDep, cat_id: int, new_cat: CatCreate) -> Cat:
    cat = db.query(Cat).get(cat_id)

    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cat not found")

    for var, value in vars(new_cat).items():
        setattr(cat, var, value) if value else None

    return cat


@router.delete("/{cat_id}", response_model=CatDetail)
def delete_cat(db: DatabaseDep, cat_id: int) -> Cat:
    cat = db.query(Cat).get(cat_id)
    if not cat:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cat not found")
    db.delete(cat)
    db.commit()
    return cat
