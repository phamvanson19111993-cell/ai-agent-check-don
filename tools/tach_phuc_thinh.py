"""Tách riêng danh sách chưa chốt của page Phúc Thịnh (BPT Tim Mạch Não Bộ)."""

import csv
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "data", "sdt_chua_chot_tong_hop.csv")
OUT = os.path.join(BASE, "data", "sdt_chua_chot_phuc_thinh.csv")

with open(SRC, "r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.reader(handle)
    header = next(reader)
    rows = [row for row in reader if row[4].startswith("BPT")]

with open(OUT, "w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["Tên", "SĐT", "Tình trạng", "Ngày", "Ghi chú"])
    for row in rows:
        writer.writerow([row[0], row[1], row[2], row[3], row[5]])

print("%s dòng -> %s" % (len(rows), OUT))
