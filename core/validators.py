import re
from datetime import datetime
from typing import Optional


GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{1}Z[0-9A-Z]{1}$")


_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_CHAR_TO_VAL = {c: i for i, c in enumerate(_CHARSET)}


def _gstin_check_digit_compute(gstin14: str) -> str:
    # As per official MOD 36 algorithm with weighting pattern [1,2] repeating over 14 chars
    factor = 1
    total = 0
    for ch in gstin14:
        code_point = _CHAR_TO_VAL.get(ch, 0)
        addend = factor * code_point
        # Sum digits in base-36: addend = (addend // 36) + (addend % 36)
        addend = (addend // 36) + (addend % 36)
        total += addend
        factor = 2 if factor == 1 else 1
    remainder = total % 36
    check_code_point = (36 - remainder) % 36
    return _CHARSET[check_code_point]


def is_valid_gstin(gstin: str) -> bool:
    if not gstin or len(gstin) != 15 or not GSTIN_REGEX.match(gstin):
        return False
    expected = _gstin_check_digit_compute(gstin[:14])
    return gstin[-1] == expected


def parse_date_any(s: str) -> Optional[datetime]:
    if not s:
        return None
    fmts = [
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d %b %Y",
        "%d %B %Y",
        "%d/%m/%Y",
    ]
    for fmt in fmts:
        try:
            return datetime.strptime(s.strip(), fmt)
        except Exception:
            pass
    return None


def valid_tax_math(intrastate: bool, igst: float, cgst: float, sgst: float, tol: float = 0.01) -> bool:
    if intrastate:
        return abs(igst) <= tol and cgst > 0 and sgst > 0
    return igst > 0 and abs(cgst) <= tol and abs(sgst) <= tol


def is_hsn_length_valid(hsn: str, turnover_gt_5cr: bool) -> bool:
    if not hsn:
        return False
    digits = re.sub(r"\D", "", hsn)
    min_len = 6 if turnover_gt_5cr else 4
    return len(digits) >= min_len

