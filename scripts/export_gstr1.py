from __future__ import annotations

import typer
import pandas as pd
from io.parsers import parse_sales
from core.gstr1 import split_b2b_b2c, build_b2_sheet, build_table12, build_table13
from pathlib import Path


app = typer.Typer()


@app.command()
def main(
    sales: str = typer.Option(..., help="Sales Excel/CSV"),
    out: str = typer.Option("out", help="Output directory"),
    turnover_band: str = typer.Option(">5cr", help="Turnover band for HSN enforcement (unused in CLI stub)"),
):
    s_path = Path(sales)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    sdf = pd.read_excel(s_path) if s_path.suffix.lower() == ".xlsx" else pd.read_csv(s_path)
    rows = parse_sales(sdf, {})
    b2b, b2c = split_b2b_b2c(rows)
    (out_dir / "B2B.xlsx").write_bytes(build_b2_sheet(b2b))
    (out_dir / "B2C.xlsx").write_bytes(build_b2_sheet(b2c))
    (out_dir / "HSN_Table12.xlsx").write_bytes(build_table12(rows))
    (out_dir / "Document_Table13.xlsx").write_bytes(build_table13(rows))

    typer.echo({"b2b": len(b2b), "b2c": len(b2c)})


if __name__ == "__main__":
    app()

