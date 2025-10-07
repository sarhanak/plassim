from __future__ import annotations

import io
from typing import Iterable, List, Tuple
import pandas as pd

from models.schemas import SalesRow, HSNTable12Row, Table13Row


GSTR1_B2_ORDER = [
    "Invoice No",
    "Invoice Date",
    "GSTIN of Recipient",
    "Receiver Name",
    "Place of Supply",
    "Invoice Type",
    "Invoice Value",
    "HSN/SAC Code",
    "Taxable Value",
    "Tax Rate (%)",
    "IGST",
    "CGST",
    "SGST",
    "Cess",
    "Document Type",
    "Document Number/Date",
    "Export under LUT/IGST (Yes/No as applicable)",
]


def split_b2b_b2c(rows: Iterable[SalesRow]) -> Tuple[List[SalesRow], List[SalesRow]]:
    b2b: List[SalesRow] = []
    b2c: List[SalesRow] = []
    for r in rows:
        if r.receiver_gstin:
            b2b.append(r)
        else:
            b2c.append(r)
    return b2b, b2c


def build_b2_sheet(rows: List[SalesRow]) -> bytes:
    sheet_rows = []
    for r in rows:
        sheet_rows.append({
            "Invoice No": r.invoice_no,
            "Invoice Date": r.invoice_date,
            "GSTIN of Recipient": r.receiver_gstin or "",
            "Receiver Name": r.receiver_name or "",
            "Place of Supply": r.place_of_supply,
            "Invoice Type": r.invoice_type,
            "Invoice Value": r.invoice_value,
            "HSN/SAC Code": r.hsn_code,
            "Taxable Value": r.taxable_value,
            "Tax Rate (%)": 0,
            "IGST": r.igst,
            "CGST": r.cgst,
            "SGST": r.sgst,
            "Cess": r.cess,
            "Document Type": r.doc_type,
            "Document Number/Date": (r.doc_no or "") + (f"/{r.doc_date}" if r.doc_date else ""),
            "Export under LUT/IGST (Yes/No as applicable)": r.lut_or_igst_paid or "NA",
        })
    df = pd.DataFrame(sheet_rows, columns=GSTR1_B2_ORDER)
    buff = io.BytesIO()
    with pd.ExcelWriter(buff, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buff.getvalue()


def build_table12(rows: List[SalesRow]) -> bytes:
    acc = {}
    for r in rows:
        key = ("B2B" if r.receiver_gstin else "B2C", r.hsn_code)
        cur = acc.setdefault(key, {"total_qty": 0.0, "taxable_value": 0.0, "igst": 0.0, "cgst": 0.0, "sgst": 0.0, "cess": 0.0})
        cur["taxable_value"] += float(r.taxable_value)
        cur["igst"] += float(r.igst)
        cur["cgst"] += float(r.cgst)
        cur["sgst"] += float(r.sgst)
        cur["cess"] += float(r.cess)
    out_rows = []
    for (typ, hsn), v in acc.items():
        out_rows.append({
            "Type": typ,
            "HSN Code": hsn,
            "UQC": "NOS",
            "Total Quantity": v["total_qty"],
            "Taxable Value": v["taxable_value"],
            "IGST": v["igst"],
            "CGST": v["cgst"],
            "SGST": v["sgst"],
            "Cess": v["cess"],
        })
    df = pd.DataFrame(out_rows, columns=["Type", "HSN Code", "UQC", "Total Quantity", "Taxable Value", "IGST", "CGST", "SGST", "Cess"])
    buff = io.BytesIO()
    with pd.ExcelWriter(buff, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buff.getvalue()


def build_table13(rows: List[SalesRow]) -> bytes:
    # Count by doc_type and simple series derivation from invoice_no prefix before first digit
    import re

    def series_of(inv: str) -> str:
        m = re.match(r"^[^0-9A-Za-z]*([A-Za-z]*)", inv or "")
        return (m.group(1) if m else "").upper() or "NA"

    counts = {}
    for r in rows:
        key = (r.doc_type, series_of(r.invoice_no))
        cur = counts.setdefault(key, {"total": 0, "cancelled": 0})
        cur["total"] += 1
        # cancellation not modeled yet; keep zero
    out = []
    for (doc_type, series_no), v in counts.items():
        out.append({
            "Document Type": doc_type,
            "Series No": series_no,
            "Document Number": "",
            "Document Date": "",
            "Total Number": v["total"],
            "Cancelled": v["cancelled"],
            "Net Issued": v["total"] - v["cancelled"],
        })
    df = pd.DataFrame(out, columns=["Document Type", "Series No", "Document Number", "Document Date", "Total Number", "Cancelled", "Net Issued"])
    buff = io.BytesIO()
    with pd.ExcelWriter(buff, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return buff.getvalue()

