from __future__ import annotations

from typing import List, Tuple
import pandas as pd

from core.normalize import normalize_invoice_number
from models.schemas import PurchaseInvoice, GSTR2BRow, SalesRow


def load_excel_or_csv(file_path: str) -> pd.DataFrame:
    if file_path.lower().endswith(".csv"):
        return pd.read_csv(file_path)
    return pd.read_excel(file_path)


def parse_purchases(df: pd.DataFrame, mapping: dict) -> List[PurchaseInvoice]:
    recs: List[PurchaseInvoice] = []
    for _, row in df.iterrows():
        inv_raw = str(row.get(mapping.get("invoice_no_raw", "invoice no"), ""))
        inv_norm = normalize_invoice_number(inv_raw)
        recs.append(
            PurchaseInvoice(
                doc_id=f"{row.get(mapping.get('supplier_gstin', 'gstin'), '')}-{inv_norm}",
                supplier_gstin=str(row.get(mapping.get("supplier_gstin", "gstin"), "")),
                supplier_name=str(row.get(mapping.get("supplier_name", "supplier"), "")) or None,
                invoice_no_raw=inv_raw,
                invoice_no_norm=inv_norm,
                invoice_date=str(row.get(mapping.get("invoice_date", "date"), "")),
                place_of_supply=str(row.get(mapping.get("place_of_supply", "pos"), "")) or None,
                hsn_code=str(row.get(mapping.get("hsn_code", "hsn"), "")) or None,
                taxable_value=float(row.get(mapping.get("taxable_value", "taxable"), 0) or 0),
                cgst_amount=float(row.get(mapping.get("cgst_amount", "cgst"), 0) or 0),
                sgst_amount=float(row.get(mapping.get("sgst_amount", "sgst"), 0) or 0),
                igst_amount=float(row.get(mapping.get("igst_amount", "igst"), 0) or 0),
                cess_amount=float(row.get(mapping.get("cess_amount", "cess"), 0) or 0),
                round_off=float(row.get(mapping.get("round_off", "round off"), 0) or 0),
                total_amount=float(row.get(mapping.get("total_amount", "total"), 0) or 0),
                doc_type=str(row.get(mapping.get("doc_type", "doc type"), "INV") or "INV"),
                source="excel",
            )
        )
    return recs


def parse_2b(df: pd.DataFrame, mapping: dict) -> List[GSTR2BRow]:
    recs: List[GSTR2BRow] = []
    for _, row in df.iterrows():
        recs.append(
            GSTR2BRow(
                row_id=str(row.get("row_id", "")) or None or "",
                supplier_gstin=str(row.get(mapping.get("supplier_gstin", "gstin"), "")),
                invoice_no=str(row.get(mapping.get("invoice_no", "invoice no"), "")),
                invoice_date=str(row.get(mapping.get("invoice_date", "date"), "")) or None,
                taxable_value=float(row.get(mapping.get("taxable_value", "taxable"), 0) or 0),
                cgst_amount=float(row.get(mapping.get("cgst_amount", "cgst"), 0) or 0),
                sgst_amount=float(row.get(mapping.get("sgst_amount", "sgst"), 0) or 0),
                igst_amount=float(row.get(mapping.get("igst_amount", "igst"), 0) or 0),
                cess_amount=float(row.get(mapping.get("cess_amount", "cess"), 0) or 0),
                total_amount=float(row.get(mapping.get("total_amount", "total"), 0) or 0),
                doc_type=str(row.get(mapping.get("doc_type", "doc type"), "INV") or "INV"),
            )
        )
    return recs


def parse_sales(df: pd.DataFrame, mapping: dict) -> List[SalesRow]:
    recs: List[SalesRow] = []
    for _, row in df.iterrows():
        recs.append(
            SalesRow(
                invoice_no=str(row.get(mapping.get("invoice_no", "invoice no"), "")),
                invoice_date=str(row.get(mapping.get("invoice_date", "date"), "")),
                receiver_gstin=str(row.get(mapping.get("receiver_gstin", "gstin"), "")) or None,
                receiver_name=str(row.get(mapping.get("receiver_name", "name"), "")) or None,
                place_of_supply=str(row.get(mapping.get("place_of_supply", "pos"), "")),
                invoice_type=str(row.get(mapping.get("invoice_type", "invoice type"), "REGULAR")),
                invoice_value=float(row.get(mapping.get("invoice_value", "invoice value"), 0) or 0),
                hsn_code=str(row.get(mapping.get("hsn_code", "hsn"), "")),
                taxable_value=float(row.get(mapping.get("taxable_value", "taxable"), 0) or 0),
                igst=float(row.get(mapping.get("igst", "igst"), 0) or 0),
                cgst=float(row.get(mapping.get("cgst", "cgst"), 0) or 0),
                sgst=float(row.get(mapping.get("sgst", "sgst"), 0) or 0),
                cess=float(row.get(mapping.get("cess", "cess"), 0) or 0),
                doc_type=str(row.get(mapping.get("doc_type", "doc type"), "INV")),
                doc_no=str(row.get(mapping.get("doc_no", "doc no"), "")) or None,
                doc_date=str(row.get(mapping.get("doc_date", "doc date"), "")) or None,
                export_flag=bool(row.get(mapping.get("export_flag", "export"), False)),
                lut_or_igst_paid=str(row.get(mapping.get("lut_or_igst_paid", "lut/igst"), "NA")),
            )
        )
    return recs

