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


# File tra cứu (bản thân nó liệt kê từ cấm làm ví dụ) đánh dấu dòng này ở đầu file
# để bộ soát bỏ qua. Chỉ dùng cho tài liệu nội bộ, KHÔNG dùng cho nội dung đem đăng.
BO_QUA_MARKER = "<!-- soat-tuan-thu: bo-qua -->"


# --- Nhận diện dòng THAM CHIẾU (nhắc tới từ cấm để cấm, không phải để dùng) -----------
# Bộ soát càng nghiêm càng đẩy các phòng xoá chính danh sách cấm của mình cho báo cáo xanh.
# Đó là lỗi thiết kế, nên phải phân biệt "dùng từ cấm" với "nhắc từ cấm để cấm".

_ICON_THAM_CHIEU = ("❌", "⛔", "⚠️", "⚠", "🚫", "🔴", "🚨", "‼️")

# Dòng mở đầu một khối liệt kê điều cấm
_TIEU_DE_KHOI_CAM = re.compile(
    r"(không được nói|không được viết|không được|tuyệt đối không|cấm nói|cấm viết|"
    r"những điều cấm|từ cấm|bảng thay từ|không bao giờ|điều cấm|không phải|"
    r"câu cấm|không nên nói|tránh nói|trước khi nói|nên nói)"
)

# Cụm phủ định đứng SAU từ cấm: "Làm tan cục máu đông | công dụng như thuốc" ,
# "Nói X là vi phạm quy định". Không có cụm này thì câu là câu quảng cáo thật.
_PHU_DINH_SAU = re.compile(
    r"^[^.!?\n]{0,60}?(là vi phạm|vi phạm|là sai|sai luật|bị phạt|mức phạt|cấm|"
    r"mất uy tín|thất đức|sai lệch|không được|không nên|nguy hiểm|"
    r"công dụng như thuốc|cam kết y tế|quảng cáo sai)"
)

# Câu hỏi của khách được trích lại, không phải câu khẳng định của người bán
_LA_CAU_HOI = re.compile(r"^[^.!\n]{0,25}\?")

# Cụm phủ định đứng ngay trước từ cấm
_PHU_DINH = re.compile(
    r"(không|đừng|cấm|tránh|thay vì|thay cho|chớ|nghiêm cấm|hạn chế|bỏ|sai|nhầm)"
    r"[^.!?\n]{0,12}$"
)

# Cửa sổ nhìn ngược để tìm phủ định, tính bằng ký tự
_CUA_SO_PHU_DINH = 30


def _la_dong_tham_chieu(line: str) -> bool:
    """Dòng liệt kê điều cấm, không phải dòng nội dung đem đăng."""
    tho = line.strip().lstrip("-*|>#0123456789. \t")
    if tho[:2] in _ICON_THAM_CHIEU or any(tho.startswith(i) for i in _ICON_THAM_CHIEU):
        return True
    return bool(_TIEU_DE_KHOI_CAM.search(_norm(line)))


def _bi_phu_dinh(norm_line: str, vi_tri: int, het: int | None = None) -> bool:
    """Từ cấm nằm trong ngữ cảnh CẤM chứ không phải ngữ cảnh dùng.

    Ba dấu hiệu: phủ định đứng trước ("không hứa chữa khỏi"), phủ định đứng sau
    ("làm tan cục máu đông | công dụng như thuốc"), hoặc đang trích câu hỏi của khách.
    """
    truoc = norm_line[max(0, vi_tri - _CUA_SO_PHU_DINH) : vi_tri]
    if _PHU_DINH.search(truoc):
        return True
    sau = norm_line[het if het is not None else vi_tri :]
    return bool(_PHU_DINH_SAU.search(sau) or _LA_CAU_HOI.match(sau))


_LA_TIEU_DE = re.compile(r"^\s{0,3}#{1,6}\s")
# Chỉ bỏ qua GẠCH ĐẦU DÒNG và Ô BẢNG nằm dưới tiêu đề cấm - không bỏ qua văn xuôi.
# Kịch bản quảng cáo viết bằng văn xuôi, nên lỗ hổng "nấp dưới tiêu đề cấm" bị chặn.
# Ô bảng bắt đầu bằng | và không cần khoảng trắng sau (dòng kẻ |---|---| cũng tính)
_LA_MUC_LIET_KE = re.compile(r"^\s{0,4}(\||[-*+>]\s|\d+[.)]\s)")


