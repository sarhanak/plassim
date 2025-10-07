from __future__ import annotations

import io
import os
from typing import Tuple
from minio import Minio


def get_minio() -> Minio:
    endpoint = os.getenv("S3_ENDPOINT", "http://localhost:9000").replace("http://", "").replace("https://", "")
    access_key = os.getenv("S3_ACCESS_KEY", "minio")
    secret_key = os.getenv("S3_SECRET_KEY", "minio123")
    secure = os.getenv("S3_ENDPOINT", "http://localhost:9000").startswith("https://")
    return Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)


def put_bytes(bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    mc = get_minio()
    found = mc.bucket_exists(bucket)
    if not found:
        mc.make_bucket(bucket)
    mc.put_object(bucket, key, io.BytesIO(data), length=len(data), content_type=content_type)
    return f"s3://{bucket}/{key}"


def presign(bucket: str, key: str, days: int = 1) -> str:
    mc = get_minio()
    return mc.presigned_get_object(bucket, key)

