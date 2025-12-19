from fastapi import APIRouter, Depends
from app.deps import oauth2_scheme

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def read_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
