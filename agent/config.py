"""Cấu hình chung cho agent."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
OUTPUT_DIR = Path(os.environ.get("KICHBAN_OUTPUT_DIR", ROOT / "output"))

# Model mặc định. Xem thêm: https://docs.anthropic.com/en/docs/about-claude/models
MODEL = os.environ.get("KICHBAN_MODEL", "claude-opus-5")

# Số token tối đa cho một kịch bản. Dùng streaming nên có thể để rộng rãi.
MAX_TOKENS = int(os.environ.get("KICHBAN_MAX_TOKENS", "16000"))

# Mức effort suy luận: low | medium | high | xhigh | max
EFFORT = os.environ.get("KICHBAN_EFFORT", "high")

# Beta cho phép server tự chuyển sang model dự phòng nếu request bị từ chối.
# Nội dung sức khoẻ đôi khi chạm ngưỡng an toàn nên bật mặc định cho ổn định.
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# Giọng thương hiệu - sửa tại đây để đổi phong cách toàn bộ kịch bản.
BRAND_VOICE = os.environ.get(
    "KICHBAN_BRAND_VOICE",
    "Ấm áp, tử tế, nói chuyện như người thân trong nhà. "
    "Câu ngắn, không dùng từ chuyên môn nếu chưa giải thích. "
    "Không doạ nạt, không thổi phồng, không hứa hẹn.",
)
