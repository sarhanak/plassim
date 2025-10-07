from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
from rapidfuzz import fuzz

from models.schemas import PurchaseInvoice, GSTR2BRow, ReconResult
from core.normalize import variants
from core.enums import ReasonCode


@dataclass
class Tolerances:
    amount_abs: float = 1.0
    amount_pct: float = 0.005
    date_days: int = 3


def within_amount_tol(a: float, b: float, tol: Tolerances) -> bool:
    diff = abs(a - b)
    pct = diff / max(1.0, abs(a))
    return diff <= max(tol.amount_abs, tol.amount_pct * abs(a))


def reconcile(purchases: List[PurchaseInvoice], two_b: List[GSTR2BRow], tol: Tolerances | None = None) -> Tuple[List[ReconResult], Dict[str, int]]:
    tol = tol or Tolerances()
    index: Dict[str, List[GSTR2BRow]] = {}
    for r in two_b:
        index.setdefault(r.supplier_gstin, []).append(r)

    results: List[ReconResult] = []
    extras_in_2b: set[str] = {f"{r.supplier_gstin}|{r.invoice_no}" for r in two_b}

    for p in purchases:
        candidates = index.get(p.supplier_gstin, [])
        found: GSTR2BRow | None = None
        # pass 1: exact variant
        pv = variants(p.invoice_no_norm)
        for c in candidates:
            if c.invoice_no in pv and within_amount_tol(p.total_amount, c.total_amount, tol):
                found = c
                break
        # pass 2: fuzzy on invoice_no gated by amount
        if not found:
            best = None
            best_score = 0
            for c in candidates:
                score = fuzz.partial_ratio(p.invoice_no_norm, c.invoice_no)
                if score > best_score and within_amount_tol(p.total_amount, c.total_amount, tol):
                    best = c
                    best_score = score
            if best and best_score >= 90:
                found = best

        if found:
            extras_in_2b.discard(f"{found.supplier_gstin}|{found.invoice_no}")
            if within_amount_tol(p.total_amount, found.total_amount, tol):
                results.append(ReconResult(doc_id=p.doc_id, status="MATCHED", matched_2b_ref=found.row_id, reason_codes=[], diffs={}))
            else:
                results.append(ReconResult(doc_id=p.doc_id, status="MISMATCH", matched_2b_ref=found.row_id, reason_codes=[ReasonCode.AMOUNT_MISMATCH.value], diffs={"total_amount": {"ours": p.total_amount, "two_b": found.total_amount}}))
        else:
            results.append(ReconResult(doc_id=p.doc_id, status="MISMATCH", matched_2b_ref=None, reason_codes=[ReasonCode.MISSING_IN_2B.value], diffs={}))

    counts = {
        "matched": sum(1 for r in results if r.status == "MATCHED"),
        "mismatched": sum(1 for r in results if r.status == "MISMATCH"),
        "missing_in_2b": sum(1 for r in results if ReasonCode.MISSING_IN_2B.value in r.reason_codes),
        "extras_in_2b": len(extras_in_2b),
    }
    return results, counts

