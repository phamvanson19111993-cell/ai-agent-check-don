#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dung ban xem thu de dang len link cho anh Son xem.

Trang that (index.html) la mot file HTML day du. Ben dang link thi tu boc
lai phan <html>/<head>/<body>, nen ban xem thu phai bo cac the do di,
chi giu <title>, phong chu, <style> va phan than trang.

    python3 lady-giam-mo/tao-ban-xem-thu.py

Ra file xem-thu.html cung thu muc. File nay khong theo doi trong git —
sinh lai bat cu luc nao tu index.html.

Trang that de anh o thu muc images/ cho nhe. Ban xem thu la mot file gui
di nen phai nhung anh vao trong, vi vay no nang hon trang that nhieu.

Hai thu KHONG chay trong ban xem thu, nhung chay binh thuong tren trang that:
  · nut "Luu ma QR" — ben dang link khong cho trang tu tai file ve may
  · pixel Facebook  — ben dang link chan goi ra connect.facebook.net
"""
import base64
import pathlib
import re
import sys

GOC = pathlib.Path(__file__).resolve().parent


def nhung_anh(ra: str) -> str:
    """Nhet anh vao thang trong file.

    Trang that de anh o thu muc images/ cho nhe va cho trinh duyet nho anh.
    Nhung ban xem thu chi la MOT file gui di, khong mang theo thu muc nao,
    nen duong dan images/... se hong. Vi vay ban xem thu phai nhung anh vao."""
    anh = GOC / 'images'
    for f in sorted(anh.glob('*.webp')):
        duong = 'images/' + f.name
        if duong not in ra:
            continue
        uri = 'data:image/webp;base64,' + base64.b64encode(f.read_bytes()).decode()
        ra = ra.replace(duong, uri)
    assert 'images/' not in ra, 'con duong dan anh chua nhung duoc'
    return ra


def dung(trang: pathlib.Path) -> str:
    s = trang.read_text(encoding='utf-8')
    dau = s[s.index('<title>'):s.index('</head>')]
    than = s[s.index('<body>') + len('<body>'):s.rindex('</body>')]

    # The meta va canonical nam trong than trang thi vo nghia, bo di
    dau = re.sub(r'\s*<meta[^>]*>', '', dau)
    dau = re.sub(r'\s*<link rel="canonical"[^>]*>', '', dau)

    ra = dau.rstrip() + '\n' + than.strip() + '\n'
    ra = nhung_anh(ra)

    thap = ra.lower()
    for the in ['<!doctype', '<html', '</html>', '<head>', '</head>', '<body', '</body>']:
        assert the not in thap, 'con sot the boc: ' + the
    assert '<title>' in ra, 'mat tieu de trang'
    assert 'body{margin:0;background:' in ra, \
        'body phai tu dat mau nen, khong thi no muon nen cua ben dang link'
    return ra


if __name__ == '__main__':
    ra = dung(GOC / 'index.html')
    out = GOC / 'xem-thu.html'
    out.write_text(ra, encoding='utf-8')
    print('%s — %d KB' % (out.name, len(ra.encode()) / 1024))
    sys.exit(0)
