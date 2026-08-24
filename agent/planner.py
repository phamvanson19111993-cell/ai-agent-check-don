"""Lên lịch nội dung theo tháng - chạy được offline, không cần API."""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict
from datetime import date, timedelta

from . import kb

# Tỉ lệ trụ cột nội dung trong một tuần 7 ngày.
TRU_COT = (
    ["giao-duc"] * 3 + ["cau-chuyen"] * 2 + ["san-pham"] * 1 + ["tuong-tac"] * 1
)

FORMAT_THEO_TRU_COT = {
    "giao-duc": ["giai-thich-co-che", "dap-tan-hieu-lam", "hoi-dap"],
    "cau-chuyen": ["ke-chuyen"],
    "san-pham": ["hook-noi-dau-giai-phap", "bo-ba-san-pham"],
    "tuong-tac": ["hoi-dap", "dap-tan-hieu-lam"],
}

CTA_THEO_TRU_COT = {
    "giao-duc": "mềm",
    "cau-chuyen": "mềm",
    "san-pham": "mạnh",
    "tuong-tac": "trung bình",
}


@dataclass
class Ngay:
    ngay: str
    thu: str
    tru_cot: str
    trieu_chung: str
    doi_tuong: str
    dinh_dang: str
    nen_tang: str
    thoi_luong: int
    cta: str
    hook_goi_y: str

    @property
    def lenh_tao(self) -> str:
        return (
            f"python -m agent.cli generate --trieu-chung {self.trieu_chung} "
            f"--doi-tuong {self.doi_tuong} --dinh-dang {self.dinh_dang} "
            f"--nen-tang {self.nen_tang} --thoi-luong {self.thoi_luong}"
        )


THU_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def build(so_ngay: int = 30, bat_dau: date | None = None, seed: int = 7) -> list[Ngay]:
    """Xoay vòng triệu chứng - đối tượng - định dạng để lịch không bị lặp nhàm."""
    rng = random.Random(seed)
    bat_dau = bat_dau or date.today()

    symptoms = [s["id"] for s in kb.symptoms()]
    personas = [p["id"] for p in kb.personas()]
    formats = {f["id"]: f for f in kb.formats()}

    ke_hoach: list[Ngay] = []
    for i in range(so_ngay):
        d = bat_dau + timedelta(days=i)
        tru_cot = TRU_COT[i % len(TRU_COT)]
        sym = symptoms[i % len(symptoms)]
        per = personas[(i // 2) % len(personas)]
        fmt_id = FORMAT_THEO_TRU_COT[tru_cot][i % len(FORMAT_THEO_TRU_COT[tru_cot])]
        fmt = formats[fmt_id]
        nen_tang = fmt["nen_tang"][i % len(fmt["nen_tang"])]
        hooks = kb.hooks_for(sym)
        hook = rng.choice(hooks)["cau"] if hooks else ""

        ke_hoach.append(
            Ngay(
                ngay=d.isoformat(),
                thu=THU_VN[d.weekday()],
                tru_cot=tru_cot,
                trieu_chung=sym,
                doi_tuong=per,
                dinh_dang=fmt_id,
                nen_tang=nen_tang,
                thoi_luong=fmt["thoi_luong_goi_y"],
                cta=CTA_THEO_TRU_COT[tru_cot],
                hook_goi_y=hook,
            )
        )
    return ke_hoach


def to_markdown(ke_hoach: list[Ngay]) -> str:
    ten_sym = {s["id"]: s["ten"] for s in kb.symptoms()}
    ten_per = {p["id"]: p["ten"] for p in kb.personas()}
    ten_fmt = {f["id"]: f["ten"] for f in kb.formats()}

    lines = [
        f"# Lịch nội dung {len(ke_hoach)} ngày",
        "",
        "Tỉ lệ trụ cột: 3 giáo dục - 2 câu chuyện - 1 sản phẩm - 1 tương tác mỗi tuần.",
        "",
        "| Ngày | Thứ | Trụ cột | Chủ đề | Đối tượng | Định dạng | Nền tảng | Giây | CTA | Hook gợi ý |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for n in ke_hoach:
        lines.append(
            f"| {n.ngay} | {n.thu} | {n.tru_cot} | {ten_sym[n.trieu_chung]} | "
            f"{ten_per[n.doi_tuong]} | {ten_fmt[n.dinh_dang]} | {n.nen_tang} | "
            f"{n.thoi_luong} | {n.cta} | {n.hook_goi_y} |"
        )

    lines += ["", "## Lệnh tạo kịch bản cho từng ngày", "", "```bash"]
    lines += [f"# {n.ngay} - {n.thu}\n{n.lenh_tao}" for n in ke_hoach]
    lines += ["```"]
    return "\n".join(lines)


def to_dicts(ke_hoach: list[Ngay]) -> list[dict]:
    return [asdict(n) for n in ke_hoach]
