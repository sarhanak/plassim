from __future__ import annotations

import typer
import pandas as pd
from io.mapper import infer_mapping
from io.parsers import parse_purchases, parse_2b
from core.reconcile import reconcile, Tolerances
from core.exports import build_itc_excels, build_tally_csv
from pathlib import Path


app = typer.Typer()


@app.command()
def main(
    purchases: str = typer.Option(..., help="Purchases Excel/CSV"),
    two_b: str = typer.Option(..., help="GSTR-2B Excel/CSV"),
    out: str = typer.Option("out", help="Output directory"),
    client_id: str = typer.Option("demo", help="Client ID"),
    preset: bool = typer.Option(False, help="Save preset (not persistent in CLI)"),
):
    p_path = Path(purchases)
    t_path = Path(two_b)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf = pd.read_excel(p_path) if p_path.suffix.lower() == ".xlsx" else pd.read_csv(p_path)
    mapping, _ = infer_mapping(pdf)
    p_rows = parse_purchases(pdf, mapping)

    tdf = pd.read_excel(t_path) if t_path.suffix.lower() == ".xlsx" else pd.read_csv(t_path)
    t_rows = parse_2b(tdf, {})

    results, counts = reconcile(p_rows, t_rows, Tolerances())
    claim_now, hold, extras = build_itc_excels(p_rows, results)
    tally_csv = build_tally_csv(p_rows)

    (out_dir / "claim_now.xlsx").write_bytes(claim_now)
    (out_dir / "hold_or_mismatch.xlsx").write_bytes(hold)
    (out_dir / "extras_in_2b.xlsx").write_bytes(extras)
    (out_dir / "Tally_Purchase_Import.csv").write_text(tally_csv, encoding="utf-8")

    typer.echo(counts)


if __name__ == "__main__":
    app()

