#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tu kiem trang tren trinh duyet that TRUOC KHI day len.

Moi lan day code la sua thang trang khach dang xem, khong co ban nhap.
Chay file nay truoc, xanh het roi hay day.

    pip install playwright
    python3 lady-giam-mo/kiem-trang.py
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

GOC = pathlib.Path(__file__).resolve().parent
TRANG = GOC / 'index.html'
CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

loi, dat = [], []


def ghi(ok, ten, ct=''):
    (dat if ok else loi).append(ten)
    print(('  OK  ' if ok else ' HỎNG ') + ten + (' — ' + ct if ct else ''))


def mo(pw):
    kw = {'executable_path': CHROME} if pathlib.Path(CHROME).exists() else {}
    return pw.chromium.launch(**kw)


def bat_loi(pg):
    """Gom loi JavaScript. Bo qua loi mang: may chu nay bi chan ra Internet
    nen phong chu Google va pixel Facebook khong tai duoc."""
    ds = []
    pg.on('pageerror', lambda e: ds.append(str(e)))
    pg.on('console', lambda m: ds.append(m.text)
          if (m.type == 'error' and 'net::ERR' not in m.text) else None)
    return ds


def dien_phieu(pg):
    pg.fill('#ten', 'Nguyễn Văn Kiểm')
    pg.fill('#sdt', '0912345678')
    pg.fill('#diachi', 'Xóm 5, Yên Định, Hải Hậu, Nam Định')


def ban_tin(pg):
    return pg.evaluate("decodeURIComponent(document.querySelector('.don-chinh')"
                       ".href.split('text=')[1])")


def kiem_trang(br, rong):
    print('\n=== TRANG · màn hình %dpx ===' % rong)
    pg = br.new_page(viewport={'width': rong, 'height': 900})
    ljs = bat_loi(pg)
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(700)

    ghi(not ljs, 'không lỗi JavaScript', '; '.join(ljs[:2]))
    tran = pg.evaluate('() => document.documentElement.scrollWidth'
                       ' - document.documentElement.clientWidth')
    ghi(tran <= 1, 'không tràn ngang', 'dư ra %dpx' % tran)

    # Phieu chi con ba o de dien
    o = pg.locator('#lead-form input[type="text"], #lead-form input[type="tel"], '
                   '#lead-form textarea')
    ghi(o.count() == 3, 'phiếu chỉ còn ba ô: họ tên, số điện thoại, địa chỉ',
        str(o.count()) + ' ô')
    ghi(pg.locator('#lead-form input[name="cach_tra"]').count() == 0,
        'không còn ô chọn cách thanh toán')
    ghi(pg.locator('.qr-card, .pay').count() == 0, 'không còn khối chuyển khoản')

    # Bai kiem tra
    pg.click('#bat-dau')
    pg.wait_for_timeout(300)
    for i in range(6):
        pg.locator('#q-opts .qopt').nth(2 if i % 2 else 1).click()
        pg.wait_for_timeout(110)
    ghi(pg.locator('#q-result').is_visible(), 'bài kiểm tra ra kết quả',
        pg.locator('#score-n').inner_text() + '/12 điểm')
    ghi(pg.locator('#chan-doan').is_visible(), 'có đoạn chẩn đoán nhóm nguyên nhân')
    ghi(pg.locator('#advice .adv').count() > 0, 'có tư vấn theo từng câu')
    ghi(pg.locator('.chot-quiz').is_visible(), 'làm xong bài thì hiện khối chốt')
    ghi(pg.input_value('#tuKiem') != '', 'kết quả bài kiểm chạy vào đơn')
    ghi(pg.locator('#ket-qua-don').is_visible(), 'phiếu đặt hàng nhắc lại kết quả')

    # Dat thu mot don
    dien_phieu(pg)
    pg.evaluate('window.__fb = []; window.fbq = function(a,b,c){ window.__fb.push([a,b,c]); };')
    pg.click('button[type="submit"]')
    pg.wait_for_timeout(900)
    ghi(pg.locator('#ok-msg.on').count() == 1, 'gửi đơn xong hiện khối xác nhận')

    tin = ban_tin(pg)
    ghi('Xóm 5, Yên Định, Hải Hậu, Nam Định' in tin, 'đơn mang đúng địa chỉ khách gõ')
    ghi('Nhắc trước khi hết gói: Có' in tin, 'đơn ghi khách đồng ý cho gọi nhắc')
    ghi('Chuyển khoản' not in tin and 'Đặt cọc' not in tin,
        'bản tin không còn nhắc chuyện chuyển khoản')
    ghi(pg.locator('#ok-msg .don-nut a').count() >= 4,
        'có đủ bốn nút Messenger · Zalo · SMS · Gọi')
    pg.close()


