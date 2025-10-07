GST-Recon-Engine v1.0

Quickstart

1) Prereqs: Docker, Docker Compose, Make.
2) Copy `.env.example` to `.env` and adjust values.
3) `make up` to start the stack (API at http://localhost:8000).
4) Open OpenAPI at http://localhost:8000/docs and health at http://localhost:8000/health

Stack

- Python 3.11, FastAPI, Uvicorn
- Pandas, OpenPyXL, RapidFuzz, python-dateutil, Pydantic v2
- Postgres + SQLAlchemy; Redis + Celery
- MinIO (S3-compatible) for storage

Repo layout

- `/api` (FastAPI app and routers)
- `/core` (normalize, validators, reconcile, exports, gstr1)
- `/io` (mappers/parsers/storage)
- `/models` (pydantic + ORM bootstraps)
- `/ocr` (preprocess + OCR fallback)
- `/tests` (unit/integration)
- `/configs` (hsn codes etc.)
- `/scripts` (CLI tools)
- `/docker` (compose, Dockerfiles)
- `/docs` (runbook, samples)

Run locally (dev)

- Start API only: `make api` (hot-reload via uvicorn)
- Full stack: `make up` then `make logs`

CLI usage

- Reconcile purchases vs 2B and write outputs:
```bash
python -m scripts.reconcile --purchases purchases.xlsx --two_b two_b.xlsx --out out_dir --client-id demo --preset
```

- Build GSTR-1 outputs from sales file:
```bash
python -m scripts.export_gstr1 --sales sales.xlsx --out out_dir --turnover-band ">5cr"
```

API examples (curl)

- Upload purchases Excel:
```bash
curl -F "file=@purchases.xlsx" -F "client_id=demo" http://localhost:8000/upload/purchases/excel
```

- Upload GSTR-2B:
```bash
curl -F "file=@two_b.xlsx" http://localhost:8000/upload/2b
```

- Reconcile (use ids from previous responses):
```bash
curl -X POST http://localhost:8000/reconcile -H 'Content-Type: application/json' \
  -d '{"dataset_id":"ds_xxx","two_b_id":"2b_xxx","tolerances":{"amount_abs":1,"amount_pct":0.005,"date_days":3}}'
```

- Export ITC Excel and Tally CSV (returns presigned links):
```bash
curl http://localhost:8000/export/itc/ds_xxx
```

- Upload sales and export GSTR-1 files:
```bash
curl -F "file=@sales.xlsx" http://localhost:8000/upload/sales/excel
curl http://localhost:8000/export/gstr1/sales_xxx
```

Notes

- MinIO console at http://localhost:9001 (user `minio` / `minio123`).
- Environment: see `.env.example`. Default bucket `gst-recon`.
- OCR fallback is stubbed and heavy; set `OCR_FALLBACK=false` by default.

