#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng ảnh "khách nhìn thấy gì" — bài quảng cáo y như trên bảng tin Facebook.

Lấy chữ THẲNG từ hồ sơ sản phẩm, không chép tay lại. Nhờ vậy ảnh xem trước
không bao giờ lệch với thứ thật sự được đẩy lên Facebook — sửa hồ sơ rồi chạy
lại là ảnh tự đúng theo.

    python3 xem-quang-cao.py giam-mo 1

Ra: quang-cao/anh/xem-truoc-giam-mo-nhom1.jpg
"""

import base64
import html
import importlib.util as iu
import os
import re
import sys

GOC = os.path.dirname(os.path.abspath(__file__))
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

TEN_TRANG = 'DiLiM Supplement'
# Facebook trên điện thoại cắt văn bản chính ở khoảng 125 ký tự rồi hiện
# "Xem thêm". Để đúng con số thật chứ không để rộng cho ảnh xem trước đẹp —
# nhìn ra được bao nhiêu phần bài viết KHÔNG ai đọc mới là cái đáng biết.
CAT_O = 125


def nap(ten):
    d = os.path.join(GOC, 'san-pham', ten.replace('-', '_') + '.py')
    if not os.path.exists(d):
        sys.exit('Khong co ho so san pham %r' % ten)
    s = iu.spec_from_file_location('sp', d)
    m = iu.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def anh64(duong):
    with open(duong, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')


def than_bai(chu):
    """Chia thành đoạn, và đánh dấu chỗ Facebook sẽ cắt."""
    doan = [d for d in chu.split('\n\n') if d.strip()]
    ra, da_dem, cat_roi = [], 0, False
    for d in doan:
        if cat_roi:
            ra.append(('mo', d))
            continue
        da_dem += len(d)
        ra.append(('ro', d))
        if da_dem > CAT_O:
            cat_roi = True
    return ra


def dong(d):
    """Đoạn có gạch đầu dòng thì giữ nguyên xuống dòng."""
    return '<br>'.join(html.escape(x) for x in d.split('\n'))


TRANG = """<!doctype html><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1080px;background:#F0F2F5;padding:36px;
       font-family:"Liberation Sans","DejaVu Sans",sans-serif}
  .bai{background:#fff;border-radius:16px;overflow:hidden;
       box-shadow:0 2px 10px rgba(0,0,0,.10)}
  .dau{display:flex;align-items:center;gap:16px;padding:22px 24px 14px}
  .ava{width:72px;height:72px;border-radius:50%%;background:#BE1B10;color:#fff;
       font-size:32px;font-weight:700;display:flex;align-items:center;
       justify-content:center;flex:0 0 auto}
  .ten{font-size:29px;font-weight:700;color:#050505}
  .tt{font-size:24px;color:#65676B;margin-top:3px}
  .than{padding:4px 24px 18px;font-size:27px;line-height:1.45;color:#050505;
        white-space:pre-wrap}
  .than p{margin:0 0 18px}
  .than p.mo{color:#BCC0C4}
  .xem-them{color:#65676B;font-weight:600}
  .anh{width:100%%;display:block}
  .the{display:flex;align-items:center;gap:18px;background:#F0F2F5;
       padding:20px 24px;border-top:1px solid #E4E6EB}
  .the-chu{flex:1;min-width:0}
  .mien{font-size:22px;color:#65676B;text-transform:uppercase;letter-spacing:.03em}
  .tieu-de{font-size:30px;font-weight:700;color:#050505;margin-top:4px;line-height:1.25}
  .mo-ta{font-size:23px;color:#65676B;margin-top:5px;line-height:1.3}
  .nut{background:#E4E6EB;color:#050505;font-size:25px;font-weight:700;
       padding:16px 26px;border-radius:8px;white-space:nowrap;flex:0 0 auto}
  .cuoi{display:flex;justify-content:space-around;padding:14px 0;
         border-top:1px solid #E4E6EB;color:#65676B;font-size:26px;font-weight:600}
  .ghi{margin-top:26px;font-size:22px;color:#65676B;line-height:1.5}
</style>
<div class="bai">
  <div class="dau">
    <div class="ava">D</div>
    <div><div class="ten">%s</div><div class="tt">Được tài trợ · 🌐</div></div>
  </div>
  <div class="than">%s</div>
  <img class="anh" src="data:image/jpeg;base64,%s">
  <div class="the">
    <div class="the-chu">
      <div class="mien">%s</div>
      <div class="tieu-de">%s</div>
      <div class="mo-ta">%s</div>
    </div>
    <div class="nut">Tìm hiểu thêm</div>
  </div>
  <div class="cuoi"><span>👍 Thích</span><span>💬 Bình luận</span><span>↗ Chia sẻ</span></div>
</div>
<div class="ghi">%s</div>"""


def main():
    ten_sp = sys.argv[1] if len(sys.argv) > 1 else 'giam-mo'
    so = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    m = nap(ten_sp)
    n = m.NHOM[so - 1]

    mien = re.sub(r'^https?://', '', m.LINK).split('/')[0]
    doan = than_bai(n['chu'])
    than = ''
    for i, (lop, d) in enumerate(doan):
        them = ' <span class="xem-them">… Xem thêm</span>' \
            if lop == 'ro' and i + 1 < len(doan) and doan[i + 1][0] == 'mo' else ''
        than += '<p class="%s">%s%s</p>' % (lop, dong(d), them)

    gioi = {1: 'nam', 2: 'nữ'}.get(n.get('gioi'), 'nam và nữ')
    ghi = ('%s · %s %d–%d tuổi · toàn quốc · sở thích để trống · '
           '%s đ mỗi ngày<br>Chữ mờ là phần khách phải bấm “Xem thêm” mới đọc được.'
           % (n['ten'], gioi, n['tuoi'][0], n['tuoi'][1], format(m.NGAN_SACH, ',')))

    ra = os.path.join(GOC, 'quang-cao', 'anh')
    os.makedirs(ra, exist_ok=True)
    duong = os.path.join(ra, 'xem-truoc-%s-nhom%d.jpg' % (ten_sp, so))
    tam = duong.replace('.jpg', '.html')
    with open(tam, 'w', encoding='utf-8') as f:
        f.write(TRANG % (html.escape(TEN_TRANG), than,
                         anh64(os.path.join(GOC, m.ANH_QC)),
                         html.escape(mien), html.escape(n['tieu_de']),
                         html.escape(n['mo_ta']), ghi))

    from playwright.sync_api import sync_playwright
    import cv2
    with sync_playwright() as p:
        br = p.chromium.launch(**({'executable_path': CHROME}
                                  if os.path.exists(CHROME) else {}))
        tr = br.new_page(viewport={'width': 1080, 'height': 1200})
        tr.goto('file://' + tam)
        tr.wait_for_timeout(400)
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
