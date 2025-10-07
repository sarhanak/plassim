from __future__ import annotations

import os
from typing import Dict, Any
import cv2
import numpy as np


def preprocess(image_bytes: bytes) -> bytes:
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return image_bytes
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.fastNlMeansDenoising(gray, h=7)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 3)
    _, buff = cv2.imencode('.png', th)
    return bytes(buff)


def run_ocr(image_bytes: bytes) -> Dict[str, Any]:
    try:
        from paddleocr import PaddleOCR  # heavy import
        lang = 'en'
        ocr = PaddleOCR(lang=lang, use_angle_cls=True, show_log=False)
        arr = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        result = ocr.ocr(img, cls=True)
        mean_conf = 0.0
        words = []
        n = 0
        for line in result:
            for box, (txt, conf) in line:
                words.append({"text": txt, "conf": float(conf), "bbox": box})
                mean_conf += float(conf)
                n += 1
        mean_conf = mean_conf / max(1, n)
        return {"mean_conf": mean_conf, "words": words}
    except Exception as e:
        return {"error": str(e)}


def extract_key_fields(ocr_result: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder extraction: a real implementation would use regex and layout heuristics
    return {
        "supplier_gstin": None,
        "invoice_no": None,
        "invoice_date": None,
        "taxable": None,
        "igst": None,
        "cgst": None,
        "sgst": None,
        "total": None,
        "doc_type": "INV",
    }


def ocr_fallback(image_bytes: bytes) -> Dict[str, Any]:
    processed = preprocess(image_bytes)
    res = run_ocr(processed)
    mean = res.get("mean_conf", 0.0)
    low_conf = mean < 0.65
    fields = extract_key_fields(res)
    return {"low_confidence": low_conf, "mean_conf": mean, "fields": fields, "provenance": res.get("words", [])}