def _danh_dau_dong_tham_chieu(lines: list[str]) -> list[bool]:
    """Đánh dấu những dòng chỉ NHẮC tới từ cấm để cấm, không phải để dùng.

    Khối cấm mở bằng một dòng gợi ý ("Không được nói:", "❌ Câu cấm", tiêu đề bảng
    thay từ) và chỉ tha các GẠCH ĐẦU DÒNG, Ô BẢNG ngay sau đó. Gặp văn xuôi hoặc
    tiêu đề mới là đóng khối - nên không nấp văn quảng cáo dưới tiêu đề cấm được.
    """
    ket_qua: list[bool] = []
    trong_khoi_cam = False
    for line in lines:
        la_cue = _la_dong_tham_chieu(line)
        if _LA_TIEU_DE.match(line):
            trong_khoi_cam = la_cue
            ket_qua.append(la_cue)
            continue
        if la_cue:
            trong_khoi_cam = True  # dòng gợi ý mở khối cho các mục ngay dưới
            ket_qua.append(True)
            continue
        if not line.strip():
            ket_qua.append(False)  # dòng trống giữ nguyên khối, không tính
            continue
        if _LA_MUC_LIET_KE.match(line):
            ket_qua.append(trong_khoi_cam)
            continue
        trong_khoi_cam = False  # gặp văn xuôi là đóng khối
        ket_qua.append(False)
    return ket_qua


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
    bo_qua: bool = False  # file tra cứu, có đánh dấu bỏ qua
    so_dong_tham_chieu: int = 0  # dòng nhắc từ cấm trong ngữ cảnh cấm, đã bỏ qua

    @property
    def blocking(self) -> list[Issue]:
        return [i for i in self.issues if i.muc_do == "chan"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.muc_do == "canh_bao"]

    def to_text(self) -> str:
        if self.bo_qua:
            return "File tra cứu (có đánh dấu bỏ qua) - không soát."
        ghi_chu = (
            f"\nĐã bỏ qua {self.so_dong_tham_chieu} dòng nhắc tới từ cấm trong ngữ cảnh "
            "cấm hoặc phủ định (dùng --nghiem-ngat để soát cả những dòng này)."
            if self.so_dong_tham_chieu
            else ""
        )
        if not self.issues:
            return (
                "Không phát hiện lỗi tuân thủ. Vẫn nên đọc lại bằng mắt trước khi đăng."
                + ghi_chu
            )
        lines = [str(i) for i in self.issues]
        lines.append("")
        lines.append(
            f"Tổng: {len(self.blocking)} lỗi chặn đăng, {len(self.warnings)} cảnh báo."
        )
        return "\n".join(lines) + ghi_chu

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

_ABSOLUTE = re.compile(
    r"\b(100%|chắc chắn khỏi|hoàn toàn khỏi)\b"
    r"|(khỏi|hết|tác dụng|hiệu quả)[^.!?\n]{0,20}vĩnh viễn"
    r"|tuyệt đối[^.!?\n]{0,15}(an toàn|hiệu quả|khỏi|không tái phát)"
)


def check(
    text: str, *, yeu_cau_khuyen_cao: bool = True, nghiem_ngat: bool = False
) -> Report:
    """Soát một kịch bản và trả về báo cáo tuân thủ.

    nghiem_ngat=True thì soát cả những dòng liệt kê điều cấm. Chỉ dùng khi muốn
    kiểm tra thật kỹ một kịch bản sắp quay, không dùng cho tài liệu tra cứu.
    """
    rules = kb.compliance()
    report = Report()

    if BO_QUA_MARKER in text:
        report.bo_qua = True
        return report

    lines = text.splitlines()
    norm_lines = [_norm(line) for line in lines]
    norm_full = _norm(text)
    # Bản đã che các cụm hợp lệ - chỉ dùng cho bước soát từ cấm, vì bản thân câu
    # khuyến cáo bắt buộc cũng chứa những từ nằm trong danh sách cấm.
    masked_lines = [_mask_allowed(line, rules) for line in norm_lines]

    # Dòng nào chỉ NHẮC tới từ cấm để cấm thì không tính là vi phạm.
    if nghiem_ngat:
        tham_chieu = [False] * len(lines)
    else:
        tham_chieu = _danh_dau_dong_tham_chieu(lines)
        report.so_dong_tham_chieu = sum(tham_chieu)

    # 1. Từ cấm
    for pair in rules["tu_cam_va_tu_thay_the"]:
        needle = _norm(pair["cam"])
        for idx, line in enumerate(masked_lines, start=1):
            if tham_chieu[idx - 1]:
                continue
            vi_tri = line.find(needle)
            if (
                vi_tri >= 0
                and _bi_phu_dinh(line, vi_tri, vi_tri + len(needle))
                and not nghiem_ngat
            ):
                report.so_dong_tham_chieu += 1
                continue
            if vi_tri >= 0:
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
            if tham_chieu[idx - 1]:
                continue
            khop = pattern.search(line)
            if khop and _bi_phu_dinh(line, khop.start(), khop.end()) and not nghiem_ngat:
                report.so_dong_tham_chieu += 1
                continue
            if khop:
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
        if tham_chieu[idx - 1]:
            continue
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
