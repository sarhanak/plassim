from fastapi import APIRouter

router = APIRouter(prefix="/reconcile", tags=["reconcile"])


@router.post("")
async def run_reconcile(body: dict) -> dict:
    return {"matched": 0, "mismatched": 0, "missing_in_2b": 0, "links": {}}

