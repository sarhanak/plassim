from __future__ import annotations

import io
from typing import List, Tuple
import pandas as pd

from models.schemas import PurchaseInvoice, ReconResult


def build_itc_excels(purchases: List[PurchaseInvoice], results: List[ReconResult]) -> Tuple[bytes, bytes, bytes]:
    status_by_doc = {r.doc_id: r for r in results}
    rows_claim = []
    rows_hold = []
    for p in purchases:
        r = status_by_doc.get(p.doc_id)
        base = {
            "supplier_gstin": p.supplier_gstin,
            "supplier_name": p.supplier_name,
            "invoice_no": p.invoice_no_norm,
            "invoice_date": p.invoice_date,
            "taxable_value": p.taxable_value,
            "igst": p.igst_amount,
            "cgst": p.cgst_amount,
            "sgst": p.sgst_amount,
            "cess": p.cess_amount,
            "total_amount": p.total_amount,
        }
        if r and r.status == "MATCHED":
            rows_claim.append({**base, "status": "MATCHED"})
        else:
            reason = ",".join(r.reason_codes) if r else ""
            rows_hold.append({**base, "status": "HOLD", "reason_codes": reason, "diffs": getattr(r, "diffs", {})})

    def to_bytes(df: pd.DataFrame) -> bytes:
        buff = io.BytesIO()
        with pd.ExcelWriter(buff, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        return buff.getvalue()

    claim_now = to_bytes(pd.DataFrame(rows_claim))
    hold = to_bytes(pd.DataFrame(rows_hold))
    extras = to_bytes(pd.DataFrame([]))
    return claim_now, hold, extras


def build_tally_csv(purchases: List[PurchaseInvoice]) -> str:
    import csv
    from io import StringIO

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Date",
        "VoucherType",
        "PartyName",
        "PartyGSTIN",
        "InvoiceNumber",
        "InvoiceDate",
        "TaxableValue",
        "CGST",
        "SGST",
        "IGST",
        "Cess",
        "RoundOff",
        "Total",
        "Narration",
    ])
    for p in purchases:
        writer.writerow([
            p.invoice_date,
            "Purchase",
            p.supplier_name or "",
            p.supplier_gstin,
            p.invoice_no_norm,
            p.invoice_date,
            f"{p.taxable_value:.2f}",
            f"{p.cgst_amount:.2f}",
            f"{p.sgst_amount:.2f}",
            f"{p.igst_amount:.2f}",
            f"{p.cess_amount or 0.0:.2f}",
            f"{p.round_off or 0.0:.2f}",
            f"{p.total_amount:.2f}",
            "Imported via GST-Recon-Engine",
        ])
    return output.getvalue()

