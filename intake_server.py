# -*- coding: utf-8 -*-
"""Cổng HTTP nội bộ (mặc định 127.0.0.1:8787) nhận số từ userscript Tampermonkey.

POST /intake
  Header:  X-Intake-Secret: <INTAKE_SECRET>   (hoặc trường "secret" trong JSON)
  Body:    {"text": "..."}  hoặc  {"phone": "0976486366"}
GET /health → {"ok": true}
"""
import hmac
import logging

from aiohttp import web

import config
from phone_utils import extract_phones, normalize

log = logging.getLogger(__name__)


def _secret_ok(request: web.Request, data: dict) -> bool:
    if not config.INTAKE_SECRET:
        return False  # bắt buộc phải đặt INTAKE_SECRET mới mở cổng
    got = request.headers.get("X-Intake-Secret", "") or str(data.get("secret", ""))
    return hmac.compare_digest(got, config.INTAKE_SECRET)


async def start_intake_server(process_phone) -> web.AppRunner | None:
    """process_phone: coroutine nhận (key: str, source: str) để xử lý và gửi báo cáo."""
    if not config.INTAKE_SECRET:
        log.warning("INTAKE_SECRET trống — KHÔNG mở cổng HTTP nhận số (an toàn).")
        return None

    async def intake(request: web.Request) -> web.Response:
        try:
            data = await request.json()
        except Exception:  # noqa: BLE001
            data = {}
        if not _secret_ok(request, data):
            return web.json_response({"ok": False, "error": "bad secret"}, status=403)

        keys: list[str] = []
        if data.get("phone"):
            k = normalize(str(data["phone"]))
            if k:
                keys.append(k)
        if data.get("text"):
            keys.extend(k for k in extract_phones(str(data["text"])) if k not in keys)

        for key in keys:
            await process_phone(key, source="messenger")
        return web.json_response({"ok": True, "received": len(keys)})

    async def health(_: web.Request) -> web.Response:
        return web.json_response({"ok": True})

    app = web.Application()
    app.router.add_post("/intake", intake)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, config.INTAKE_HOST, config.INTAKE_PORT)
    await site.start()
    log.info("Cổng nhận số đang chạy tại http://%s:%d/intake", config.INTAKE_HOST, config.INTAKE_PORT)
    return runner
