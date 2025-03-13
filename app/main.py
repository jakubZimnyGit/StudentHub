from fastapi import FastAPI
from . database import engine
from . import models
from . routers import grades, students, teachers, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
