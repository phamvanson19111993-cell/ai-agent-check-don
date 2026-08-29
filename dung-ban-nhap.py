#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dung ban nhap xem-truoc/index.html tu index.html.

Moi thay doi dang cho anh Son duyet deu nam o day, moi cai mot ham.
Duyet xong thi chay:  python3 dung-ban-nhap.py --len-trang-chinh
de ap dung DUNG bo thay doi do len index.html, khong sua tay lan hai.
"""
import re, sys, pathlib

GOC = pathlib.Path("index.html")
NHAP = pathlib.Path("xem-truoc/index.html")


def doi_cho_bao_gia(s):
    """Chuyen khoi Bao gia & dat hang len ngay truoc phan Phan hoi."""
    i = s.index('id="dat-hang"')
    a = s.rindex('<section', 0, i)
    b = s.index('</section>', i) + len('</section>')
    khoi = s[a:b].replace(
        'class="eyebrow">Phần 12 · Báo giá &amp; đặt hàng',
        'class="eyebrow">Báo giá &amp; đặt hàng')
    con = s[:a] + s[b:]
    j = con.index('id="phan-hoi"')
    k = con.rindex('<section', 0, j)
    return con[:k] + khoi + "\n\n  " + con[k:]


def anh_canh_bang_gia(s):
    """Dat anh san pham nho ben canh bang gia."""
    neo = '.quote{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--card)}'
    css = neo + (
        "\n.bang-gia{display:flex;gap:1rem;align-items:flex-start}"
        "\n.bang-gia>.quote{flex:1 1 auto;min-width:0}"
        "\n.bg-anh{flex:0 0 132px;margin:0;text-align:center;padding:.6rem .4rem;"
        "border:1px solid var(--line);border-radius:var(--r);background:var(--card)}"
        "\n.bg-anh img{display:block;width:100%;height:auto}"
        "\n.bg-anh figcaption{margin-top:.4rem;font-size:.72rem;line-height:1.35;"
        "font-weight:700;color:var(--ink2)}"
        "\n.bg-anh figcaption span{display:block;font-weight:400;font-size:.66rem;color:var(--ink3)}"
        "\n@media(max-width:720px){.bang-gia{display:block}"
        ".bg-anh{display:flex;align-items:center;gap:.7rem;text-align:left;"
        "margin:0 0 .6rem;padding:.5rem .7rem}"
        ".bg-anh img{flex:0 0 64px;width:64px}"
        ".bg-anh figcaption{margin-top:0}}"
    )
    s = s.replace(neo, css, 1)

    hinh = ('<figure class="bg-anh"><img src="images/san-pham-tach-nen.webp" '
            'width="621" height="673" loading="lazy" decoding="async" '
            'alt="Hộp AFC Rich Coenzyme Q10 chính hãng Nhật Bản">'
            '<figcaption>Rich Coenzyme Q10<span>lọ 120 viên · dùng 60 ngày</span></figcaption>'
            '</figure>')
    i = s.index('<div class="quote">', s.index('id="dat-hang"'))
    j = s.index('</table>', i) + len('</table>')
    j = s.index('</div>', j) + len('</div>')
    return s[:i] + '<div class="bang-gia">' + hinh + s[i:j] + '</div>' + s[j:]


def gia_moi_ngay_o_man_dau(s):
    """Dat cau do gia ngay canh cu soc gia o man hinh dau."""
    cu = ('<p class="hero-gia">Từ <b>2.890.000đ</b> một hộp · 6 hộp <b>tặng thêm 1 hộp</b>'
          ' — <a href="#chot-som">xem các mốc</a></p>')
    moi = ('<p class="hero-gia">Từ <b>2.890.000đ</b> một hộp — khoảng <b>48.167đ mỗi ngày</b>,'
           ' bằng hai cốc cà phê.<br>6 hộp <b>tặng thêm 1 hộp</b>, còn'
           ' <b>41.286đ mỗi ngày</b> — <a href="#chot-som">xem các mốc</a></p>')
    assert cu in s, "khong tim thay dong gia o man dau"
    return s.replace(cu, moi, 1)


def bo_cau_nhan_vat_minh_hoa(s):
    """Bo dong chu thich duoi cau chuyen anh Tuan — anh Son yeu cau, da xac nhan lai.

    Co HAI cho: ban tinh trong HTML, va ban do JavaScript dung lai khi bai tu kiem
    doi cau chuyen. Bo mot cho thi cau kia van hien ra, nen phai bo ca hai.
    """
    cau = ('Nhân vật minh hoạ, dựng lại từ tình huống thường gặp.'
           ' Không phải lời chứng thực về hiệu quả sản phẩm.')

    tinh = '<p class="note">' + cau + '</p>'
    assert tinh in s, "khong tim thay dong chu thich tinh"
    s = s.replace(tinh, "", 1)

    dong = """      var nt = document.createElement('p'); nt.className='note';
      nt.textContent = '""" + cau + """';
      elStory.appendChild(nt);
"""
    assert dong in s, "khong tim thay doan JavaScript dung lai dong chu thich"
    s = s.replace(dong, "", 1)

    assert cau not in s, "van con sot cau chu thich"
    return s


THAY_DOI = [doi_cho_bao_gia, anh_canh_bang_gia, gia_moi_ngay_o_man_dau,
             bo_cau_nhan_vat_minh_hoa]

BANG = ('<div style="position:sticky;top:0;z-index:99;background:#7A1030;color:#fff;'
        'padding:.55rem .9rem;font:600 13px/1.4 system-ui,sans-serif;text-align:center">'
        'BẢN XEM TRƯỚC — chưa lên trang chính. Pixel đã tắt, số liệu quảng cáo không bị ảnh hưởng.</div>')


def ap_dung(s):
    for ham in THAY_DOI:
        s = ham(s)
    return s


def main():
    goc = GOC.read_text(encoding="utf-8")
    ra = ap_dung(goc)

    if "--len-trang-chinh" in sys.argv:
        GOC.write_text(ra, encoding="utf-8")
        print("Da ap dung len index.html —", len(THAY_DOI), "thay doi.")
        return

    # ban nhap nam o /xem-truoc/ nen duong dan tuong doi tro sai — doi sang tuyet doi
    truoc = len(re.findall(r'="(?:images|videos)/', ra))
    ra = re.sub(r'="((?:images|videos)/)', r'="/\1', ra)
    assert len(re.findall(r'="(?:images|videos)/', ra)) == 0, "con duong dan tuong doi"
    print("  doi", truoc, "duong dan sang tuyet doi cho ban nhap")

    ra = ra.replace('var PIXEL_ID = "1277743445418211";',
                    'var PIXEL_ID = ""; // ban xem truoc: tat Pixel')
    assert 'var PIXEL_ID = "";' in ra, "khong tat duoc Pixel"
    ra = ra.replace('<body>', '<body>\n' + BANG, 1)
    NHAP.parent.mkdir(exist_ok=True)
    NHAP.write_text(ra, encoding="utf-8")
    print("Da dung", NHAP, "-", len(ra), "ky tu,", len(THAY_DOI), "thay doi.")


if __name__ == "__main__":
    main()
