from datetime import datetime
import os

from fastapi import FastAPI
from api.routers.health import router as health_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="GST-Recon-Engine v1.0", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router)


@app.get("/metrics")
async def metrics() -> dict:
    # Stub metrics; will be updated by pipelines
    return {
        "total_invoices": 0,
        "matched": 0,
        "mismatched": 0,
        "missing_in_2b": 0,
        "extras_in_2b": 0,
        "ocr_low_conf_pages": 0,
        "job_time_ms": 0,
    }

