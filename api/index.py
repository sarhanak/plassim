import os

# On Vercel, avoid importing heavy OCR deps
os.environ.setdefault("OCR_FALLBACK", "false")

from .main import app as app  # noqa: E402

