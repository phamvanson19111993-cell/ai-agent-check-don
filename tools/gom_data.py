"""Gom dữ liệu 'chưa chốt' từ các file Drive cũ -> 1 danh sách sạch.

- Khôi phục số 0 đầu của số điện thoại (Google Sheet cũ làm mất)
- Bỏ số trùng, giữ lần gần nhất
- Sắp xếp mới nhất trước
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pancake_export import phones

PAGES = {
    "BPT": "BPT Tim Mạch Não Bộ",
    "D1": "PHS DILIM 1",
    "D2": "PHS DiLim 2",
    "D3": "PHS DILIM 3",
    "D4": "PHS DiLim 4",
    "D5": "PHS Dilim 5",
    "SKLV": "PHS Sức Khoẻ Là Vàng",
    "PHS": "PHS",
    "": "(không rõ)",
}

# Ghi chú sale đã nhập tay trong file Drive cũ, ghép lại theo số điện thoại.
NOTES = {
    "0919244899": "tê bì tay, ko đau đầu, 2-3h sáng tê bì, thức đêm nhiều, xung huyết dạ dày, "
                  "chạy xe tải 10h/ngày, ê cổ",
    "0909620057": "tí gọi lại",
    "0919855689": "đỡ mất ngủ, đau cổ vai gáy, tê xuống chân, mỡ máu, ngủ được 4 tiếng",
    "0942185956": "17h gọi lại",
    "0916666687": "trước khó ngủ, ngủ khuya, giờ đỡ rồi",
    "0947537084": "thuê bao",
    "0917861290": "lộn số",
    "0779944095": "cần hỏi lại tên",
    "0977414711": "Quan tâm: RICH - Rich Coenzyme Q10",
    "0913237864": "ko còn đau đầu nữa",
    "0914168801": "Rich đã đặt",
    "0919871392": "đi BS bảo hiểm Bạc Liêu, mất ngủ, uống thuốc nam dễ ngủ",
    "0917511717": "khó ngủ, công việc, thuốc tây, CoQ10, khỏe",
    "0913470644": "tai biến nhẹ, không muốn nghe nhiều",
    "0916906404": "5h chiều gọi lại",
    "0969866349": "Quan tâm: RICH - Rich Coenzyme Q10",
}

MONTH_ORDER = {4: 4, 5: 5, 7: 7, 8: 8}


def sort_key(row):
    day, month = row["_day"], row["_month"]
    return (month, day)


def load(path):
    rows = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            parts = line.split("|")
            if len(parts) < 3:
                continue
            name, raw_phone, date = parts[0], parts[1], parts[2]
            page_code = parts[3] if len(parts) > 3 else ""

            phone = phones.normalize(raw_phone if raw_phone.startswith("0") else "0" + raw_phone)
            if not phone:
                phone = "0" + raw_phone.strip()

            day, month = (date.split("/") + ["0"])[:2]
            rows.append({
                "ten": name.strip(),
                "sdt": phone,
                "tinh_trang": "Chưa chốt",
                "ngay": date.strip(),
                "page": PAGES.get(page_code.strip(), page_code.strip()),
                "ghi_chu": NOTES.get(phone, ""),
                "_day": int(day) if day.isdigit() else 0,
                "_month": int(month) if month.isdigit() else 0,
            })
    return rows


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rows = []
    for name in ("raw_thang7_8.txt", "raw_thang4_5.txt"):
        rows.extend(load(os.path.join(base, "data", name)))

    rows.sort(key=sort_key, reverse=True)

    seen, unique = set(), []
    for row in rows:
        if row["sdt"] in seen:
            continue
        seen.add(row["sdt"])
        unique.append(row)

    out = os.path.join(base, "data", "sdt_chua_chot_tong_hop.csv")
    with open(out, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Tên", "SĐT", "Tình trạng", "Ngày", "Page", "Ghi chú"])
        for row in unique:
            writer.writerow([row["ten"], row["sdt"], row["tinh_trang"],
                             row["ngay"], row["page"], row["ghi_chu"]])

    by_page = {}
    for row in unique:
        by_page[row["page"]] = by_page.get(row["page"], 0) + 1

    print("Tổng dòng đọc được : %s" % len(rows))
    print("Sau khi lọc trùng  : %s số" % len(unique))
    print("Đã ghi: %s" % out)
    print("\nTheo page:")
    for page, count in sorted(by_page.items(), key=lambda item: -item[1]):
        print("  %-24s %s" % (page, count))


if __name__ == "__main__":
    main()
