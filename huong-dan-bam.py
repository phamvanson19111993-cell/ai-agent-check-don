#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vẽ ảnh chỉ chỗ bấm trên màn hình Ads Manager, cho anh Sơn vừa nhìn vừa làm.

Vẽ lại màn hình bằng HTML rồi chụp, chứ không chú thích lên ảnh chụp thật —
như vậy chữ nào cũng sắc nét và đọc được trên điện thoại.

    python3 huong-dan-bam.py
Ra: quang-cao/anh/huong-dan-dich-den.jpg
"""

import os
import sys

GOC = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

TRANG = """<!doctype html><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1000px;background:#F0F2F5;padding:32px;
       font-family:"Liberation Sans","DejaVu Sans",sans-serif;color:#1C1E21}
  h1{font-size:34px;margin-bottom:6px}
  .phu{font-size:21px;color:#65676B;margin-bottom:26px}
  .the{background:#fff;border:1px solid #DADDE1;border-radius:12px;
       padding:22px 24px;margin-bottom:18px;position:relative}
  .nhan{font-size:20px;font-weight:700;margin-bottom:12px}
  .o{border:1px solid #CCD0D5;border-radius:8px;padding:14px 16px;
     font-size:20px;color:#8A8D91;background:#fff}
  .o.dien{color:#1C1E21;border:3px solid #1877F2;background:#F0F6FF;font-weight:700}
  .hang{display:flex;align-items:flex-start;gap:12px;margin:11px 0;font-size:20px}
  .tick{width:24px;height:24px;border:2px solid #8A8D91;border-radius:4px;
        flex:0 0 auto;margin-top:2px}
  .tick.on{background:#1877F2;border-color:#1877F2;color:#fff;text-align:center;
           line-height:22px;font-size:17px;font-weight:700}
  .tron{width:24px;height:24px;border:2px solid #8A8D91;border-radius:50%;
        flex:0 0 auto;margin-top:2px;position:relative}
  .tron.on{border-color:#1877F2}
  .tron.on::after{content:"";position:absolute;inset:5px;border-radius:50%;
                  background:#1877F2}
  .mo{color:#65676B;font-size:18px}
  .xanh{color:#1877F2;font-weight:700;font-size:20px}
  .so{position:absolute;left:-16px;width:46px;height:46px;border-radius:50%;
      background:#D93025;color:#fff;font-size:26px;font-weight:700;
      display:flex;align-items:center;justify-content:center;
      box-shadow:0 2px 6px rgba(0,0,0,.25)}
  .viec{background:#FFF4F3;border-left:5px solid #D93025;border-radius:0 8px 8px 0;
        padding:12px 16px;margin-top:12px;font-size:20px;line-height:1.45}
  .viec b{color:#D93025}
  .dat{background:#E7F3E8;border-left:5px solid #2E7D32;border-radius:0 8px 8px 0;
       padding:12px 16px;margin-top:12px;font-size:20px}
  .dat b{color:#2E7D32}
  code{background:#EBEDF0;border-radius:5px;padding:3px 8px;font-size:19px;
       font-family:"DejaVu Sans Mono",monospace}
  .cuoi{font-size:20px;color:#65676B;margin-top:8px;line-height:1.5}
</style>

<h1>Màn hình anh đang mở — bốn chỗ cần đụng vào</h1>
<div class="phu">Số đỏ là việc phải làm. Chỗ nào không có số đỏ thì để nguyên.</div>

<div class="the">
  <div class="nhan">Nguồn nội dung</div>
  <div class="hang"><span class="tron on"></span><span>Tải lên thủ công</span></div>
  <div class="hang"><span class="tron"></span><span class="mo">Quảng cáo danh mục Advantage+</span></div>
  <div class="dat"><b>✓ Đúng rồi</b> — để nguyên, không đụng.</div>
</div>

<div class="the">
  <div class="nhan">Định dạng</div>
  <div class="hang"><span class="tron on"></span><span>Một hình ảnh/video</span></div>
  <div class="hang"><span class="tron"></span><span class="mo">Quay vòng</span></div>
  <div class="dat"><b>✓ Đúng rồi</b> — để nguyên.</div>
</div>

<div class="the">
  <div class="so" style="top:20px">1</div>
  <div class="hang"><span class="tick on">✓</span>
    <span><b>Quảng cáo đa bên</b><br>
    <span class="mo">Nội dung quảng cáo có thể bị cắt hoặc thay đổi kích thước.</span></span>
  </div>
  <div class="viec"><b>BỎ TICK ô này.</b> Ảnh của mình có chữ giá và dòng khuyến cáo
  bắt buộc — bị cắt là mất đúng phần quan trọng nhất.</div>
</div>

<div class="the">
  <div class="so" style="top:20px">2</div>
  <div class="xanh">Hiển thị thêm cài đặt ▾</div>
  <div class="viec"><b>BẤM vào dòng xanh này.</b> Mở ra tìm mục
  <b>Cải tiến sáng tạo Advantage+</b> rồi <b>gạt tắt hết</b>.<br>
  Để bật thì Facebook tự đổi chữ, tự thêm nhạc, tự chỉnh ảnh — làm mất câu
  “Thực phẩm này không phải là thuốc…” là bài sai luật.</div>
</div>

<div class="the">
  <div class="so" style="top:20px">3</div>
  <div class="nhan">Đích đến chính</div>
  <div class="o" style="margin-bottom:14px">Trang web ▾ <span class="mo">(đúng rồi)</span></div>
  <div class="nhan">URL trang web · Bắt buộc</div>
  <div class="o dien">https://sonsongkhoe.com/giam-mo/</div>
  <div class="viec"><b>DÁN đúng dòng này</b> — nhớ có dấu <code>/</code> ở cuối.
  Dán xong bấm ra ngoài ô một cái.</div>
</div>

<div class="the">
  <div class="so" style="top:20px">4</div>
  <div class="hang"><span class="tick"></span><span>Dùng liên kết hiển thị</span></div>
  <div class="viec"><b>ĐỂ TRỐNG</b> — đừng tick.</div>
</div>

<div class="cuoi">
  Kéo xuống dưới còn <b>Văn bản chính · Tiêu đề · Mô tả · Lời kêu gọi</b> và chỗ
  <b>thêm ảnh</b>. Điền đủ hết rồi mới bấm nút xanh <b>Đăng</b>.<br>
  Ô “Điểm chiến dịch 61” góc trên cứ kệ — đó là Facebook rủ bật mấy thứ tự động
  mà mình cố tình không bật.
</div>
"""


def main():
    ra = os.path.join(GOC, 'quang-cao', 'anh')
    os.makedirs(ra, exist_ok=True)
    duong = os.path.join(ra, 'huong-dan-dich-den.jpg')
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
