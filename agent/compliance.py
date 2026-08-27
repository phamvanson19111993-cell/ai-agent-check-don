"""Bộ kiểm tra tuân thủ quảng cáo thực phẩm bảo vệ sức khoẻ.

Dùng được độc lập, không cần API key:
    python -m agent.cli check duong-dan-file.md
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from . import kb


def _norm(text: str) -> str:
    """Chuẩn hoá để so khớp: NFC + chữ thường + gộp khoảng trắng."""
    text = unicodedata.normalize("NFC", text).lower()
    return re.sub(r"\s+", " ", text)


def _mask_allowed(norm_line: str, rules: dict) -> str:
    """Che các cụm hợp lệ (khuyến cáo bắt buộc, lời khuyên đi khám...) trước khi soát từ cấm."""
    out = norm_line
    for phrase in rules.get("ngoai_le_khong_tinh_la_vi_pham", []):
        needle = _norm(phrase)
        if needle:
            out = out.replace(needle, " " * len(needle))
    return out


@dataclass
class Issue:
    """Một lỗi tuân thủ được phát hiện."""

    muc_do: str  # "chan" (chặn đăng) hoặc "canh_bao"
    loai: str
    chi_tiet: str
    dong: int | None = None
    goi_y: str | None = None

    def __str__(self) -> str:
        vi_tri = f" (dòng {self.dong})" if self.dong else ""
        goi_y = f" -> {self.goi_y}" if self.goi_y else ""
        return f"[{self.muc_do.upper()}] {self.loai}{vi_tri}: {self.chi_tiet}{goi_y}"


@dataclass
class Report:
    dat: bool = True
    issues: list[Issue] = field(default_factory=list)

    @property
    def blocking(self) -> list[Issue]:
        return [i for i in self.issues if i.muc_do == "chan"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.muc_do == "canh_bao"]

    def to_text(self) -> str:
        if not self.issues:
            return "Không phát hiện lỗi tuân thủ. Vẫn nên đọc lại bằng mắt trước khi đăng."
        lines = [str(i) for i in self.issues]
        lines.append("")
        lines.append(
            f"Tổng: {len(self.blocking)} lỗi chặn đăng, {len(self.warnings)} cảnh báo."
        )
        return "\n".join(lines)

    def to_prompt_feedback(self) -> str:
        """Định dạng lỗi để gửi lại cho model tự sửa."""
        lines = ["Kịch bản vừa rồi có các lỗi tuân thủ sau, hãy sửa lại:"]
        for i in self.issues:
            fix = f" Thay bằng: {i.goi_y}." if i.goi_y else ""
            lines.append(f"- {i.loai}: {i.chi_tiet}.{fix}")
        lines.append(
            "Giữ nguyên cấu trúc, độ dài và giọng văn. Chỉ sửa đúng những chỗ vi phạm, "
            "rồi in lại TOÀN BỘ kịch bản đã sửa."
        )
        return "\n".join(lines)


# Những cụm gợi ý cam kết thời gian kiểu "hết đau sau 3 ngày"
_TIME_PROMISE = re.compile(
    r"\b(khỏi|hết|dứt|tan|biến mất|không còn)\b[^.!?\n]{0,40}?"
    r"\b(sau|trong|chỉ)\b[^.!?\n]{0,15}?\d+\s*(ngày|tuần|tháng|liệu trình|hộp)",
)

# Nhân viên y tế đứng ra quảng cáo
# Chỉ tính là vi phạm khi lời chứng thực nhắm vào SẢN PHẨM.
# "bác sĩ kê thuốc", "hỏi ý kiến bác sĩ" là câu hợp lệ, không được bắt nhầm.
_MEDICAL_ENDORSE = re.compile(
    r"(bác sĩ|dược sĩ|y tá|điều dưỡng|bệnh viện|phòng khám|chuyên gia y tế)"
    r"[^.!?\n]{0,30}?(khuyên dùng|khuyến cáo dùng|tin dùng|chứng nhận|"
    r"kê đơn sản phẩm|kê sản phẩm|giới thiệu sản phẩm|đảm bảo chất lượng)"
    r"|sản phẩm[^.!?\n]{0,25}?(bác sĩ|dược sĩ|bệnh viện|phòng khám)"
    r"[^.!?\n]{0,15}?(kê đơn|khuyên dùng|tin dùng|giới thiệu|chứng nhận)"
)

_ABSOLUTE = re.compile(r"\b(100%|tuyệt đối|chắc chắn khỏi|hoàn toàn khỏi|vĩnh viễn)\b")


def check(text: str, *, yeu_cau_khuyen_cao: bool = True) -> Report:
    """Soát một kịch bản và trả về báo cáo tuân thủ."""
    rules = kb.compliance()
    report = Report()
    lines = text.splitlines()
    norm_lines = [_norm(line) for line in lines]
    norm_full = _norm(text)
    # Bản đã che các cụm hợp lệ - chỉ dùng cho bước soát từ cấm, vì bản thân câu
    # khuyến cáo bắt buộc cũng chứa những từ nằm trong danh sách cấm.
    masked_lines = [_mask_allowed(line, rules) for line in norm_lines]

    # 1. Từ cấm
    for pair in rules["tu_cam_va_tu_thay_the"]:
        needle = _norm(pair["cam"])
        for idx, line in enumerate(masked_lines, start=1):
            if needle in line:
                report.issues.append(
                    Issue(
                        muc_do="chan",
                        loai="Từ ngữ vi phạm",
                        chi_tiet=f'dùng cụm "{pair["cam"]}"',
                        dong=idx,
                        goi_y=pair["thay_bang"],
                    )
                )

    # 1b. Các mẫu chỉ vi phạm khi đúng ngữ cảnh (tự xưng số 1, tốt nhất, duy nhất)
    for rule in rules.get("mau_cam_regex", []):
        pattern = re.compile(rule["mau"])
        for idx, line in enumerate(masked_lines, start=1):
            if pattern.search(line):
                report.issues.append(
                    Issue(
                        muc_do="chan",
                        loai=f'So sánh tuyệt đối - {rule["ten"]}',
                        chi_tiet=lines[idx - 1].strip()[:90],
                        dong=idx,
                        goi_y=rule["thay_bang"],
                    )
                )

    # 1c. Các cụm đang bị TẠM KHOÁ vì chưa xác minh (không sai luật, chỉ chưa đủ căn cứ)
    for khoa in rules.get("khoa_tam_thoi", []):
        for cum in khoa["cum_bi_khoa"]:
            needle = _norm(cum)
            for idx, line in enumerate(norm_lines, start=1):
                if needle in line:
                    report.issues.append(
                        Issue(
                            muc_do="chan",
                            loai=f'Đang tạm khoá - {khoa["ten"]}',
                            chi_tiet=f'dùng cụm "{cum}" ({khoa["ly_do"]})',
                            dong=idx,
                            goi_y=khoa["thay_bang"],
                        )
                    )

    # 2. Câu khuyến cáo bắt buộc
    if yeu_cau_khuyen_cao:
        disclaimer = _norm(rules["cau_bat_buoc"]["khuyen_cao"])
        # So khớp nới lỏng: chấp nhận thiếu dấu chấm hoặc viết hoa khác
        if disclaimer.rstrip(".") not in norm_full.replace("!", "."):
            report.issues.append(
                Issue(
                    muc_do="chan",
                    loai="Thiếu khuyến cáo bắt buộc",
                    chi_tiet="chưa có câu khuyến cáo theo quy định",
                    goi_y=rules["cau_bat_buoc"]["khuyen_cao"],
                )
            )

    # 3. Cam kết thời gian
    for idx, line in enumerate(norm_lines, start=1):
        if _TIME_PROMISE.search(line):
            report.issues.append(
                Issue(
                    muc_do="chan",
                    loai="Cam kết kết quả theo thời gian",
                    chi_tiet=lines[idx - 1].strip()[:90],
                    dong=idx,
                    goi_y="thời gian cảm nhận khác nhau ở mỗi người",
                )
            )
        if _MEDICAL_ENDORSE.search(line):
            report.issues.append(
                Issue(
                    muc_do="chan",
                    loai="Dùng danh nghĩa nhân viên/cơ sở y tế",
                    chi_tiet=lines[idx - 1].strip()[:90],
                    dong=idx,
                    goi_y="bỏ hẳn, thay bằng lời khuyên chung về việc đi khám",
                )
            )
        if _ABSOLUTE.search(line):
            report.issues.append(
                Issue(
                    muc_do="canh_bao",
                    loai="Khẳng định tuyệt đối",
                    chi_tiet=lines[idx - 1].strip()[:90],
                    dong=idx,
                    goi_y="diễn đạt chừng mực hơn",
                )
            )

    # 4. Nhắc nhở mềm: nên có lưu ý hiệu quả tuỳ cơ địa khi có lời chứng thực
    if any(k in norm_full for k in ("chia sẻ của", "phản hồi của", "khách hàng kể")):
        if "cơ địa" not in norm_full:
            report.issues.append(
                Issue(
                    muc_do="canh_bao",
                    loai="Lời chứng thực thiếu lưu ý",
                    chi_tiet="có lời kể của người dùng nhưng chưa nhắc hiệu quả tuỳ cơ địa",
                    goi_y="thêm dòng chữ: Hiệu quả tuỳ thuộc cơ địa từng người",
                )
            )

    report.dat = not report.blocking
    return report
