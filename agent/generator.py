"""Gọi Claude API để sinh kịch bản, kèm vòng tự sửa lỗi tuân thủ."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from . import compliance, prompts
from .config import EFFORT, FALLBACK_BETA, MAX_TOKENS, MODEL


@dataclass
class Result:
    """Kết quả sinh kịch bản."""

    text: str
    report: compliance.Report
    so_lan_sua: int = 0
    model: str = MODEL
    usage: dict[str, Any] = field(default_factory=dict)
    tu_choi: str | None = None  # lý do nếu model từ chối trả lời


def _client():
    try:
        import anthropic
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Chưa cài thư viện anthropic. Chạy: pip install -r requirements.txt"
        ) from exc
    # Tự lấy khoá theo thứ tự: ANTHROPIC_API_KEY -> ANTHROPIC_AUTH_TOKEN -> hồ sơ `ant auth login`
    return anthropic.Anthropic()


def _call(client, system: str, messages: list[dict[str, Any]], *, dung_fallback: bool = True):
    """Một lượt gọi model. Dùng streaming vì kịch bản có thể dài."""
    import anthropic

    system_blocks = [
        # Đánh dấu cache: phần system giữ nguyên giữa các lần gọi nên tái sử dụng được.
        {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
    ]
    kwargs: dict[str, Any] = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "system": system_blocks,
        "messages": messages,
        "thinking": {"type": "adaptive"},
        "output_config": {"effort": EFFORT},
    }

    if dung_fallback:
        try:
            with client.beta.messages.stream(
                **kwargs, betas=[FALLBACK_BETA], fallbacks="default"
            ) as stream:
                return stream.get_final_message()
        except (anthropic.BadRequestError, TypeError):
            # Tài khoản chưa bật beta dự phòng - gọi lại bằng endpoint thường.
            pass

    with client.messages.stream(**kwargs) as stream:
        return stream.get_final_message()


def _text_of(message) -> str:
    return "\n".join(b.text for b in message.content if b.type == "text").strip()


def _usage_of(message) -> dict[str, Any]:
    u = getattr(message, "usage", None)
    if u is None:
        return {}
    return {
        "input_tokens": getattr(u, "input_tokens", None),
        "output_tokens": getattr(u, "output_tokens", None),
        "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", None),
    }


def generate(
    *,
    symptom_key: str,
    persona_key: str,
    format_key: str,
    platform: str = "tiktok",
    duration: int | None = None,
    product_keys: list[str] | None = None,
    extra: str | None = None,
    max_fix: int = 2,
) -> Result:
    """Sinh một kịch bản và tự sửa cho tới khi qua được bộ kiểm tra tuân thủ."""
    import anthropic

    system = prompts.build_system()
    brief = prompts.build_brief(
        symptom_key=symptom_key,
        persona_key=persona_key,
        format_key=format_key,
        platform=platform,
        duration=duration,
        product_keys=product_keys,
        extra=extra,
    )

    client = _client()
    messages: list[dict[str, Any]] = [{"role": "user", "content": brief}]

    try:
        message = _call(client, system, messages)
    except anthropic.AuthenticationError as exc:
        raise SystemExit(
            "Chưa có khoá API. Hãy đặt biến môi trường ANTHROPIC_API_KEY "
            "hoặc đăng nhập bằng `ant auth login`."
        ) from exc
    except anthropic.RateLimitError as exc:
        raise SystemExit("Bị giới hạn tốc độ gọi API, thử lại sau ít phút.") from exc
    except anthropic.APIConnectionError as exc:
        raise SystemExit(f"Không kết nối được tới API: {exc}") from exc
    except anthropic.APIStatusError as exc:
        raise SystemExit(f"API trả về lỗi {exc.status_code}: {exc}") from exc

    if getattr(message, "stop_reason", None) == "refusal":
        detail = getattr(message, "stop_details", None)
        return Result(
            text="",
            report=compliance.Report(dat=False),
            model=MODEL,
            usage=_usage_of(message),
            tu_choi=getattr(detail, "explanation", "Model từ chối tạo nội dung này."),
        )

    text = _text_of(message)
    report = compliance.check(text)
    usage = _usage_of(message)
    lan_sua = 0

    while not report.dat and lan_sua < max_fix:
        lan_sua += 1
        messages += [
            {"role": "assistant", "content": text},
            {"role": "user", "content": report.to_prompt_feedback()},
        ]
        message = _call(client, system, messages)
        if getattr(message, "stop_reason", None) == "refusal":
            break
        text = _text_of(message)
        report = compliance.check(text)
        for k, v in _usage_of(message).items():
            if isinstance(v, int) and isinstance(usage.get(k), int):
                usage[k] += v

    return Result(text=text, report=report, so_lan_sua=lan_sua, model=MODEL, usage=usage)
