from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/health",
    tags=["Sanity"],
    responses={503: {"message": "Service unavailable"}}
)


@router.get("")
async def sanity():
    return {"health": "UP"}

