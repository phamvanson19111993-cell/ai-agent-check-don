"""Cập nhật danh sách chưa chốt theo ghi chú mới trên Google Sheet (bản sửa 10/9).

Sheet gốc: "SĐT chưa chốt Pancake - 3 tháng gần nhất"
(1_SjwNvfzPMUzAjeDJ46MmCsSXYcmZ_cggj6NKz5kJjk), đọc ngày 14/09/2026.

Dòng dữ liệu vẫn dừng ở 15/8 — phần thay đổi là ghi chú sale nhập tay và một tab
đơn hàng. Script này chỉ làm một việc: bỏ/đánh dấu những số mà ghi chú mới cho
thấy không cần gọi lại nữa.
"""

import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "sdt_chua_chot_tong_hop.csv")
OUT = os.path.join(BASE, "data", "sdt_chua_chot_cap_nhat_10-9.csv")
OUT_LOAI = os.path.join(BASE, "data", "sdt_da_loai_10-9.csv")

# Đã chốt đơn — đối chiếu tab đơn hàng trong sheet.
DA_CHOT = {
    "0986027778": "Đã chốt Nattokinase 2.290.000đ (tab đơn hàng)",
    "0845001769": "Đã chốt Rich + DHA 6.180.000đ ngày 26/08 (tab đơn hàng)",
}

# Khách nói không có nhu cầu / không gọi lại nữa.
KHONG_NHU_CAU = {
    "0913638052": "Anh không có nhu cầu",
    "0912228414": "Gọi lần thứ 3, không có nhu cầu — không gọi lại nữa",
    "0853727255": "Không cần, đi khám sức khoẻ định kỳ",
    "0839856016": "Chị không mua đâu nhá",
    "0854283549": "Uống thuốc đỡ rồi",
    "0913810822": "Không bị",
}

# Số không dùng được.
SO_HONG = {
    "0945142618": "Số điện thoại chưa đúng",
    "0947537084": "Thuê bao",
    "0916365062": "Thuê bao",
    "0947838695": "Thuê bao",
    "0917861290": "Lộn số",
}

# Có hẹn gọi lại — giữ trong danh sách, ưu tiên gọi.
HEN_GOI_LAI = {
    "0389192830": "Hẹn gọi lại 28/8",
    "0918433858": "Khách tiềm năng — hẹn 13h30 ngày 31/8",
    "0941802238": "Hẹn lên đơn ngày 7/9 — Gia Lai",
    "0942185956": "Hẹn 17h gọi lại",
    "0916906404": "Hẹn 17h gọi lại",
    "0909620057": "Hẹn gọi lại",
    "0325748057": "Hẹn gọi lại sau",
}


def main():
    with open(SRC, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = list(reader)

    giu, loai = [], []
    for row in rows:
        phone = row[1]
        if phone in DA_CHOT:
            loai.append(row + ["ĐÃ CHỐT", DA_CHOT[phone]])
        elif phone in KHONG_NHU_CAU:
            loai.append(row + ["KHÔNG NHU CẦU", KHONG_NHU_CAU[phone]])
        elif phone in SO_HONG:
            loai.append(row + ["SỐ HỎNG", SO_HONG[phone]])
        else:
            uu_tien = "ƯU TIÊN" if phone in HEN_GOI_LAI else ""
            hen = HEN_GOI_LAI.get(phone, "")
            giu.append(row + [uu_tien, hen])

    # Số có hẹn gọi lại xếp lên đầu.
    giu.sort(key=lambda item: item[-2] != "ƯU TIÊN")

    with open(OUT, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header + ["Ưu tiên", "Hẹn gọi lại"])
        writer.writerows(giu)

    with open(OUT_LOAI, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header + ["Lý do loại", "Chi tiết"])
        writer.writerows(loai)

    print("Danh sách cũ      : %s số" % len(rows))
    print("Loại ra           : %s số (%s đã chốt, %s không nhu cầu, %s số hỏng)"
          % (len(loai), len(DA_CHOT), len(KHONG_NHU_CAU), len(SO_HONG)))
    print("Còn cần gọi       : %s số — trong đó %s số có hẹn gọi lại"
          % (len(giu), len(HEN_GOI_LAI)))
    print("→ %s" % OUT)
    print("→ %s" % OUT_LOAI)


if __name__ == "__main__":
    main()
