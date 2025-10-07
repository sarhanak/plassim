from models.schemas import SalesRow
from core.gstr1 import split_b2b_b2c, build_b2_sheet, build_table12, build_table13


def sample_rows():
    return [
        SalesRow(invoice_no="A001", invoice_date="01-04-2025", receiver_gstin="27ABCDE1234F1Z5", receiver_name="X", place_of_supply="27", invoice_type="REGULAR", invoice_value=118.0, hsn_code="1001", taxable_value=100.0, igst=0.0, cgst=9.0, sgst=9.0, cess=0.0, doc_type="INV"),
        SalesRow(invoice_no="B002", invoice_date="02-04-2025", receiver_gstin=None, receiver_name="Y", place_of_supply="29", invoice_type="REGULAR", invoice_value=118.0, hsn_code="1001", taxable_value=100.0, igst=18.0, cgst=0.0, sgst=0.0, cess=0.0, doc_type="INV"),
    ]


def test_split_and_builders():
    rows = sample_rows()
    b2b, b2c = split_b2b_b2c(rows)
    assert len(b2b) == 1 and len(b2c) == 1
    b2b_xlsx = build_b2_sheet(b2b)
    b2c_xlsx = build_b2_sheet(b2c)
    assert len(b2b_xlsx) > 100 and len(b2c_xlsx) > 100
    t12 = build_table12(rows)
    t13 = build_table13(rows)
    assert len(t12) > 100 and len(t13) > 100

