#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tu kiem trang tren trinh duyet that TRUOC KHI day len.

Moi lan day code la sua thang trang khach dang xem, khong co ban nhap.
Nen chay file nay truoc, xanh het roi hay day.

    pip install playwright opencv-python-headless numpy segno
    python3 lady-giam-mo/kiem-trang.py

Kiem ba duong:
  1 · trang that (BANG_GIA con trong) o 390px va 1280px
  2 · duong bang gia — dung ban thu co gia gia dinh, khong dung file that
  3 · ma QR — quet lai anh PNG ma trinh duyet ve ra, dung nhu app ngan hang
"""
import base64
import importlib.util
import pathlib
import re
import sys
import tempfile

import cv2
import numpy as np
from playwright.sync_api import sync_playwright

GOC   = pathlib.Path(__file__).resolve().parent
TRANG = GOC / 'index.html'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

loi, dat = [], []


def ghi(ok, ten, ct=''):
    (dat if ok else loi).append(ten)
    print(('  OK  ' if ok else ' HỎNG ') + ten + (' — ' + ct if ct else ''))


def mo_trinh_duyet(pw):
    kw = {'executable_path': CHROME} if pathlib.Path(CHROME).exists() else {}
    return pw.chromium.launch(**kw)


def bat_loi(pg):
    """Gom loi JavaScript. Bo qua loi mang: may chu dung o day co the bi chan
    ra Internet nen font Google va pixel Facebook khong tai duoc."""
    ds = []
    pg.on('pageerror', lambda e: ds.append(str(e)))
    pg.on('console', lambda m: ds.append(m.text)
          if (m.type == 'error' and 'net::ERR' not in m.text) else None)
    return ds


def dien_phieu(pg):
    pg.fill('#ten', 'Nguyễn Văn Kiểm')
    pg.fill('#sdt', '0912345678')
    for o, v in [('#tinh', 'Nam Định'), ('#huyen', 'Hải Hậu'),
                 ('#xa', 'Yên Định'), ('#thon', 'Xóm 5')]:
        pg.fill(o, v)


def ban_thu_co_gia():
    """Dung mot ban co gia gia dinh de kiem duong bang gia.
    Ban nay chi nam trong thu muc tam, khong bao gio duoc day len."""
    spec = importlib.util.spec_from_file_location('qr', GOC / 'tao-ma-qr.py')
    qr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qr)

    tien = [590000, 1150000, 3150000, 4900000]
    s = TRANG.read_text(encoding='utf-8')
    assert 'var QR_TIEN = {};' in s, \
        'index.html khong con cho de cam ma QR thu — xem lai da sua gi'
    s, n = re.subn(r'var BANG_GIA = \[.*?\];',
                   "var BANG_GIA = ["
                   "{hop:1,  gia:590000,  nhan:'Mua thử'},"
                   "{hop:2,  gia:1150000},"
                   "{hop:6,  gia:3150000, loi_nhat:true, qua:'Quà thử', qua_tien:675000},"
                   "{hop:10, gia:4900000}];", s, flags=re.S)
    assert n == 1, 'khong tim thay BANG_GIA de thay'
    s = s.replace('var VIEN_MOI_NGAY = 0;', 'var VIEN_MOI_NGAY = 2;')
    s = s.replace('var QR_TIEN = {};',
                  'var QR_TIEN = {' + ', '.join(
                      '"%d": "%s"' % (t, qr.ra_svg(t)) for t in tien) + '};')
    f = pathlib.Path(tempfile.mkdtemp()) / 'thu-co-gia.html'
    f.write_text(s, encoding='utf-8')
    return f


def quet(png_url):
    """Doc mot anh PNG dang data: giong het app ngan hang quet ma."""
    raw = base64.b64decode(png_url.split(',', 1)[1])
    img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_GRAYSCALE)
    txt, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return txt


def so_tien_trong_ma(p):
    """O 54 cua chuan EMVCo la so tien."""
    m = re.search(r'54(\d{2})', p or '')
    if not m:
        return None
    n = int(m.group(1))
    return int(p[m.end():m.end() + n])


def kiem_trang_that(br):
    for rong in (390, 1280):
        print('\n=== TRANG THẬT · màn hình %dpx ===' % rong)
        pg = br.new_page(viewport={'width': rong, 'height': 900})
        ljs = bat_loi(pg)
        pg.goto(TRANG.as_uri(), wait_until='load')
        pg.wait_for_timeout(600)

        ghi(not ljs, 'không lỗi JavaScript', '; '.join(ljs[:2]))
        tran = pg.evaluate('() => document.documentElement.scrollWidth'
                           ' - document.documentElement.clientWidth')
        ghi(tran <= 1, 'không tràn ngang', 'dư ra %dpx' % tran)

        pg.click('#bat-dau')
        pg.wait_for_timeout(300)
        for i in range(6):
            pg.locator('#q-opts .qopt').nth(2 if i % 2 else 1).click()
            pg.wait_for_timeout(120)
        ghi(pg.locator('#q-result').is_visible(), 'bài kiểm tra ra kết quả',
            pg.locator('#score-n').inner_text() + '/12 điểm')
        ghi(pg.locator('#chan-doan').is_visible(), 'có đoạn chẩn đoán nhóm nguyên nhân')
        ghi(pg.locator('#story-box').is_visible(), 'có câu chuyện hợp hồ sơ')
        ghi(pg.locator('#advice .adv').count() > 0, 'có tư vấn theo từng câu')
        ghi(pg.input_value('#tuKiem') != '', 'kết quả bài kiểm chạy vào đơn')

        ghi(pg.locator('.pay .qr-card img.qr').count() == 1,
            'mã QR tĩnh đã đổi sang PNG (điện thoại bấm giữ lưu được)')
        ghi(pg.locator('.pay .qr-card a.qr-tai').count() == 1, 'có nút Lưu mã QR')

        dien_phieu(pg)
        pg.click('button[type="submit"]')
        pg.wait_for_timeout(900)
        ghi(pg.locator('#ok-msg.on').count() == 1, 'gửi đơn xong hiện khối xác nhận')
        ghi(pg.locator('#ok-msg .ck-hang').count() >= 3, 'có các hàng chép số tài khoản')
        ghi(pg.locator('#ok-msg .ck-qr img.qr').count() >= 1, 'mã QR trong đơn cũng là PNG')
        ghi(pg.locator('#ok-msg .ck-xong').count() == 1, 'có nút Tôi đã chuyển khoản xong')
        pg.close()


def kiem_bang_gia(br, ban_thu):
    print('\n=== ĐƯỜNG BẢNG GIÁ · bản thử có giá giả định ===')
    pg = br.new_page(viewport={'width': 390, 'height': 900})
    ljs = bat_loi(pg)
    pg.goto(ban_thu.as_uri(), wait_until='load')
    pg.wait_for_timeout(600)

    ghi(not ljs, 'không lỗi JavaScript', '; '.join(ljs[:2]))
    bg0 = pg.locator('#bang-gia').inner_text()
    ghi(pg.locator('#bang-gia .quote table tbody tr').count() == 4,
        'bảng báo giá đủ 4 mốc 1 · 2 · 6 · 10 hộp')
    ghi('30 ngày' in bg0 and '300 ngày' in bg0, 'số ngày dùng tự tính từ liều trên nhãn')
    ghi(pg.locator('#bang-gia .fill').count() == 0, 'lời báo "chưa có bảng giá" đã tắt')
    bg = pg.locator('#bang-gia').inner_text()
    ghi('lợi nhất' in bg.lower(), 'có nhãn Lợi nhất')
    ghi('675.000đ' in bg, 'quà tặng ghi rõ trị giá bao nhiêu tiền')
    ghi(pg.locator('#chon-hop .hop-o').count() == 5, 'thẻ chọn số lượng: 4 mốc + 1 chưa quyết')
    ghi(pg.locator('.offer .price').inner_text() == '590.000đ', 'dòng giá đầu ô đặt hàng đổi theo')
    ghi(pg.locator('#chon-hop input:checked').count() == 1, 'luôn có đúng một mốc được chọn sẵn')

    # Khach chon CHUYEN KHOAN DU — day la cho trang Q10 tung hong ba lan
    dien_phieu(pg)
    pg.locator('#chon-tra-form label').nth(1).click()
    pg.evaluate('window.__mua = []; window.fbq = function(a,b,c){ window.__mua.push([a,b,c]); };')
    pg.click('button[type="submit"]')
    pg.wait_for_timeout(1000)

    ghi(pg.locator('#ok-msg .ck-du').first.is_visible()
        and not pg.locator('#ok-msg .ck-coc').first.is_visible(),
        'chọn trả đủ thì hiện khối trả đủ ngay từ đầu, không đợi bấm lại')
    tin = pg.evaluate("decodeURIComponent(document.querySelector('.don-chinh')"
                      ".href.split('text=')[1])")
    ghi('CHUYỂN KHOẢN ĐỦ' in tin and 'ĐẶT CỌC' not in tin,
        'bản tin Messenger khớp đúng cách trả khách chọn')

    pg.locator('#ok-msg .ck-xong').click()
    pg.wait_for_timeout(300)
    mua = pg.evaluate("window.__mua.filter(function(x){ return x[1] === 'Purchase'; })")
    ghi(len(mua) == 1 and mua[0][2]['value'] == 3150000,
        'Purchase báo GIÁ TRỊ ĐƠN, không phải tiền cọc', str(mua))

    ma = {}
    anh = pg.locator('#ok-msg .ck-qr img.qr')
    for i in range(anh.count()):
        lop = anh.nth(i).evaluate("e => e.closest('.ck-qr').className")
        ma['du' if 'ck-du' in lop else 'coc'] = so_tien_trong_ma(quet(anh.nth(i).get_attribute('src')))
    ghi(ma.get('du') == 3150000, 'quét mã "chuyển khoản đủ" ra đúng 3.150.000đ', str(ma))
    ghi(ma.get('coc') == 200000, 'quét mã "đặt cọc" ra đúng 200.000đ', str(ma))
    pg.close()


def kiem_ma_qr_tinh(br):
    print('\n=== MÃ QR TĨNH · quét lại như app ngân hàng ===')
    pg = br.new_page(viewport={'width': 390, 'height': 900})
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(800)
    p = quet(pg.locator('.pay .qr-card img.qr').get_attribute('src'))
    ghi(p.startswith('000201') and 'A000000727' in p, 'là mã VietQR hợp lệ')
    ghi(so_tien_trong_ma(p) == 200000, 'quét ra đúng tiền cọc 200.000đ', str(so_tien_trong_ma(p)))
    ghi('38691388888' in p and '970423' in p, 'đúng số tài khoản và mã ngân hàng TPBank')
    pg.close()



def kiem_chuyen_doi(br):
    """Nhung thu them vao de khach de mua hon — moi cai deu phai chay dung."""
    print('\n=== ĐƯỜNG CHUYỂN ĐỔI ===')
    pg = br.new_page(viewport={'width': 390, 'height': 900})
    ljs = bat_loi(pg)
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(600)

    ghi(pg.locator('.ba-so div').count() == 3, 'đầu trang có ba con số kiểm chứng được')
    ghi(not pg.locator('.chot-quiz').is_visible(), 'khối chốt chưa hiện khi chưa làm bài')
    ghi(not pg.locator('#ket-qua-don').is_visible(), 'phiếu chưa nhắc kết quả khi chưa làm bài')

    # phieu hai buoc: luc dau chi hoi ten va so dien thoai
    ghi('gon' in (pg.get_attribute('#lead-form', 'class') or ''), 'phiếu mở ra ở dạng gọn')
    ghi(not pg.locator('#tinh').is_visible(), 'khối địa chỉ đang ẩn')
    ghi(pg.evaluate("() => !document.getElementById('tinh').required"),
        'ô địa chỉ đang ẩn thì bỏ bắt buộc — nếu không, bấm Gửi sẽ đứng im không báo gì')

    pg.fill('#sdt', '0912345678')
    pg.wait_for_timeout(300)
    ghi(pg.locator('#tinh').is_visible(), 'điền số điện thoại xong thì khối địa chỉ hiện ra')
    ghi(pg.evaluate("() => document.getElementById('tinh').required"),
        'khối địa chỉ hiện ra thì bắt buộc được trả về')

    # bam Gui khi con dang gon cung phai mo khoi dia chi ra
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(400)
    pg.fill('#ten', 'Nguyễn Văn Kiểm')
    pg.click('button[type="submit"]')
    pg.wait_for_timeout(300)
    ghi(pg.locator('#tinh').is_visible(), 'bấm Gửi khi phiếu còn gọn thì địa chỉ mở ra')
    ghi(pg.locator('#ok-msg.on').count() == 0, 'đơn thiếu địa chỉ thì không gửi đi')

    # lam xong bai kiem tra: ket qua phai theo khach xuong toi phieu
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(400)
    pg.click('#bat-dau')
    pg.wait_for_timeout(300)
    for i in range(6):
        pg.locator('#q-opts .qopt').nth(2).click()
        pg.wait_for_timeout(120)
    ghi(pg.locator('.chot-quiz').is_visible(), 'làm xong bài thì hiện khối chốt')
    ghi(pg.locator('#ket-qua-don').is_visible()
        and '12/12' in pg.locator('#ket-qua-don').inner_text(),
        'phiếu đặt hàng nhắc lại đúng số điểm',
        pg.locator('#ket-qua-don').inner_text()[:60])
    ghi('12/12' in pg.locator('.dock .p').inner_text(),
        'thanh dưới màn hình đổi theo kết quả', pg.locator('.dock .p').inner_text()[:50])

    pg.click('#chot-de-so')
    pg.wait_for_timeout(800)
    ghi(pg.evaluate("() => document.activeElement && document.activeElement.id") == 'ten',
        'bấm "Để lại số" thì con trỏ nhảy thẳng vào ô Họ tên')

    # lam lai bai thi moi cho nhac ket qua phai xoa theo
    pg.locator('#q-again').click()
    pg.wait_for_timeout(300)
    ghi(not pg.locator('#ket-qua-don').is_visible(), 'làm lại bài thì phiếu xoá kết quả cũ')
    ghi('12/12' not in pg.locator('.dock .p').inner_text(), 'làm lại bài thì thanh dưới cũng xoá')

    ghi(not ljs, 'không lỗi JavaScript', '; '.join(ljs[:2]))
    pg.close()


def main():
    ban_thu = ban_thu_co_gia()
    with sync_playwright() as pw:
        br = mo_trinh_duyet(pw)
        kiem_trang_that(br)
        kiem_chuyen_doi(br)
        kiem_ma_qr_tinh(br)
        kiem_bang_gia(br, ban_thu)
        br.close()

    print('\n===== %d đạt, %d hỏng =====' % (len(dat), len(loi)))
    for x in loi:
        print('  HỎNG: ' + x)
    return 1 if loi else 0


if __name__ == '__main__':
    sys.exit(main())
