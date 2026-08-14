# -*- coding: utf-8 -*-
"""Bot Telegram "check trùng đơn" — DiLi Supplement.

Luồng hoạt động:
- Nhận SĐT từ (a) tin nhắn Telegram gửi cho bot / trong nhóm có bot, hoặc
  (b) cổng HTTP nội bộ do userscript Tampermonkey bắn sang từ Messenger.
- Dò số trong Google Sheet (tất cả các tab đã cấu hình), báo cáo lên nhóm REPORT_CHAT_ID.
- Tin nhắn không chứa số → bot im lặng. Bot không bao giờ tự trả lời ai ngoài báo cáo.

Lệnh: /id (lấy chat id) · /check <số> (kiểm tra tay) · /reload (nạp lại Sheet)
"""
from __future__ import annotations

import asyncio
import logging
import time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import config
from intake_server import start_intake_server
from phone_utils import extract_phones, normalize
from report import build_report
from sheet_store import store

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("dili-bot")

# Báo lỗi đọc Sheet lên Telegram tối đa 1 lần / 30 phút (tránh spam nhóm)
_ERROR_COOLDOWN = 30 * 60
_last_error_sent = 0.0


# ---------------------------------------------------------------- gửi báo cáo

async def send_report(bot, text: str, fallback_chat_id=None) -> None:
    chat_id = config.REPORT_CHAT_ID or fallback_chat_id
    if not chat_id:
        log.warning("Chưa có REPORT_CHAT_ID — bỏ qua báo cáo:\n%s", text)
        return
    await bot.send_message(chat_id=chat_id, text=text)


async def notify_error(bot, message: str) -> None:
    """Báo lỗi vận hành lên nhóm, có giới hạn tần suất."""
    global _last_error_sent
    now = time.time()
    if now - _last_error_sent < _ERROR_COOLDOWN:
        return
    _last_error_sent = now
    if config.REPORT_CHAT_ID:
        try:
            await bot.send_message(
                chat_id=config.REPORT_CHAT_ID, text=f"🛑 Lỗi bot: {message}"
            )
        except Exception:  # noqa: BLE001
            log.exception("Không gửi được thông báo lỗi lên Telegram")


async def process_phone(app: Application, key: str, source: str, fallback_chat_id=None,
                        force: bool = False) -> str:
    """Tra 1 số và gửi báo cáo. Trả về nội dung báo cáo (để /check dùng lại)."""
    if not force and store.recently_reported(key):
        log.info("Bỏ qua số %s (vừa báo trong %s phút)", key, config.DEDUP_TTL_MIN)
        return ""
    text = build_report(key, store.lookup(key))
    await send_report(app.bot, text, fallback_chat_id=fallback_chat_id)
    log.info("Đã báo cáo số %s (nguồn: %s)", key, source)
    return text


# ---------------------------------------------------------------- handlers

