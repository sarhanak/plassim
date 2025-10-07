from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/purchases/excel")
async def upload_purchases_excel(
    file: UploadFile = File(...),
    client_id: str = Form(...),
    preset_id: str | None = Form(None),
) -> dict:
    return {"dataset_id": "demo-dataset", "inferred_mapping": {}, "row_stats": {"rows": 0}}


@router.post("/2b")
async def upload_2b(file: UploadFile = File(...)) -> dict:
    return {"two_b_id": "demo-2b", "rows": 0}


@router.post("/sales/excel")
async def upload_sales_excel(file: UploadFile = File(...)) -> dict:
    return {"sales_id": "demo-sales"}

