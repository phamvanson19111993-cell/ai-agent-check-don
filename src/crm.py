"""Thao tác với Cơ hội (crm.lead) trên Odoo — tương ứng màn hình
'Cơ hội đang hoạt động' (/odoo/cohoidanghoatdongs)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .odoo_client import OdooClient

MODEL = "crm.lead"

# Domain của màn hình 'Cơ hội đang hoạt động':
# là opportunity, đang active (chưa lưu trữ / chưa mất).
ACTIVE_OPP_DOMAIN: List[Any] = [
    ("type", "=", "opportunity"),
    ("active", "=", True),
]

DEFAULT_FIELDS = [
    "id",
    "name",
    "partner_id",
    "stage_id",
    "expected_revenue",
    "probability",
    "phone",
    "email_from",
    "user_id",
    "date_deadline",
]


class CrmService:
    """Nghiệp vụ đọc/tạo/cập nhật Cơ hội."""

    def __init__(self, client: OdooClient):
        self.client = client

    def list_active_opportunities(
        self,
        extra_domain: Optional[List[Any]] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Lấy danh sách cơ hội đang hoạt động."""
        domain = list(ACTIVE_OPP_DOMAIN) + list(extra_domain or [])
        return self.client.search_read(
            MODEL,
            domain=domain,
            fields=fields or DEFAULT_FIELDS,
            limit=limit,
            order="create_date desc",
        )

    def count_active_opportunities(self) -> int:
        return self.client.search_count(MODEL, ACTIVE_OPP_DOMAIN)

    def find_by_ref(self, ref: str, ref_field: str = "name") -> List[Dict[str, Any]]:
        """Tìm cơ hội theo một mã/tên tham chiếu (mặc định theo 'name')."""
        domain = list(ACTIVE_OPP_DOMAIN) + [(ref_field, "=", ref)]
        return self.client.search_read(MODEL, domain=domain, fields=DEFAULT_FIELDS)

    def create_opportunity(self, values: Dict[str, Any]) -> int:
        """Tạo mới một cơ hội. `values` là dict field->value của crm.lead."""
        payload = {"type": "opportunity", **values}
        return self.client.create(MODEL, payload)

    def update_opportunity(self, opp_id: int, values: Dict[str, Any]) -> bool:
        """Cập nhật một cơ hội theo id."""
        return self.client.write(MODEL, [opp_id], values)

    def upsert_by_ref(
        self,
        ref: str,
        values: Dict[str, Any],
        ref_field: str = "name",
    ) -> Dict[str, Any]:
        """Có thì cập nhật, chưa có thì tạo mới — khớp theo `ref_field`.

        Trả về {'action': 'created'|'updated', 'id': <id>}.
        """
        existing = self.find_by_ref(ref, ref_field=ref_field)
        if existing:
            opp_id = existing[0]["id"]
            self.update_opportunity(opp_id, values)
            return {"action": "updated", "id": opp_id}
        opp_id = self.create_opportunity({ref_field: ref, **values})
        return {"action": "created", "id": opp_id}