def kiem_ban_hang(br):
    print('\n=== KHỐI BÁN HÀNG & BẢNG GIÁ ===')
    pg = br.new_page(viewport={'width': 390, 'height': 900})
    ljs = bat_loi(pg)
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(700)

    ghi(not ljs, 'không lỗi JavaScript', '; '.join(ljs[:2]))
    ghi(pg.locator('#mua-nhanh .anh-goi').count() == 1, 'khối bán hàng có ảnh gói thật')
    ghi(pg.locator('#mua-nhanh .moc-nut').count() == 4, 'khối bán hàng có bốn nút mốc giá')

    # Moc chon san phai la moc RE NHAT, khong phai moc dat nhat. Khach vao tu
    # quang cao bam mot cai roi dien ba o la gui don — chon san moc 6,75 trieu
    # thi thanh bay, khong phai ban hang.
    ghi(pg.evaluate("() => document.querySelector('#chon-hop input:checked').value")
        .startswith('1 gói'), 'phiếu chọn sẵn mốc 1 gói, không phải mốc đắt nhất',
        pg.evaluate("() => document.querySelector('#chon-hop input:checked').value"))
    ghi(pg.evaluate("() => document.querySelector('#chon-hop .h-tem')"
                    ".closest('.hop-o').querySelector('.h-t').textContent").startswith('10 gói'),
        'nhãn Lợi nhất vẫn nằm ở mốc 10 gói để kéo khách lên')
    ghi(pg.locator('#mua-nhanh').bounding_box()['y'] < pg.locator('#van-de').bounding_box()['y'],
        'khối bán hàng nằm trên bài kiểm tra — bán thẳng, không bắt đọc hết mới mua')
    ghi(pg.locator('#dat-hang').bounding_box()['y'] < pg.locator('#van-de').bounding_box()['y'],
        'phiếu đặt hàng nằm trên bài kiểm tra')

    # Trang dich cho chien dich tra tien: khong duoc co link dan khach di
    # cho khac. Moi link ra ngoai la mot phan tien quang cao bi mat.
    ra = pg.evaluate("""() => { const nb = document.getElementById('noi-bo');
        return Array.from(document.querySelectorAll('a[href^=\"http\"]'))
          .filter(a => !nb.contains(a) && a.offsetParent !== null)
          .map(a => a.getAttribute('href')); }""")
    ghi(not ra, 'không link nào dẫn khách ra khỏi trang', '; '.join(ra[:3]))
    ghi(pg.locator('.steps-nav a').count() == 0, 'không có thanh mục lục để khách lạc đi')
    cta = pg.evaluate("() => Math.round(document.querySelector('.hero-jump')"
                      ".getBoundingClientRect().top + window.scrollY)")
    ghi(cta < 844, 'nút mua nằm trong màn hình đầu', str(cta) + 'px')
    ghi(pg.locator('.hero-jump').inner_text().strip().startswith('Xem giá'),
        'nút to nhất ở đầu trang là nút mua, không phải nút làm bài kiểm tra')

    bg = pg.locator('#bang-gia').inner_text()
    ghi(pg.locator('#bang-gia .quote table tbody tr').count() == 4, 'bảng báo giá đủ bốn mốc')
    ghi(all(x in bg for x in ['675.000đ', '1.269.000đ', '3.375.000đ', '6.750.000đ']),
        'đủ bốn giá đúng như bảng giá niêm yết 2026')
    ghi('30 ngày' in bg and '360 ngày' in bg, 'số ngày dùng tính từ liều 2 viên mỗi ngày')
    ghi('lợi nhất' in bg.lower(), 'có nhãn Lợi nhất')
    ghi('1.350.000đ' in bg, 'quà tặng ghi rõ trị giá bao nhiêu tiền')
    ghi(pg.locator('#bang-gia .icon-goi').count() == 4, 'mốc nào cũng có dãy biểu tượng gói')
    ghi(pg.evaluate("() => document.querySelectorAll('#bang-gia tbody tr:last-child"
                    " .icon-goi g').length") == 12, 'mốc 10 tặng 2 vẽ đủ 12 gói')

    dl = pg.locator('#dat-lai').inner_text()
    ghi(pg.locator('#dat-lai table tbody tr').count() == 4, 'bảng đặt lại đủ bốn mốc')
    ghi('12 lần' in dl and '1 lần' in dl, 'bảng đặt lại tính đúng số lần mỗi năm')

    # Bam nut moc o dau trang: vua chon so luong vua nhay xuong phieu
    pg.locator('#mua-nhanh .moc-nut').nth(3).click()
    pg.wait_for_timeout(900)
    ghi(pg.evaluate("() => document.querySelector('#chon-hop input:checked').value")
        .startswith('10 gói'), 'bấm nút mốc ở đầu trang thì phiếu chọn sẵn đúng mốc đó')
    ghi(pg.evaluate('() => document.activeElement && document.activeElement.id') == 'ten',
        'và con trỏ nhảy thẳng vào ô Họ tên')

    dien_phieu(pg)
    pg.evaluate('window.__fb = []; window.fbq = function(a,b,c){ window.__fb.push([a,b,c]); };')
    pg.click('button[type="submit"]')
    pg.wait_for_timeout(900)
    fb = pg.evaluate("window.__fb.filter(function(x){ return x[1] === 'Lead'; })")
    ghi(len(fb) == 1 and fb[0][2]['value'] == 6750000,
        'Lead báo đúng giá trị đơn', str(fb))
    ghi('10 gói — 6.750.000đ' in ban_tin(pg), 'đơn mang đúng mốc khách chọn')
    pg.close()


