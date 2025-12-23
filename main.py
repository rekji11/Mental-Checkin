from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routes import users_routes
from app.routes import tracker_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mental Health Check-in API")


origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)



app.include_router(users_routes.router)
app.include_router(tracker_routes.router)

@app.get("/")
def read_root():
    return {"message": "Api is running"}