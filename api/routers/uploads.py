from fastapi import APIRouter, UploadFile, File, Form
import pandas as pd
from api.state import DATASETS, TWO_B, SALES, Dataset, TwoB, Sales, gen_id
from io import BytesIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO
from io import BytesIO
from io import StringIO

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/purchases/excel")
async def upload_purchases_excel(
    file: UploadFile = File(...),
    client_id: str = Form(...),
    preset_id: str | None = Form(None),
) -> dict:
    content = await file.read()
    df = pd.read_excel(BytesIO(content)) if file.filename.lower().endswith(".xlsx") else pd.read_csv(BytesIO(content))
    from io.mapper import infer_mapping
    from io.parsers import parse_purchases

    mapping, scores = infer_mapping(df)
    purchases = parse_purchases(df, mapping)
    dataset_id = gen_id("ds")
    DATASETS[dataset_id] = Dataset(dataset_id=dataset_id, client_id=client_id, mapping=mapping, purchases=purchases)
    return {"dataset_id": dataset_id, "inferred_mapping": mapping, "row_stats": {"rows": len(purchases)}}


@router.post("/2b")
async def upload_2b(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    df = pd.read_excel(BytesIO(content)) if file.filename.lower().endswith(".xlsx") else pd.read_csv(BytesIO(content))
    from io.parsers import parse_2b

    rows = parse_2b(df, {})
    two_b_id = gen_id("2b")
    TWO_B[two_b_id] = TwoB(two_b_id=two_b_id, rows=rows)
    return {"two_b_id": two_b_id, "rows": len(rows)}


@router.post("/sales/excel")
async def upload_sales_excel(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    df = pd.read_excel(BytesIO(content)) if file.filename.lower().endswith(".xlsx") else pd.read_csv(BytesIO(content))
    from io.parsers import parse_sales

    rows = parse_sales(df, {})
    sales_id = gen_id("sales")
    SALES[sales_id] = Sales(sales_id=sales_id, rows=rows)
    return {"sales_id": sales_id, "rows": len(rows)}

