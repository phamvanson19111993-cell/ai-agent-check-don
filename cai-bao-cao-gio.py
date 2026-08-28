#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CÀI BÁO CÁO MỖI GIỜ — chạy MỘT LẦN, xong là chạy mãi

Chương trình này làm hộ anh bốn việc:
  1. Hỏi ba mã, lưu vào file cau-hinh.json bên cạnh
  2. Gửi thử một tin về Telegram để chắc chắn thông
  3. Tự đặt lịch chạy mỗi giờ trên máy anh
  4. In ra cách gỡ nếu sau này muốn dừng

CÁCH CHẠY
    python3 cai-bao-cao-gio.py

Chạy lại lần nữa lúc nào cũng được — nó hỏi lại và ghi đè cấu hình cũ,
không tạo thêm lịch trùng.
"""

import json
import os
import platform
import subprocess
import sys
from getpass import getpass

O_DAY   = os.path.dirname(os.path.abspath(__file__))
CAU_HINH = os.path.join(O_DAY, "cau-hinh.json")
CHUONG_TRINH = os.path.join(O_DAY, "bao-cao-telegram.py")
TEN_LICH = "DiLiM bao cao moi gio"


def hoi(nhan, cu="", kin=False, bat_buoc=True):
    goi = "  %s%s: " % (nhan, (" [giữ nguyên]" if cu else ""))
    while True:
        gt = (getpass(goi) if kin else input(goi)).strip()
        if not gt and cu:
            return cu
        if gt or not bat_buoc:
            return gt
        print("     Chưa nhập gì. Thử lại.")


def main():
    print("\n" + "═" * 62)
    print("  CÀI BÁO CÁO QUẢNG CÁO MỖI GIỜ QUA TELEGRAM")
    print("═" * 62)

    if not os.path.exists(CHUONG_TRINH):
        sys.exit("Không thấy bao-cao-telegram.py cạnh file này. "
                 "Hai file phải nằm cùng một thư mục.")

    cu = {}
    if os.path.exists(CAU_HINH):
        try:
            with open(CAU_HINH, encoding="utf-8") as f:
                cu = json.load(f)
            print("\n  Đã có cấu hình cũ. Enter là giữ nguyên từng dòng.")
        except Exception:
            pass

    # ── 1. Hỏi ba mã ──
    print("\n─ 1. BA MÃ ─────────────────────────────────────────────")
    print("  Mã bot lấy từ @BotFather, mã cuộc trò chuyện từ @userinfobot.")
    print("  Gõ vào sẽ không hiện lên màn hình với hai mã bí mật — cố ý.")
    ch = {
        "TG_TOKEN": hoi("Mã bot Telegram", cu.get("TG_TOKEN", ""), kin=True),
        "TG_CHAT":  hoi("Mã cuộc trò chuyện", cu.get("TG_CHAT", "")),
        "FB_TOKEN": hoi("Mã truy cập Facebook", cu.get("FB_TOKEN", ""), kin=True),
        "FB_ACT":   hoi("Mã tài khoản quảng cáo", cu.get("FB_ACT", "2260044828113956")),
        "FB_PIXEL": hoi("Mã Pixel", cu.get("FB_PIXEL", "1277743445418211")),
    }

    with open(CAU_HINH, "w", encoding="utf-8") as f:
        json.dump(ch, f, ensure_ascii=False, indent=2)
    try:
        os.chmod(CAU_HINH, 0o600)     # chi minh anh doc duoc
    except Exception:
        pass
    print("\n  ✓ Đã lưu vào %s" % CAU_HINH)
    print("    File này chứa mã bí mật. Đừng gửi cho ai, đừng đẩy lên GitHub.")

    # ── 2. Gửi thử ──
    print("\n─ 2. GỬI THỬ ───────────────────────────────────────────")
    print("  Đang chạy báo cáo và gửi về Telegram…\n")
    kq = subprocess.run([sys.executable, CHUONG_TRINH],
                        capture_output=True, text=True)
    ra = (kq.stdout or "") + (kq.stderr or "")
    for d in ra.strip().split("\n"):
        print("  | " + d)

    if "Đã gửi về Telegram" not in ra:
        print("\n  ⛔ CHƯA GỬI ĐƯỢC. Đọc dòng lỗi ở trên.")
        print("     Hai lý do hay gặp nhất:")
        print("       · Chưa nhắn cho bot CỦA ANH một câu bất kỳ trước.")
        print("         Telegram không cho bot nhắn tới người lạ.")
        print("       · Mã truy cập Facebook đã hết hạn. Mã lấy từ Graph API")
        print("         Explorer chỉ sống 1-2 tiếng — phải dùng mã Người dùng")
        print("         hệ thống thì mới chạy tự động được.")
        print("\n     Sửa xong chạy lại chương trình này. CHƯA đặt lịch.")
        return

    print("\n  ✓ Tin đã tới Telegram. Mở điện thoại xem thử.")

    # ── 3. Đặt lịch ──
    print("\n─ 3. ĐẶT LỊCH MỖI GIỜ ──────────────────────────────────")
    he = platform.system()

    if he == "Windows":
        subprocess.run(["schtasks", "/Delete", "/TN", TEN_LICH, "/F"],
                       capture_output=True)
        r = subprocess.run(
            ["schtasks", "/Create", "/SC", "HOURLY", "/TN", TEN_LICH,
             "/TR", '"%s" "%s"' % (sys.executable, CHUONG_TRINH), "/F"],
            capture_output=True, text=True)
        if r.returncode == 0:
            print("  ✓ Đã đặt lịch Windows, tên: %s" % TEN_LICH)
            print("    Xem lại: mở Task Scheduler, tìm đúng tên đó.")
            print("    Muốn dừng: schtasks /Delete /TN \"%s\" /F" % TEN_LICH)
        else:
            print("  ⚠ Chưa đặt được lịch tự động.")
            print("    %s" % (r.stderr or r.stdout or "").strip()[:200])
            print("    Thường do chưa chạy bằng quyền quản trị.")
            print("    Bấm phải vào Command Prompt → Run as administrator → chạy lại.")
    else:
        dong = "0 * * * * cd %s && %s %s >> %s 2>&1" % (
            O_DAY, sys.executable, CHUONG_TRINH, os.path.join(O_DAY, "nhat-ky.txt"))
        hien = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        cu_lich = hien.stdout if hien.returncode == 0 else ""
        giu = [d for d in cu_lich.split("\n")
               if d.strip() and "bao-cao-telegram.py" not in d]
        giu.append(dong)
        moi = "\n".join(giu) + "\n"
        r = subprocess.run(["crontab", "-"], input=moi, capture_output=True, text=True)
        if r.returncode == 0:
            print("  ✓ Đã đặt lịch chạy phút thứ 0 mỗi giờ.")
            print("    Xem lại:  crontab -l")
            print("    Nhật ký:  %s" % os.path.join(O_DAY, "nhat-ky.txt"))
            print("    Muốn dừng: crontab -e rồi xoá dòng có bao-cao-telegram.py")
        else:
            print("  ⚠ Chưa đặt được lịch: %s" % (r.stderr or "").strip()[:160])
            print("    Đặt tay: crontab -e rồi thêm dòng này")
            print("    %s" % dong)

    print("\n" + "═" * 62)
    print("  XONG. Mỗi giờ anh sẽ nhận một tin.")
    print("  LƯU Ý: lịch chạy trên máy này. Máy tắt hoặc ngủ là không chạy.")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nĐã dừng. Chưa đặt lịch gì.\n")
