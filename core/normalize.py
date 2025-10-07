import re
from typing import Iterable, List


LABEL_PATTERN = re.compile(r"\b(INVOICE|INV|BILL|NO|NUMBER|#)\b", re.IGNORECASE)
SEPARATORS_PATTERN = re.compile(r"[\s\-_/.:]+")
REPEAT_COLLAPSE_PATTERN = re.compile(r"(.)\1{3,}")


def normalize_invoice_number(raw: str) -> str:
    if raw is None:
        return ""
    s = raw.upper().strip()
    s = LABEL_PATTERN.sub(" ", s)
    s = SEPARATORS_PATTERN.sub("", s)
    s = REPEAT_COLLAPSE_PATTERN.sub(r"\1\1\1", s)
    s = s.lstrip("0")
    return s


def build_variants(inv: str) -> List[str]:
    if not inv:
        return [""]
    base = inv
    swaps = [
        ("O", "0"),
        ("I", "1"),
        ("L", "1"),
        ("S", "5"),
        ("B", "8"),
    ]
    variants = {base}
    for a, b in swaps:
        variants.add(base.replace(a, b))
        variants.add(base.replace(b, a))
    # LETTERS-NUMBERS form: split alpha/numeric blocks with hyphen
    alphas = re.findall(r"[A-Z]+", base)
    nums = re.findall(r"\d+", base)
    if alphas and nums:
        variants.add(f"{alphas[0]}{nums[0]}")
        variants.add(f"{alphas[0]}-{nums[0]}")
    return list(variants)

