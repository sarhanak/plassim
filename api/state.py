from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from uuid import uuid4

from models.schemas import PurchaseInvoice, GSTR2BRow, ReconResult, SalesRow


def gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass
class Dataset:
    dataset_id: str
    client_id: Optional[str] = None
    mapping: dict = field(default_factory=dict)
    purchases: List[PurchaseInvoice] = field(default_factory=list)


@dataclass
class TwoB:
    two_b_id: str
    rows: List[GSTR2BRow] = field(default_factory=list)


@dataclass
class Sales:
    sales_id: str
    rows: List[SalesRow] = field(default_factory=list)


@dataclass
class ReconJob:
    dataset_id: str
    two_b_id: str
    results: List[ReconResult] = field(default_factory=list)
    counts: dict = field(default_factory=dict)


DATASETS: Dict[str, Dataset] = {}
TWO_B: Dict[str, TwoB] = {}
SALES: Dict[str, Sales] = {}
RECONS: Dict[str, ReconJob] = {}

