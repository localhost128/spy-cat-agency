from fastapi import FastAPI

from .database import Base, engine
from .routes.cat import router as car_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(car_router)
