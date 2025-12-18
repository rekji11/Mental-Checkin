from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mental Health Check-in API")

app.include_router(auth_routes.router)

@app.get("/")
def root():
    return {"status": "API is running"}
