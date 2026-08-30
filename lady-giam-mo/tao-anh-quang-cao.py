#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng ảnh quảng cáo 4:5 cho Ellagic Acid, theo đúng khuôn ba ảnh Q10 của Phòng 7.

Khuôn: ảnh sản phẩm ở trên, nền trắng ở dưới, chữ thưa —
   dòng nhỏ chữ hoa giãn ·  con số to  ·  "mỗi ngày"  ·  gạch ngang
   ·  hai dòng thân bài  ·  một viên thuốc chữ trắng nền đỏ.

Chữ trên ảnh chỉ được nói ĐÚNG câu nhãn cho phép: "Hỗ trợ giảm béo."
Không số cân, không số ngày giảm, không ảnh trước–sau.

Chạy:  python3 tao-anh-quang-cao.py
Ra:    quang-cao/anh/giam-mo-vuong.jpg   (1080×1350)
"""

import base64
import os
import sys

import cv2

GOC = os.path.dirname(os.path.abspath(__file__))

# File này nằm ở hai chỗ: trong kho trang bán (ảnh ở images/) và trong kho
# website sonsongkhoe.com (ảnh ở giam-mo/images/, vì images/ trên đó là của Q10).
ANH_GOI = next(
    (d for d in (os.path.join(GOC, 'images', 'goi-san-pham.webp'),
                 os.path.join(GOC, 'giam-mo', 'images', 'goi-san-pham.webp'))
     if os.path.exists(d)),
    os.path.join(GOC, 'images', 'goi-san-pham.webp'))

# Khung chứa cái túi trong ảnh gốc 700×1171, chừa lề cho thoáng.
# Mép trên đặt ở 272: cành cây phía trên hết ở khoảng dòng 285, cắt cao hơn
# nữa là lôi cả cành tối vào góc ảnh quảng cáo.
CAT = (100, 272, 605, 1045)   # trai, tren, phai, duoi

DO = '#BE1B10'                # do lay tu chinh bao bi san pham

# --doc  -> khổ 9:16 (1080×1920) cho Reels và Story, chiếm hết màn hình điện thoại
# không ghi -> khổ 4:5 (1080×1350) cho bảng tin, y như ba ảnh Q10 của Phòng 7
DOC = '--doc' in sys.argv

# ── Chữ trên ảnh ────────────────────────────────────────────────────────────
KICKER  = 'ELLAGIC ACID · AFC NHẬT BẢN'
SO_TIEN = '22.500đ'
DUOI_SO = 'mỗi ngày'
THAN_1  = 'Hỗ trợ giảm béo. Ngày hai viên với nước.'
THAN_2  = 'Túi nhôm 60 viên, dùng đúng 30 ngày.'
VIEN    = 'Xem nhãn và bảng giá trước khi mua'

# Câu hook trên đầu ảnh dọc. Chỉ có ở khổ 9:16, vì khổ đó có chỗ.
#
# Ogilvy: "Nói sự thật, nhưng làm cho sự thật hấp dẫn." Cả ngách giảm cân đang
# gào số cân và số ngày. Câu mạnh nhất còn lại — và là câu duy nhất mình được
# phép nói — chính là NÓI THẬT. Nó vừa chặn đứng ngón tay đang lướt, vừa hợp
# luật, vừa dựng sẵn lý do để tin phần còn lại của bài.
#
# Không dùng câu chỉ thẳng vào thân thể người xem ("bạn đang béo…") — Meta cấm.
HOOK_1  = 'Không hứa'
HOOK_2  = 'xuống mấy cân.'
HOOK_3  = 'Nhãn ghi sao, bên em nói vậy.'


def anh_nen_base64():
    """Cắt lấy cái túi, đặt giữa một nền kem phẳng đúng màu nền thật của tấm ảnh.

    Nền lấy màu TRUNG VỊ của dải bên trái cái túi — chỗ đó là tường kem trơn,
    không dính cành cây phía trên nên không bị xỉn góc. Hai mép trái phải của
    miếng cắt được vuốt mờ dần sang nền để không thấy đường viền hộp.
    """
    import numpy as np

    im = cv2.imread(ANH_GOI)
    if im is None:
        sys.exit('Khong doc duoc %s' % ANH_GOI)
    t, tr, p, d = CAT
    tui = im[tr:d, t:p]

    # Mau nen lay tu chinh hai mep cua mieng cat, phan nua tren — cho do la
    # tuong kem tron, chua toi cai chan nen thuy tinh lan mat ban mau nau.
    # Trung vi chu khong phai trung binh, de mot vai diem la khong keo mau di.
    ria = np.vstack([tui[10:500, 0:22].reshape(-1, 3),
                     tui[10:500, -22:].reshape(-1, 3)])
    nen = np.median(ria, axis=0)

    cao, rong, vuot = (900 if DOC else 620), 1080, 70
    ty = cao / tui.shape[0]
    tui = cv2.resize(tui, (int(tui.shape[1] * ty), cao), interpolation=cv2.INTER_AREA)

    khung = np.full((cao, rong, 3), nen, dtype=np.float32)
    x = (rong - tui.shape[1]) // 2

    # Mat na: giua bang 1, hai mep giam dan ve 0 de hoa vao nen.
    mn = np.ones(tui.shape[1], dtype=np.float32)
    n = min(vuot, tui.shape[1] // 2)
    mn[:n] = np.linspace(0, 1, n)
    mn[-n:] = np.linspace(1, 0, n)
    mn = mn[None, :, None]

    o = khung[:, x:x + tui.shape[1]]
    khung[:, x:x + tui.shape[1]] = tui.astype(np.float32) * mn + o * (1 - mn)

    ok, buf = cv2.imencode('.jpg', khung.astype(np.uint8),
                           [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    if not ok:
        sys.exit('Khong ma hoa duoc anh nen')
    print('Nen  : %d×%d, mau kem RGB %s, tui rong %dpx'
          % (rong, cao, tuple(int(v) for v in nen[::-1]), tui.shape[1]))
    return base64.b64encode(buf.tobytes()).decode('ascii')


TRANG = """<!doctype html><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1080px;height:1350px;background:#fff;
       font-family:"Liberation Sans","DejaVu Sans",sans-serif;
       -webkit-font-smoothing:antialiased}
  .anh{width:1080px;height:620px;object-fit:cover;display:block}
  .duoi{height:730px;display:flex;flex-direction:column;align-items:center;
        justify-content:center;text-align:center;padding:0 70px}
  .kicker{font-size:31px;font-weight:700;letter-spacing:.13em;color:#8A8A8A}
  .so{font-size:150px;font-weight:700;color:#1A1A1A;line-height:1.05;
      letter-spacing:-.02em;margin-top:26px}
  .ngay{font-size:46px;color:#8A8A8A;margin-top:2px}
  hr{width:340px;border:0;border-top:2px solid #DDD;margin:40px 0}
  .than{font-size:40px;color:#1A1A1A;line-height:1.5}
  .vien{margin-top:44px;background:%s;color:#fff;font-size:38px;font-weight:700;
        padding:26px 54px;border-radius:999px}
</style>
<img class="anh" src="data:image/jpeg;base64,%s">
<div class="duoi">
  <div class="kicker">%s</div>
  <div class="so">%s</div>
  <div class="ngay">%s</div>
  <hr>
  <div class="than">%s<br>%s</div>
  <div class="vien">%s</div>
</div>"""


# Khổ 9:16 cho Reels và Story. Ba tầng: câu hook chặn ngón tay ở trên,
# ảnh sản phẩm ở giữa, giá và lời mời ở dưới.
# Chừa 14% trên và 20% dưới cho phần giao diện Reels che — theo SOP Phòng 7.
TRANG_DOC = """<!doctype html><meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{width:1080px;height:1920px;background:#fff;
       font-family:"Liberation Sans","DejaVu Sans",sans-serif;
       -webkit-font-smoothing:antialiased;display:flex;flex-direction:column}
  .tren{height:490px;padding:150px 70px 0;text-align:center}
  .hook{font-size:82px;font-weight:700;line-height:1.12;letter-spacing:-.02em;
        color:#1A1A1A}
  .hook em{font-style:normal;color:%s}
  .hook-phu{font-size:38px;color:#6B6B6B;margin-top:26px;line-height:1.4}
  .anh{width:1080px;height:900px;object-fit:cover;display:block;flex:0 0 auto}
  .duoi{flex:1;display:flex;flex-direction:column;align-items:center;
        justify-content:center;text-align:center;padding:40px 70px 260px}
  .kicker{font-size:29px;font-weight:700;letter-spacing:.13em;color:#8A8A8A}
  .so{font-size:132px;font-weight:700;color:#1A1A1A;line-height:1.05;
      letter-spacing:-.02em;margin-top:14px}
  .ngay{font-size:42px;color:#8A8A8A}
  .than{font-size:36px;color:#1A1A1A;line-height:1.45;margin-top:22px}
  /* Khong ve nut o kho doc. Story va Reels da co san nut "Xem chi tiet" cua
     Facebook o dung cho do — ve them nut cua minh la hai cai dam vao nhau,
     va SOP Phong 7 muc 1 cam ve nut gia dang nut bam cua Facebook. */
</style>
<div class="tren">
  <div class="hook">%s<br><em>%s</em></div>
  <div class="hook-phu">%s</div>
</div>
<img class="anh" src="data:image/jpeg;base64,%s">
<div class="duoi">
  <div class="kicker">%s</div>
  <div class="so">%s</div>
  <div class="ngay">%s</div>
  <div class="than">%s<br>%s</div>
</div>"""


def main():
    from playwright.sync_api import sync_playwright

    ra = os.path.join(GOC, 'quang-cao', 'anh')
    os.makedirs(ra, exist_ok=True)
    duong = os.path.join(ra, 'giam-mo-doc.jpg' if DOC else 'giam-mo-vuong.jpg')
    cao_khung = 1920 if DOC else 1350

    nen64 = anh_nen_base64()
    if DOC:
        html = TRANG_DOC % (DO, HOOK_1, HOOK_2, HOOK_3, nen64,
                            KICKER, SO_TIEN, DUOI_SO, THAN_1, THAN_2)
    else:
        html = TRANG % (DO, nen64, KICKER, SO_TIEN, DUOI_SO,
                        THAN_1, THAN_2, VIEN)
    tam = os.path.join(ra, '_tam.html')
    with open(tam, 'w', encoding='utf-8') as f:
        f.write(html)

    # Cung duong dan trinh duyet ma kiem-trang.py dung, khoi phai tai lai
    CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
    with sync_playwright() as p:
        br = p.chromium.launch(**({'executable_path': CHROME}
                                  if os.path.exists(CHROME) else {}))
        tr = br.new_page(viewport={'width': 1080, 'height': cao_khung},
                         device_scale_factor=1)
        tr.goto('file://' + tam)
        tr.wait_for_timeout(400)
        tr.screenshot(path=duong.replace('.jpg', '.png'))
        br.close()

    im = cv2.imread(duong.replace('.jpg', '.png'))
    cv2.imwrite(duong, im, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    os.remove(duong.replace('.jpg', '.png'))
    os.remove(tam)
    print('Xong : %s — %d×%d, %d KB'
          % (duong, im.shape[1], im.shape[0], os.path.getsize(duong) // 1024))


if __name__ == '__main__':
    main()