def _save_report_chat_id(chat_id: int) -> None:
    """Ghi REPORT_CHAT_ID vào file .env để lần sau khởi động vẫn nhớ."""
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    lines: list[str] = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    replaced = False
    for i, line in enumerate(lines):
        if line.strip().startswith("REPORT_CHAT_ID="):
            lines[i] = f"REPORT_CHAT_ID={chat_id}"
            replaced = True
            break
    if not replaced:
        lines.append(f"REPORT_CHAT_ID={chat_id}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    is_group = chat.type != "private"
    text = f"🆔 Chat ID của {'nhóm' if is_group else 'chat'} này là:\n`{chat.id}`"

    # Chưa cấu hình nơi nhận báo cáo + gõ /id trong NHÓM → tự nhận nhóm này luôn
    if is_group and not config.REPORT_CHAT_ID:
        config.REPORT_CHAT_ID = str(chat.id)
        try:
            _save_report_chat_id(chat.id)
            text += "\n\n✅ Đã TỰ ĐỘNG chọn nhóm này làm nơi nhận báo cáo (đã lưu vào .env). Không cần làm gì thêm!"
        except Exception as e:  # noqa: BLE001
            log.error("Không ghi được .env: %s", e)
            text += f"\n\n⚠️ Đã dùng nhóm này làm nơi nhận báo cáo, nhưng không ghi được vào .env ({e}) — hãy điền tay REPORT_CHAT_ID={chat.id}"
    else:
        text += "\n\nDán số này vào REPORT_CHAT_ID trong file .env rồi khởi động lại bot."

    await update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def cmd_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    raw = " ".join(context.args) if context.args else ""
    key = normalize(raw) or (extract_phones(raw)[0] if extract_phones(raw) else None)
    if not key:
        await msg.reply_text("Cách dùng: /check 0976486366")
        return
    if not store.loaded:
        await msg.reply_text("⏳ Sheet chưa nạp xong, thử lại sau ít giây hoặc gõ /reload.")
        return
    text = build_report(key, store.lookup(key))
    # /check là kiểm tra tay → trả lời ngay tại chỗ gõ lệnh
    await msg.reply_text(text)


async def cmd_reload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    try:
        rows, tabs = await asyncio.to_thread(store.load)
        note = f"\n(⚠️ một phần tab lỗi: {store.last_error})" if store.last_error else ""
        await msg.reply_text(f"🔄 Đã nạp lại Sheet: {rows} dòng / {tabs} tab.{note}")
    except Exception as e:  # noqa: BLE001
        await msg.reply_text(f"🛑 Nạp lại Sheet thất bại: {e}")


async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bắt SĐT trong mọi tin nhắn văn bản. Không có số → im lặng tuyệt đối."""
    msg = update.effective_message
    if not msg or not (msg.text or msg.caption):
        return
    phones = extract_phones(msg.text or msg.caption)
    if not phones:
        return
    if not store.loaded:
        await notify_error(context.bot, "Nhận được số nhưng Sheet chưa nạp được.")
        return
    for key in phones:
        await process_phone(context.application, key, source="telegram",
                            fallback_chat_id=msg.chat_id)


# ---------------------------------------------------------------- jobs

async def job_reload(context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        rows, tabs = await asyncio.to_thread(store.load)
        log.info("Tự nạp lại Sheet: %d dòng / %d tab", rows, tabs)
        if store.last_error:
            await notify_error(context.bot, f"Một phần tab đọc lỗi: {store.last_error}")
    except Exception as e:  # noqa: BLE001
        log.error("Tự nạp lại Sheet lỗi: %s", e)
        await notify_error(context.bot, f"Đọc Sheet lỗi: {e}")


async def job_heartbeat(context: ContextTypes.DEFAULT_TYPE) -> None:
    if config.REPORT_CHAT_ID:
        await context.bot.send_message(
            chat_id=config.REPORT_CHAT_ID,
            text=f"💓 Bot vẫn đang chạy · Sheet: {store.row_count} dòng / {store.tab_count} tab",
        )


# ---------------------------------------------------------------- khởi động

async def post_init(app: Application) -> None:
    # 1) Nạp Sheet lần đầu (không chặn bot nếu lỗi — job định kỳ sẽ thử lại)
    try:
        rows, tabs = await asyncio.to_thread(store.load)
        log.info("Nạp Sheet lần đầu: %d dòng / %d tab", rows, tabs)
    except Exception as e:  # noqa: BLE001
        log.error("Nạp Sheet lần đầu thất bại: %s", e)
        await notify_error(app.bot, f"Khởi động: đọc Sheet lỗi — {e}. Bot sẽ tự thử lại.")

    # 2) Mở cổng HTTP nhận số từ userscript
    async def _process(key: str, source: str) -> None:
        await process_phone(app, key, source=source)

    app.bot_data["intake_runner"] = await start_intake_server(_process)

    # 3) Báo "đã bật" lên nhóm
    if config.REPORT_CHAT_ID:
        try:
            await app.bot.send_message(
                chat_id=config.REPORT_CHAT_ID,
                text=f"✅ Bot đã BẬT · Sheet: {store.row_count} dòng / {store.tab_count} tab",
            )
        except Exception as e:  # noqa: BLE001
            log.error(
                "Không gửi được tin 'Bot đã BẬT' (kiểm tra REPORT_CHAT_ID và bot đã ở trong nhóm chưa): %s", e
            )
    else:
        log.warning("REPORT_CHAT_ID trống — thêm bot vào nhóm, gõ /id để lấy rồi điền vào .env")


async def post_shutdown(app: Application) -> None:
    runner = app.bot_data.get("intake_runner")
    if runner:
        await runner.cleanup()


def main() -> None:
    if not config.BOT_TOKEN:
        raise SystemExit("Thiếu BOT_TOKEN trong file .env — điền token từ @BotFather rồi chạy lại.")

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(CommandHandler("check", cmd_check))
    app.add_handler(CommandHandler("reload", cmd_reload))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    if config.RELOAD_MINUTES > 0:
        app.job_queue.run_repeating(
            job_reload, interval=config.RELOAD_MINUTES * 60, first=config.RELOAD_MINUTES * 60
        )
    if config.HEARTBEAT_HOURS > 0:
        app.job_queue.run_repeating(
            job_heartbeat, interval=config.HEARTBEAT_HOURS * 3600, first=config.HEARTBEAT_HOURS * 3600
        )

    log.info("Bot đang chạy (polling)... Ctrl+C để dừng.")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
