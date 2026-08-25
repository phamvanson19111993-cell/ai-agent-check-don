"""Client kết nối Odoo qua JSON-RPC.

Hỗ trợ 2 chế độ:
  * Đăng nhập bằng user + password/API key  -> gọi endpoint /jsonrpc (external API)
  * Dùng cookie session_id sẵn có           -> gọi endpoint /web/dataset/call_kw
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Sequence

import requests

from .config import OdooConfig


class OdooError(RuntimeError):
    """Lỗi trả về từ Odoo hoặc lỗi kết nối."""


class OdooClient:
    """Bao bọc các thao tác ORM (search_read/create/write...) của Odoo."""

    def __init__(self, config: OdooConfig, session: Optional[requests.Session] = None):
        config.validate()
        self.config = config
        self.uid: Optional[int] = None
        self._session = session or requests.Session()
        if config.uses_session:
            self._session.cookies.set("session_id", config.session_id)

    # ------------------------------------------------------------------ #
    # Tầng vận chuyển JSON-RPC + retry
    # ------------------------------------------------------------------ #
    def _post(self, path: str, payload: Dict[str, Any]) -> Any:
        url = f"{self.config.url}{path}"
        last_exc: Optional[Exception] = None
        for attempt in range(self.config.max_retries):
            try:
                resp = self._session.post(
                    url, json=payload, timeout=self.config.timeout
                )
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    err = data["error"]
                    message = err.get("message", "Lỗi không xác định")
                    detail = (err.get("data") or {}).get("message", "")
                    raise OdooError(f"{message}: {detail}".strip(": "))
                return data.get("result")
            except (requests.ConnectionError, requests.Timeout) as exc:
                # Chỉ retry với lỗi mạng, backoff luỹ thừa 2s,4s,8s,16s
                last_exc = exc
                if attempt < self.config.max_retries - 1:
                    time.sleep(2 ** (attempt + 1))
                    continue
                raise OdooError(f"Lỗi mạng tới Odoo: {exc}") from exc
        raise OdooError(f"Không kết nối được Odoo: {last_exc}")

    # ------------------------------------------------------------------ #
    # Xác thực
    # ------------------------------------------------------------------ #
    def authenticate(self) -> int:
        """Đăng nhập lấy uid (chế độ user/pass). Chế độ session trả uid=0."""
        if self.config.uses_session:
            self.uid = 0
            return self.uid
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [
                    self.config.db,
                    self.config.username,
                    self.config.password,
                    {},
                ],
            },
        }
        uid = self._post("/jsonrpc", payload)
        if not uid:
            raise OdooError(
                "Đăng nhập thất bại — kiểm tra ODOO_DB/USERNAME/PASSWORD."
            )
        self.uid = int(uid)
        return self.uid

    # ------------------------------------------------------------------ #
    # Gọi phương thức model (execute_kw)
    # ------------------------------------------------------------------ #
    def execute_kw(
        self,
        model: str,
        method: str,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Gọi <model>.<method>(*args, **kwargs) trên Odoo."""
        args = list(args or [])
        kwargs = dict(kwargs or {})

        if self.config.uses_session:
            payload = {
                "jsonrpc": "2.0",
                "method": "call",
                "params": {
                    "model": model,
                    "method": method,
                    "args": args,
                    "kwargs": kwargs,
                },
            }
            return self._post("/web/dataset/call_kw", payload)

        if self.uid is None:
            self.authenticate()
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.config.db,
                    self.uid,
                    self.config.password,
                    model,
                    method,
                    args,
                    kwargs,
                ],
            },
        }
        return self._post("/jsonrpc", payload)

    # ------------------------------------------------------------------ #
    # Tiện ích ORM cấp cao
    # ------------------------------------------------------------------ #
    def search_read(
        self,
        model: str,
        domain: Optional[List[Any]] = None,
        fields: Optional[List[str]] = None,
        limit: Optional[int] = None,
        order: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        kwargs: Dict[str, Any] = {"fields": fields or []}
        if limit is not None:
            kwargs["limit"] = limit
        if order:
            kwargs["order"] = order
        return self.execute_kw(model, "search_read", [domain or []], kwargs)

    def create(self, model: str, values: Dict[str, Any]) -> int:
        return self.execute_kw(model, "create", [values])

    def write(self, model: str, ids: Sequence[int], values: Dict[str, Any]) -> bool:
        return self.execute_kw(model, "write", [list(ids), values])

    def search_count(self, model: str, domain: Optional[List[Any]] = None) -> int:
        return self.execute_kw(model, "search_count", [domain or []])
