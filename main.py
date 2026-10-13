from fastapi import FastAPI

import models
from database import Base, engine
from routes_auth import router as auth_router
from routes_users import router as users_router
from routes_notes import router as notes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes API")
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(notes_router)    