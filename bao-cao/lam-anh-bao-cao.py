#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng ảnh báo cáo Phòng 7 từ một file JSON.

    python3 bao-cao/lam-anh-bao-cao.py so-lieu.json bao-cao/anh/ten.png

JSON:
{
  "tieu_de": "PHÒNG 7 · LADY PAGE",
  "moc":     "28/08/2026 · 18h00",
  "chan":    "Lượt xem cộng dồn 344/1.515 — 23% quãng đường",
  "khoi": [
    {"loai":"k|v|d",           <- xanh (xong) / vàng (cần chú ý) / đỏ (hỏng)
     "ten":"1. Quảng cáo",
     "bang":[["Chi","111.014đ"],["Giá mỗi lượt","1.018đ"]],   (tuỳ chọn)
     "y":["câu 1","câu 2"],                                    (tuỳ chọn)
     "chu":"dòng nhỏ dưới cùng"}                               (tuỳ chọn)
  ]
}
Mỗi dòng trong "bang" là ["nhãn", "giá trị"] hoặc ["nhãn", "giá trị", "tot"|"xau"]
— thành phần thứ ba quyết định màu (xanh / đỏ). Không ghi thì để trắng.
"""
import json, sys, html, pathlib, subprocess, tempfile

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

CSS = """*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;background:#0f1620;color:#e8edf4;
 font:400 26px/1.5 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;padding:44px 48px 52px}
.top{display:flex;justify-content:space-between;align-items:baseline;
 border-bottom:3px solid #2a3a4d;padding-bottom:18px;margin-bottom:34px}
h1{font-size:40px;font-weight:800;letter-spacing:-.5px}
.top span{font-size:24px;color:#8ba0b8}
h2{font-size:29px;font-weight:800;margin:34px 0 16px;display:flex;gap:12px;align-items:center}
h2 i{font-style:normal;width:40px;height:40px;border-radius:10px;flex:0 0 40px;
 display:flex;align-items:center;justify-content:center;font-size:22px;font-weight:800}
.i-k{background:#123024;border:2px solid #2f7a52}
.i-v{background:#3a2a12;border:2px solid #9a6a1e}
.i-d{background:#2a1620;border:2px solid #a03a55}
.box{border-radius:14px;padding:22px 26px}
.b-k{background:#101f18;border-left:8px solid #2f9e63}
.b-v{background:#201a10;border-left:8px solid #d09420}
.b-d{background:#1e1218;border-left:8px solid #d0455f}
p{margin:9px 0}b{color:#fff}
.chu{font-size:23px;color:#9fb3c9;margin-top:14px}
table{width:100%;border-collapse:collapse;margin:4px 0;font-size:24px}
td{padding:11px 10px;border-bottom:1px solid #263447}
tr:last-child td{border-bottom:none}
td:first-child{color:#9fb3c9;width:52%}
td:last-child{font-weight:700;color:#fff}
.len{color:#4fd18b}.xuong{color:#ff7a90}
ul{margin:6px 0 6px 26px}li{margin:9px 0}
code{background:#1c2836;padding:3px 9px;border-radius:6px;font-size:22px;color:#8fd7ff}
.foot{margin-top:34px;border-top:3px solid #2a3a4d;padding-top:18px;
 font-size:23px;color:#8ba0b8;display:flex;justify-content:space-between;gap:30px}"""

DAU = {'k': '✓', 'v': '!', 'd': '✕'}


def o_gia_tri(v, mau=None):
    """mau: 'tot' -> xanh, 'xau' -> do, con lai -> trang.

    Khong doan mau tu dau + hay - nua: "-1.018d" la so tien am hay la giam
    thi khong the doan dung. Phai ghi ro o thanh phan thu ba cua dong.
    """
    t = html.escape(str(v))
    if mau == 'tot':
        return '<span class="len">%s</span>' % t
    if mau == 'xau':
        return '<span class="xuong">%s</span>' % t
    return t


def dung(d):
    r = ['<meta charset="utf-8"><style>%s</style>' % CSS,
         '<div class="top"><h1>%s</h1><span>%s</span></div>'
         % (html.escape(d.get('tieu_de', 'PHÒNG 7 · LADY PAGE')),
            html.escape(d.get('moc', '')))]
    for k in d.get('khoi', []):
        lo = k.get('loai', 'k')
        if lo not in DAU:
            lo = 'k'
        r.append('<h2><i class="i-%s">%s</i>%s</h2>' % (lo, DAU[lo], html.escape(k.get('ten', ''))))
        r.append('<div class="box b-%s">' % lo)
        if k.get('bang'):
            r.append('<table>' + ''.join(
                '<tr><td>%s</td><td>%s</td></tr>'
                % (html.escape(str(d1[0])), o_gia_tri(d1[1], d1[2] if len(d1) > 2 else None))
                for d1 in k['bang']) + '</table>')
        if k.get('y'):
            r.append('<ul>' + ''.join('<li>%s</li>' % y for y in k['y']) + '</ul>')
        if k.get('chu'):
            r.append('<p class="chu">%s</p>' % k['chu'])
        r.append('</div>')
    if d.get('chan'):
        r.append('<div class="foot"><span>%s</span><span>Phòng 7 · Lady Page</span></div>'
                 % html.escape(d['chan']))
    return '\n'.join(r)


def chup(trang_html, dich):
    from playwright.sync_api import sync_playwright
    t = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8')
    t.write(trang_html)
    t.close()
    pathlib.Path(dich).parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={'width': 1080, 'height': 400}, device_scale_factor=2)
        pg.goto('file://' + t.name)
        pg.wait_for_timeout(350)
        # cat vua khit chieu cao that, khong de thua mang den o duoi
        cao = pg.evaluate('()=>Math.ceil(document.body.getBoundingClientRect().height)')
        pg.set_viewport_size({'width': 1080, 'height': max(400, cao)})
        pg.wait_for_timeout(120)
        pg.screenshot(path=dich)
        b.close()
    return dich


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
    print(chup(dung(d), sys.argv[2]))
