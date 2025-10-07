from typing import Optional, List, Dict, Literal
from datetime import date
from pydantic import BaseModel, Field


DocType = Literal["INV", "CN", "DN", "REVISED", "CANCELLED"]
SourceType = Literal["excel", "ocr"]
ReconStatus = Literal["MATCHED", "MISMATCH", "MISSING_IN_2B"]


class PurchaseInvoice(BaseModel):
    doc_id: str
    supplier_gstin: str
    supplier_name: Optional[str] = None
    invoice_no_raw: str
    invoice_no_norm: str
    invoice_date: date
    place_of_supply: Optional[str] = None
    hsn_code: Optional[str] = None
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: Optional[float] = 0.0
    round_off: Optional[float] = 0.0
    total_amount: float
    doc_type: DocType
    source: SourceType


class GSTR2BRow(BaseModel):
    row_id: str
    supplier_gstin: str
    invoice_no: str
    invoice_date: Optional[date] = None
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: Optional[float] = 0.0
    total_amount: float
    doc_type: Optional[DocType] = None


class ReconResult(BaseModel):
    doc_id: str
    status: ReconStatus
    matched_2b_ref: Optional[str] = None
    reason_codes: List[str] = Field(default_factory=list)
    diffs: Dict[str, Dict[str, Optional[str]]] = Field(default_factory=dict)


InvoiceType = Literal["REGULAR", "SEZ", "DEEMED_EXPORT", "EXPORT"]
LutFlag = Literal["LUT", "IGST", "NA"]


class SalesRow(BaseModel):
    invoice_no: str
    invoice_date: date
    receiver_gstin: Optional[str] = None
    receiver_name: Optional[str] = None
    place_of_supply: str
    invoice_type: InvoiceType
    invoice_value: float
    hsn_code: str
    taxable_value: float
    igst: float
    cgst: float
    sgst: float
    cess: float
    doc_type: str
    doc_no: Optional[str] = None
    doc_date: Optional[date] = None
    export_flag: Optional[bool] = None
    lut_or_igst_paid: LutFlag = "NA"


class HSNTable12Row(BaseModel):
    type: Literal["B2B", "B2C"]
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
    doc_date: date
    total_count: int
    cancelled_count: int
    @property
    def net_issued(self) -> int:
        return max(0, self.total_count - self.cancelled_count)

