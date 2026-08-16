"""Tầng đánh giá bằng Claude cho những file mà quy tắc cứng không kết luận được.

Nguyên tắc riêng tư: chỉ gửi *metadata* (đường dẫn, tên, kích thước, tuổi file).
Không bao giờ đọc hay gửi nội dung file.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .config import AIConfig
from .scanner import Candidate

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
Bạn là bộ phân loại file rác cho một công cụ dọn dẹp máy tính chạy tự động.

Với mỗi file, bạn chỉ nhận được metadata: đường dẫn, tên, phần mở rộng, kích \
thước và số ngày kể từ lần sửa cuối. Bạn KHÔNG thấy nội dung file.

Phân loại mỗi file vào một trong ba nhóm:
- "junk": gần như chắc chắn là rác tái tạo được (file tạm, cache, log, bản cài \
  đặt đã dùng xong, file trùng lặp có hậu tố kiểu "(1)").
- "keep": có khả năng là dữ liệu người dùng quan tâm (tài liệu, ảnh, mã nguồn, \
  file cấu hình, sao lưu, bất cứ thứ gì không thể tạo lại).
- "review": không đủ căn cứ để kết luận từ metadata.

Nguyên tắc quyết định: nghi ngờ thì không xoá. Ảnh, video, tài liệu và file có \
tên do người dùng đặt luôn là "keep" hoặc "review", kể cả khi rất cũ — tuổi file \
không phải bằng chứng cho thấy nó là rác. Chỉ chọn "junk" khi bản thân đường dẫn \
và tên file đã cho thấy rõ đó là dữ liệu máy sinh ra.

confidence là số từ 0 đến 1, thể hiện mức độ chắc chắn của bạn.
reason viết bằng tiếng Việt, một câu ngắn.
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "decision": {"type": "string", "enum": ["junk", "keep", "review"]},
                    "confidence": {"type": "number"},
                    "reason": {"type": "string"},
                },
                "required": ["path", "decision", "confidence", "reason"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["decisions"],
    "additionalProperties": False,
}


def _describe(c: Candidate) -> dict:
    return {
        "path": str(c.path),
        "name": c.path.name,
        "ext": c.path.suffix.lower(),
        "size_bytes": c.size,
        "age_days": round(c.age_days, 1),
        "is_dir": c.is_dir,
    }


class Classifier:
    """Gọi Claude để phân loại các ứng viên chưa rõ ràng."""

    def __init__(self, cfg: AIConfig) -> None:
        self.cfg = cfg
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - phụ thuộc tuỳ chọn
                raise RuntimeError(
                    "Cần cài gói `anthropic` để dùng chế độ AI: pip install anthropic"
                ) from exc
            self._client = anthropic.Anthropic()
        return self._client

    def classify(self, candidates: list[Candidate]) -> list[Candidate]:
        """Gán decision/confidence/reason cho từng ứng viên.

        Nếu gọi API thất bại, mọi ứng viên đều rơi về "review" — nghĩa là giữ lại.
        """
        if not candidates:
            return []

        out: list[Candidate] = []
        batch_size = max(1, self.cfg.max_files_per_call)
        for start in range(0, len(candidates), batch_size):
            batch = candidates[start : start + batch_size]
            try:
                verdicts = self._classify_batch(batch)
            except Exception as exc:  # noqa: BLE001 - lỗi nào cũng phải fail-safe
                log.warning("Phân loại bằng AI thất bại, giữ lại toàn bộ: %s", exc)
                verdicts = {}

            for cand in batch:
                v = verdicts.get(str(cand.path))
                if v is None:
                    cand.decision = "review"
                    cand.confidence = 0.0
                    cand.reason = "AI không trả lời cho file này"
                else:
                    cand.decision = v["decision"]
                    cand.confidence = float(v["confidence"])
                    cand.reason = v["reason"]
                out.append(cand)
        return out

    def _classify_batch(self, batch: list[Candidate]) -> dict[str, dict]:
        client = self._get_client()
        payload = json.dumps([_describe(c) for c in batch], ensure_ascii=False, indent=1)

        response = client.messages.create(
            model=self.cfg.model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            output_config={
                "effort": "low",
                "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
            },
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Phân loại các file sau. Trả về đúng một mục cho mỗi file, "
                        "giữ nguyên giá trị `path`.\n\n" + payload
                    ),
                }
            ],
        )

        if response.stop_reason == "refusal":
            raise RuntimeError("Claude từ chối xử lý yêu cầu phân loại")

        text = next((b.text for b in response.content if b.type == "text"), "")
        data = json.loads(text)
        return {d["path"]: d for d in data.get("decisions", [])}


def split_by_decision(
    candidates: list[Candidate], min_confidence: float = 0.8
) -> tuple[list[Candidate], list[Candidate]]:
    """Tách thành (được phép dọn, cần giữ lại) theo kết quả phân loại."""
    cleanable = [
        c for c in candidates if c.decision == "junk" and c.confidence >= min_confidence
    ]
    held = [c for c in candidates if c not in cleanable]
    return cleanable, held


def is_review_root(path: Path, roots: list[Path]) -> bool:
    from .safety import is_within

    return any(is_within(path, r) for r in roots)
