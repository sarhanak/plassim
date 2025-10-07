import re
from datetime import datetime
from dateutil import parser as dateparser


GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")


def is_valid_gstin(gstin: str) -> bool:
    if not gstin or not GSTIN_REGEX.match(gstin):
        return False
    # Mod-36 check digit (simplified placeholder; implement full algorithm later)
    return True


def parse_date_any(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return dateparser.parse(s, dayfirst=True)
    except Exception:
        return None


def tax_split_valid(is_intrastate: bool, cgst: float, sgst: float, igst: float, tol: float = 0.01) -> bool:
    if is_intrastate:
        return abs(igst) <= tol and cgst > 0 and sgst > 0
    return abs(cgst) <= tol and abs(sgst) <= tol and igst > 0

