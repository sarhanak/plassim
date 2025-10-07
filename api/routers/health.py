from fastapi import APIRouter
from datetime import datetime


router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "time_utc": datetime.utcnow().isoformat(timespec="seconds")}

