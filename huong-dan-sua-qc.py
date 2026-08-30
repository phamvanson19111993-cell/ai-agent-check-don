#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vẽ ảnh chỉ chỗ bấm để SỬA một quảng cáo đang chạy.

Khác huong-dan-bam.py: file kia chỉ màn hình lúc TẠO quảng cáo mới, file này
chỉ ba việc phải làm trên quảng cáo ĐÃ chạy — đổi ảnh sang khổ đứng, đổi tiêu
đề, rồi đăng lại.

    python3 huong-dan-sua-qc.py
Ra: quang-cao/anh/huong-dan-sua-qc.jpg
"""

import os

GOC = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

TRANG = """<!doctype html><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1000px;background:#F0F2F5;padding:32px;
       font-family:"Liberation Sans","DejaVu Sans",sans-serif;color:#1C1E21}
  h1{font-size:33px;margin-bottom:6px}
  .phu{font-size:21px;color:#65676B;margin-bottom:24px;line-height:1.45}
  .the{background:#fff;border:1px solid #DADDE1;border-radius:12px;
       padding:22px 24px 20px;margin-bottom:18px;position:relative}
  .so{position:absolute;left:-16px;top:20px;width:46px;height:46px;
      border-radius:50%;background:#D93025;color:#fff;font-size:26px;
      font-weight:700;display:flex;align-items:center;justify-content:center;
      box-shadow:0 2px 6px rgba(0,0,0,.25)}
  .tieu{font-size:24px;font-weight:700;margin-bottom:10px;padding-left:38px}
  .noi{font-size:20px;line-height:1.5}
  .o{border:3px solid #1877F2;background:#F0F6FF;border-radius:8px;
     padding:14px 16px;font-size:20px;font-weight:700;margin:12px 0}
  .nut{display:inline-block;background:#1877F2;color:#fff;font-size:20px;
       font-weight:700;padding:11px 22px;border-radius:7px;margin:4px 6px 4px 0}
  .nut.xanhla{background:#177B4C}
  .canh{background:#FFF4F3;border-left:5px solid #D93025;border-radius:0 8px 8px 0;
        padding:13px 16px;margin-top:14px;font-size:20px;line-height:1.45}
  .canh b{color:#D93025}
  .ok{background:#E7F3E8;border-left:5px solid #2E7D32;border-radius:0 8px 8px 0;
      padding:13px 16px;margin-top:12px;font-size:20px;line-height:1.45}
  .ok b{color:#2E7D32}
  code{background:#EBEDF0;border-radius:5px;padding:3px 8px;font-size:19px;
       font-family:"DejaVu Sans Mono",monospace}
</style>

<h1>Sửa quảng cáo đang chạy — ba việc, một lượt</h1>
<div class="phu">Mở Ads Manager → tab <b>Quảng cáo</b> → tick dòng
<code>QC · Nhom 1</code> → bấm <b>Chỉnh sửa</b>.<br>
Làm hết cả ba rồi mới đăng. Sửa ba lần rời rạc là reset học ba lần.</div>

<div class="the">
  <div class="so">1</div>
  <div class="tieu">Thêm ảnh khổ đứng 9:16</div>
  <div class="noi">Kéo tới mục ảnh → bấm <b>Thêm ảnh</b> → tải lên
  <code>giam-mo-doc.jpg</code>.<br><br>
  <b>GIỮ LUÔN ảnh 4:5 cũ, đừng xoá.</b> Có hai ảnh thì Facebook tự chọn:
  bảng tin dùng 4:5, Reels và Story dùng 9:16.</div>
  <div class="canh">Đây là việc đáng tiền nhất trong ba việc. Ảnh chụp bản
  xem trước Story cho thấy ảnh 4:5 <b>không lấp đầy khung</b> — trên dưới hai
  mảng nâu trống. Khách lướt qua không dừng lại, mà tiền vẫn tính.</div>
</div>

<div class="the">
  <div class="so">2</div>
  <div class="tieu">Đổi ô Tiêu đề</div>
  <div class="noi">Xoá chữ cũ, dán đúng dòng này:</div>
  <div class="o">Hỗ trợ giảm béo — 22.500đ mỗi ngày</div>
  <div class="noi">Ogilvy: hứa <b>lợi ích trước</b>, giá đỡ sau. Cái cũ bắt
  người đọc gặp con số trước khi biết con số đó mua được gì.</div>
  <div class="ok"><b>✓ Ô Mô tả giữ nguyên</b> — trong đó đã có
  “AFC Nhật Bản” và số công bố.</div>
</div>

<div class="the">
  <div class="so">3</div>
  <div class="tieu">Kiểm lại đường dẫn rồi đăng</div>
  <div class="o">https://sonsongkhoe.com/giam-mo/</div>
  <div class="noi">Nhớ dấu <code>/</code> ở cuối. Rồi bấm lần lượt:</div>
  <div><span class="nut">Xuất bản</span><span class="nut xanhla">⬆ Đăng</span></div>
  <div class="canh"><b>Bấm Xuất bản thôi là CHƯA XONG.</b> Thay đổi nằm ở bản
  nháp cho tới khi bấm <b>Đăng</b> — đúng cái đã làm anh tưởng chiến dịch đã
  bật hôm nay. Cột Phân phối còn chữ <b>Bản nháp</b> là chưa ăn.</div>
</div>

<div class="phu" style="margin-top:22px">
Sửa xong <b>để yên 48 giờ</b>, dù số có xấu. Facebook đang học lại từ đầu sau
mỗi lần sửa; đụng vào nữa là học lại lần nữa, tiền test coi như bỏ.
</div>
"""


def main():
    ra = os.path.join(GOC, 'quang-cao', 'anh')
    os.makedirs(ra, exist_ok=True)
    duong = os.path.join(ra, 'huong-dan-sua-qc.jpg')
    tam = duong.replace('.jpg', '.html')
    with open(tam, 'w', encoding='utf-8') as f:
        f.write(TRANG)

    from playwright.sync_api import sync_playwright
    import cv2
    with sync_playwright() as p:
        br = p.chromium.launch(**({'executable_path': CHROME}
                                  if os.path.exists(CHROME) else {}))
        tr = br.new_page(viewport={'width': 1000, 'height': 1200})
        tr.goto('file://' + tam)
        tr.wait_for_timeout(300)
        tr.screenshot(path=duong.replace('.jpg', '.png'), full_page=True)
        br.close()
    im = cv2.imread(duong.replace('.jpg', '.png'))
    cv2.imwrite(duong, im, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    os.remove(duong.replace('.jpg', '.png'))
    os.remove(tam)
    print('%s — %d×%d, %d KB'
          % (duong, im.shape[1], im.shape[0], os.path.getsize(duong) // 1024))


if __name__ == '__main__':
    main()
