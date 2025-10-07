from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PurchaseInvoice(BaseModel):
    doc_id: str
    supplier_gstin: str
    supplier_name: Optional[str] = None
    invoice_no_raw: str
    invoice_no_norm: str
    invoice_date: str
    place_of_supply: Optional[str] = None
    hsn_code: Optional[str] = None
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: Optional[float] = 0.0
    round_off: Optional[float] = 0.0
    total_amount: float
    doc_type: str
    source: str


class GSTR2BRow(BaseModel):
    row_id: str
    supplier_gstin: str
    invoice_no: str
    invoice_date: Optional[str] = None
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: Optional[float] = 0.0
    total_amount: float
    doc_type: Optional[str] = None


class ReconResult(BaseModel):
    doc_id: str
    status: str
    matched_2b_ref: Optional[str] = None
    reason_codes: List[str] = Field(default_factory=list)
    diffs: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class SalesRow(BaseModel):
    invoice_no: str
    invoice_date: str
    receiver_gstin: Optional[str] = None
    receiver_name: Optional[str] = None
    place_of_supply: str
    invoice_type: str
    invoice_value: float
    hsn_code: str
    taxable_value: float
    igst: float
    cgst: float
    sgst: float
    cess: float
    doc_type: str
    doc_no: Optional[str] = None
    doc_date: Optional[str] = None
    export_flag: Optional[bool] = None
    lut_or_igst_paid: Optional[str] = None


class HSNTable12Row(BaseModel):
    type: str
    hsn_code: str
    uqc: str
    total_qty: float
    taxable_value: float
    igst: float
    cgst: float
    sgst: float
    cess: float


class Table13Row(BaseModel):
    doc_type: str
    series_no: str
    doc_no: str
    doc_date: str
    total_count: int
    cancelled_count: int
    net_issued: int

