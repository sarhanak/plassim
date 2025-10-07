from fastapi import APIRouter
from api.state import DATASETS, RECONS, SALES
from core.exports import build_itc_excels, build_tally_csv
from core.gstr1 import split_b2b_b2c, build_b2_sheet, build_table12, build_table13
from io.storage import put_bytes, presign
import time
import os

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/itc/{dataset_id}")
def export_itc(dataset_id: str) -> dict:
    ds = DATASETS.get(dataset_id)
    job = RECONS.get(dataset_id)
    if not ds or not job:
        return {"error": "dataset or recon not found"}
    claim_now, hold, extras = build_itc_excels(ds.purchases, job.results)
    tally_csv = build_tally_csv(ds.purchases)
    bucket = os.getenv("S3_BUCKET", "gst-recon")
    ts = int(time.time())
    k1 = f"{dataset_id}/claim_now_{ts}.xlsx"
    k2 = f"{dataset_id}/hold_or_mismatch_{ts}.xlsx"
    k3 = f"{dataset_id}/extras_in_2b_{ts}.xlsx"
    k4 = f"{dataset_id}/Tally_Purchase_Import_{ts}.csv"
    put_bytes(bucket, k1, claim_now, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k2, hold, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k3, extras, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k4, tally_csv.encode("utf-8"), "text/csv")
    return {
        "claim_now": presign(bucket, k1),
        "hold_or_mismatch": presign(bucket, k2),
        "extras_in_2b": presign(bucket, k3),
        "tally": presign(bucket, k4),
    }


@router.get("/gstr1/{sales_id}")
def export_gstr1(sales_id: str) -> dict:
    sales = SALES.get(sales_id)
    if not sales:
        return {"error": "sales not found"}
    b2b, b2c = split_b2b_b2c(sales.rows)
    b2b_x = build_b2_sheet(b2b)
    b2c_x = build_b2_sheet(b2c)
    t12 = build_table12(sales.rows)
    t13 = build_table13(sales.rows)
    bucket = os.getenv("S3_BUCKET", "gst-recon")
    ts = int(time.time())
    k1 = f"{sales_id}/B2B_{ts}.xlsx"
    k2 = f"{sales_id}/B2C_{ts}.xlsx"
    k3 = f"{sales_id}/HSN_Table12_{ts}.xlsx"
    k4 = f"{sales_id}/Document_Table13_{ts}.xlsx"
    put_bytes(bucket, k1, b2b_x, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k2, b2c_x, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k3, t12, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    put_bytes(bucket, k4, t13, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return {
        "B2B": presign(bucket, k1),
        "B2C": presign(bucket, k2),
        "HSN_Table12": presign(bucket, k3),
        "Document_Table13": presign(bucket, k4),
    }

