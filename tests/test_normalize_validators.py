from core.normalize import normalize_invoice_number, variants
from core.validators import is_valid_gstin, parse_date_any, tax_split_valid


def test_normalize_invoice_number():
    assert normalize_invoice_number("INV-001/23") == "INV00123"


def test_variants_map():
    v = variants("B01S")
    assert "B01S" in v and "8015" in v


def test_gstin_regex_basic():
    # simplified, format-only check
    assert is_valid_gstin("27ABCDE1234F1Z5") is True


def test_parse_date_any():
    assert parse_date_any("03-07-2025").day == 3


def test_tax_split_valid():
    assert tax_split_valid(True, 10.0, 10.0, 0.0)
    assert tax_split_valid(False, 0.0, 0.0, 20.0)
