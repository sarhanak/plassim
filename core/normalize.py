import re

LABELS = re.compile(r"\b(INV|INVOICE|BILL|NO|NUMBER|#)\b", re.IGNORECASE)
STRIP_CHARS = re.compile(r"[\s\-_/.:]", re.IGNORECASE)
REPEAT_COLLAPSE = re.compile(r"(.)\1{3,}")

VARIANT_MAP = str.maketrans({
    "O": "0",
    "I": "1",
    "L": "1",
    "S": "5",
    "B": "8",
})


def normalize_invoice_number(raw: str) -> str:
    if not raw:
        return ""
    s = raw.upper()
    s = LABELS.sub(" ", s)
    s = STRIP_CHARS.sub("", s)
    s = REPEAT_COLLAPSE.sub(r"\1\1\1", s)
    s = s.lstrip("0")
    return s


def variants(invoice_no_norm: str) -> set[str]:
    if not invoice_no_norm:
        return {""}
    v = invoice_no_norm.translate(VARIANT_MAP)
    return {invoice_no_norm, v}

