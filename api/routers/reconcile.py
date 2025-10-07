from fastapi import APIRouter
from api.state import DATASETS, TWO_B, RECONS, ReconJob
from core.reconcile import reconcile, Tolerances

router = APIRouter(prefix="/reconcile", tags=["reconcile"])


@router.post("")
async def run_reconcile(body: dict) -> dict:
    dataset_id = body["dataset_id"]
    two_b_id = body["two_b_id"]
    tol = body.get("tolerances", {})
    ds = DATASETS.get(dataset_id)
    tb = TWO_B.get(two_b_id)
    if not ds or not tb:
        return {"error": "dataset_id or two_b_id not found"}
    results, counts = reconcile(ds.purchases, tb.rows, Tolerances(
        amount_abs=float(tol.get("amount_abs", 1.0)),
        amount_pct=float(tol.get("amount_pct", 0.005)),
        date_days=int(tol.get("date_days", 3)),
    ))
    job = ReconJob(dataset_id=dataset_id, two_b_id=two_b_id, results=results, counts=counts)
    RECONS[dataset_id] = job
    return counts