def kiem_hinh_va_do_dai(br):
    print('\n=== HÌNH MINH HOẠ & ĐỘ DÀI ===')
    pg = br.new_page(viewport={'width': 390, 'height': 900})
    pg.goto(TRANG.as_uri(), wait_until='load')
    pg.wait_for_timeout(700)

    ghi(pg.locator('figure.hinh').count() == 4, 'đủ bốn hình vẽ tay',
        str(pg.locator('figure.hinh').count()))
    ghi(pg.evaluate("""() => Array.from(document.querySelectorAll('figure.hinh svg'))
            .every(s => s.getAttribute('role') === 'img' && s.getAttribute('aria-label'))"""),
        'hình nào cũng có lời mô tả cho người không nhìn được')
    # Chu trong SVG phai dat co bang style noi tuyen; dat bang thuoc tinh thi
    # luat CSS de len va chu tran ra khoi khung — dung loi so 10 cua trang Q10.
    ghi(pg.evaluate("() => !document.querySelector('figure.hinh svg text[font-size]')"),
        'không đặt cỡ chữ SVG bằng thuộc tính (luật CSS sẽ đè lên)')
    tran = pg.evaluate("""() => { const x = [];
        document.querySelectorAll('figure.hinh svg').forEach((sv, i) => {
          const v = sv.getAttribute('viewBox').split(/\\s+/).map(Number);
          sv.querySelectorAll('text').forEach(t => { const b = t.getBBox();
            if (b.x < -1 || b.y < -1 || b.x + b.width > v[2] + 1 || b.y + b.height > v[3] + 1)
              x.push('hình ' + (i + 1) + ': ' + t.textContent.slice(0, 24)); }); });
        return x; }""")
    ghi(not tran, 'không chữ nào tràn khỏi khung hình', '; '.join(tran[:2]))

    ghi(pg.locator('.chot').count() == 3, 'có ba dải mời đặt hàng rải giữa trang')
    ghi(pg.evaluate("""() => Array.from(document.querySelectorAll('.chot'))
            .every(c => c.querySelector('a[href="#dat-hang"]') && c.querySelector('a[href^="tel:"]'))"""),
        'dải nào cũng có cả nút đặt hàng lẫn nút gọi')
    ghi(pg.locator('#nhac').is_checked(), 'ô nhắc trước khi hết gói mặc định có tích')

    # Trang phai ngan hon trang Q10 (5.683 chu / 32.791px), khong ke ghi chu noi bo
    do = pg.evaluate("""() => {
        const bo = new Set(['SCRIPT','STYLE','NOSCRIPT']);
        const nb = document.getElementById('noi-bo');
        let chu = '';
        const di = n => {
          if (n.nodeType === 3) { chu += n.nodeValue + ' '; return; }
          if (n.nodeType !== 1 || bo.has(n.tagName) || n === nb || n.hidden) return;
          if (getComputedStyle(n).display === 'none') return;
          n.childNodes.forEach(di);
        };
        di(document.body);
        return { tu: chu.trim().split(/\\s+/).filter(Boolean).length,
                 cao: document.documentElement.scrollHeight };
    }""")
    ghi(do['tu'] <= 5000, 'trang gọn hơn trang Q10 (5.683 chữ)', str(do['tu']) + ' chữ')
    ghi(do['cao'] <= 27000, 'đường cuộn ngắn hơn trang Q10 (32.791px)', str(do['cao']) + 'px')
    pg.close()


def main():
    with sync_playwright() as pw:
        br = mo(pw)
        kiem_trang(br, 390)
        kiem_trang(br, 1280)
        kiem_ban_hang(br)
        kiem_hinh_va_do_dai(br)
        br.close()
    print('\n===== %d đạt, %d hỏng =====' % (len(dat), len(loi)))
    for x in loi:
        print('  HỎNG: ' + x)
    return 1 if loi else 0


if __name__ == '__main__':
    sys.exit(main())
