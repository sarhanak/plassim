from fastapi import APIRouter

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/itc/{dataset_id}")
def export_itc(dataset_id: str) -> dict:
    return {"claim_now": "", "hold_or_mismatch": "", "extras_in_2b": "", "tally": ""}


@router.get("/gstr1/{sales_id}")
def export_gstr1(sales_id: str) -> dict:
    return {"B2B": "", "B2C": "", "HSN_Table12": "", "Document_Table13": ""}

