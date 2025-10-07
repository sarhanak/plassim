from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse


app = FastAPI(title="GST-Recon-Engine v1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

total_invoices = Gauge("total_invoices", "Total invoices processed")
matched = Gauge("matched", "Matched invoices")
mismatched = Gauge("mismatched", "Mismatched invoices")
missing_in_2b = Gauge("missing_in_2b", "Missing in 2B count")
extras_in_2b = Gauge("extras_in_2b", "Extras in 2B count")
ocr_low_conf_pages = Gauge("ocr_low_conf_pages", "Low confidence OCR pages")
job_time_ms = Gauge("job_time_ms", "Last job duration in ms")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    data = generate_latest()
    return PlainTextResponse(data, media_type=CONTENT_TYPE_LATEST)

# Routers
from api.routers.uploads import router as uploads_router  # noqa: E402
from api.routers.reconcile import router as reconcile_router  # noqa: E402
from api.routers.exports import router as exports_router  # noqa: E402
from api.routers.ops import router as ops_router  # noqa: E402

app.include_router(uploads_router)
app.include_router(reconcile_router)
app.include_router(exports_router)
app.include_router(ops_router)

