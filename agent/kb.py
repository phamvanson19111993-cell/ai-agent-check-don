"""Đọc và tra cứu kho kiến thức trong thư mục knowledge/."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from .config import KNOWLEDGE_DIR


@lru_cache(maxsize=None)
def load(name: str) -> dict[str, Any]:
    """Đọc một file JSON trong knowledge/ (không cần đuôi .json)."""
    path = KNOWLEDGE_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy kho kiến thức: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def products() -> list[dict[str, Any]]:
    return load("products")["san_pham"]


def combo() -> dict[str, Any]:
    return load("products")["bo_ba"]


def symptoms() -> list[dict[str, Any]]:
    return load("symptoms")["trieu_chung"]


def red_flags() -> dict[str, Any]:
    return load("symptoms")["dau_hieu_can_di_kham_ngay"]


def personas() -> list[dict[str, Any]]:
    return load("personas")["chan_dung_khach_hang"]


def formats() -> list[dict[str, Any]]:
    return load("formats")["dinh_dang"]


def compliance() -> dict[str, Any]:
    return load("compliance")


def hooks() -> dict[str, Any]:
    return load("hooks")


def ctas() -> dict[str, Any]:
    return load("ctas")


def _pick(items: list[dict[str, Any]], key: str, label: str) -> dict[str, Any]:
    for item in items:
        if item["id"] == key:
            return item
    available = ", ".join(i["id"] for i in items)
    raise KeyError(f"Không có {label} '{key}'. Các lựa chọn: {available}")


def get_symptom(key: str) -> dict[str, Any]:
    return _pick(symptoms(), key, "triệu chứng")


def get_persona(key: str) -> dict[str, Any]:
    return _pick(personas(), key, "chân dung khách hàng")


def get_format(key: str) -> dict[str, Any]:
    return _pick(formats(), key, "định dạng video")


def get_product(key: str) -> dict[str, Any]:
    return _pick(products(), key, "sản phẩm")


def products_for_symptom(symptom_key: str) -> list[dict[str, Any]]:
    """Các sản phẩm liên quan tới một triệu chứng, theo đúng thứ tự ưu tiên đã khai báo."""
    ids = get_symptom(symptom_key)["san_pham_lien_quan"]
    return [get_product(pid) for pid in ids]


def hooks_for(symptom_key: str) -> list[dict[str, Any]]:
    """Hook hợp với triệu chứng, cộng thêm các hook dùng chung."""
    return [h for h in hooks()["mau_hook"] if h["trieu_chung"] in (symptom_key, "chung")]
