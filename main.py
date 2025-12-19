from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth_routes
from app.routes import users_routes 
models.Base.metadata.create_all(bind=engine)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mental Health Check-in API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(users_routes.router)

@app.get("/")
def root():
    return {"status": "API is running"}
