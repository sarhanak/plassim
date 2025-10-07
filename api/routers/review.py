from __future__ import annotations

from fastapi import APIRouter, Query
from api.state import DATASETS, RECONS, TWO_B
from typing import Optional
import csv
import os


router = APIRouter(prefix="/review", tags=["review"])


@router.get("/{dataset_id}")
def get_review(dataset_id: str, doc_id: Optional[str] = Query(None)) -> dict:
    ds = DATASETS.get(dataset_id)
    job = RECONS.get(dataset_id)
    if not ds or not job:
        return {"error": "dataset or recon not found"}
    # build map for 2B lookup
    two_b_map = {}
    for tb in TWO_B.values():
        for r in tb.rows:
            two_b_map[(r.supplier_gstin, r.invoice_no)] = r
    rows = []
    for p in ds.purchases:
        if doc_id and p.doc_id != doc_id:
            continue
        rr = next((r for r in job.results if r.doc_id == p.doc_id), None)
        two_b_ref = None
        if rr and rr.matched_2b_ref:
            # fallback by key if row_id unknown in this stub
            two_b_ref = two_b_map.get((p.supplier_gstin, p.invoice_no_norm))
        rows.append({
            "purchase": p.model_dump(),
            "recon": rr.model_dump() if rr else None,
            "two_b": two_b_ref.model_dump() if two_b_ref else None,
        })
    return {"rows": rows}


@router.get("/hsn")
def get_hsn() -> dict:
    path_csv = os.path.join("configs", "hsn_codes.csv")
    codes = []
    if os.path.exists(path_csv):
        with open(path_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row.get("hsn_code") or row.get("HSN") or row.get("code")
                desc = row.get("description") or row.get("desc") or ""
                if code:
                    codes.append({"code": str(code), "description": desc})
    else:
        codes = [{"code": "1001", "description": "Wheat and meslin"}]
    return {"hsn": codes}

