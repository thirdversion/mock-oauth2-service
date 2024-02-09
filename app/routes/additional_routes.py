from fastapi import APIRouter

router = APIRouter()


@router.get("/online")
async def online():
    return {"message": "Service is online"}
