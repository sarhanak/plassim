from __future__ import annotations

from typing import Dict, List, Tuple
import pandas as pd
from rapidfuzz import fuzz, process


TARGET_COLS = {
    "supplier_gstin": ["gstin", "gst no", "gst number", "supplier gstin", "party gstin"],
    "supplier_name": ["supplier", "party", "vendor", "name"],
    "invoice_no_raw": ["invoice no", "bill no", "voucher no", "inv no", "invoice number"],
    "invoice_date": ["date", "bill date", "invoice date", "inv date"],
    "place_of_supply": ["pos", "place of supply", "state"],
    "hsn_code": ["hsn", "hsn code", "sac"],
    "taxable_value": ["taxable", "taxable value", "taxable amt"],
    "cgst_amount": ["cgst", "cgst amount"],
    "sgst_amount": ["sgst", "sgst amount"],
    "igst_amount": ["igst", "igst amount"],
    "cess_amount": ["cess"],
    "round_off": ["round off", "rounding"],
    "total_amount": ["total", "invoice total", "grand total"],
    "doc_type": ["doc type", "type"],
}


def infer_mapping(df: pd.DataFrame, score_threshold: int = 80) -> Tuple[Dict[str, str], Dict[str, int]]:
    cols = [str(c).strip().lower() for c in df.columns]
    mapping: Dict[str, str] = {}
    scores: Dict[str, int] = {}
    for target, synonyms in TARGET_COLS.items():
        choices = cols
        best = process.extractOne(
            target.replace("_", " "), choices, scorer=fuzz.WRatio
        )
        cand_list = synonyms + [target.replace("_", " ")]
        best_syn = process.extractOne(best[0], cand_list, scorer=fuzz.WRatio) if best else None
        if best and best[1] >= score_threshold:
            mapping[target] = best[0]
            scores[target] = int(best[1])
        elif best_syn and best_syn[1] >= score_threshold:
            # try synonyms on original headers
            best2 = process.extractOne(best_syn[0], choices, scorer=fuzz.WRatio)
            if best2 and best2[1] >= score_threshold:
                mapping[target] = best2[0]
                scores[target] = int(best2[1])
    return mapping, scores

