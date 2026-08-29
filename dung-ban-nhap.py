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


def bit_cua_thoat(s):
    """Bo cac lien ket dua khach RA KHOI trang, giu lai chu.

    Giu nguyen hai lien ket Messenger — o Viet Nam do la duong chot don that,
    khach nhan tin la mot buoc TIEN toi mua, khong phai buoc roi di.
    Bon lien ket con lai (3 sang fanpage, 1 sang trang nha san xuat) chi de
    tham khao: doi thanh chu thuong, thong tin van con nguyen, khach van tra
    cuu duoc, nhung khong con cua bam mot phat la mat khach.
    """
    FB = "https://www.facebook.com/profile.php?id=61592861334561"

    # 1. Nut to 'Xem phan hoi tren Facebook' — bo han, day la cua thoat to nhat
    nut = ('<a class="btn btn-lg" href="' + FB + '" target="_blank"'
           ' rel="noopener">Xem phản hồi trên Facebook</a>')
    assert nut in s, "khong tim thay nut Xem phan hoi tren Facebook"
    s = s.replace(nut, "", 1)

    # 2. Ba cho con lai: bo the <a>, giu chu
    for dia_chi, chu in [(FB, "trang Facebook của bên em"),
                         (FB, "DiLiM Supplement"),
                         ("https://www.ams-life.co.jp/", "ams-life.co.jp")]:
        the = ('<a href="' + dia_chi + '" target="_blank" rel="noopener">'
               + chu + '</a>')
        assert the in s, "khong tim thay lien ket: " + chu
        s = s.replace(the, '<span class="ngoai">' + chu + '</span>', 1)

    neo = '.quote{overflow-x:auto'
    s = s.replace(neo, '.ngoai{font-weight:600;color:var(--ink2)}\n' + neo, 1)

    assert s.count('href="' + FB + '"') == 0, "van con lien ket sang fanpage"
    assert s.count('ams-life.co.jp/"') == 0, "van con lien ket sang trang Nhat"
    assert s.count('href="https://m.me/') == 2, "phai giu du hai lien ket Messenger"
    return s


def loi_tran_an_len_tren_nut(s):
    """Dua cau 'bam gui chua phai tra dong nao' len TREN nut gui.

    The CSS ten la .truoc-nut nhung trong ma no dang nam SAU nut, nen hien ra
    ben DUOI nut. Khach doc nut roi quyet dinh luon, khong ai doc xuong duoi
    moi bam. Loi tran an phai den TRUOC luc tay do xuong.
    """
    i = s.index('<div class="full btn-row">')
    j = s.index('</div>', s.index('</button>', i)) + len('</div>')
    nut = s[i:j]

    k = s.index('<p class="truoc-nut">')
    m = s.index('</p>', k) + len('</p>')
    cau = s[k:m]

    assert i < k, "cau tran an da nam tren nut roi"
    s = s[:k] + s[m:]              # nhac cau ra
    return s[:i] + cau + s[i:]     # dat lai ngay TRUOC nut


COD_TIN_NHAN = """    if(du.cach_tra === 'cod'){
      return t + '\\n\\nNHẬN HÀNG RỒI TRẢ TIỀN'
             + '\\nKhách không chuyển gì trước.'
             + '\\nTrả đủ cho người giao khi nhận hàng.';
    }
"""

COD_MAN_HINH = """    if(du.cach_tra === 'cod'){
      return '<span class="don-tra">'
        + '<b>Anh chị không phải chuyển gì trước</b>'
        + '<span class="ck-note">Nhân viên gọi xác nhận đơn rồi bên em gửi hàng. '
        + 'Anh chị <b>mở hộp kiểm tra rồi mới trả tiền</b> cho người giao. '
        + 'Uống hết hộp đầu không thấy khác, bên em nhận lại hộp còn nguyên.</span>'
        + '</span>';
    }
"""


def cam_ket_va_nhan_hang_tra_tien(s):
    """Hai loi cam ket cua anh Son + lua chon COD trong o Cach thanh toan.

    Nguyen van anh Son gui 29/08:
      "Nhan hang, mo hop kiem tra roi moi tra tien."
      "Uong het hop dau khong thay khac, ben em nhan lai hop con nguyen."
    Day la CAM KET KINH DOANH cua anh Son, khong phai chu em tu nghi ra.
    Sua chu o day = sua loi hua voi khach, chi anh Son moi duoc sua.
    """
    # 1. Them lua chon nhan hang tra tien, dat len dau va chon san
    cu = ('<div class="tra-o" id="chon-tra-form">\n'
          '<label class="hop-o on"><input type="radio" name="cach_tra" value="coc" checked>'
          '<span class="h-t">Đặt cọc 200.000đ giữ hàng</span>'
          '<span class="h-s">Phần còn lại trả khi nhận hàng</span></label>')
    moi = ('<div class="tra-o" id="chon-tra-form">\n'
           '<label class="hop-o on"><input type="radio" name="cach_tra" value="cod" checked>'
           '<span class="h-t">Nhận hàng rồi trả tiền</span>'
           '<span class="h-s">Mở hộp kiểm tra rồi mới trả — không trả trước đồng nào</span></label>\n'
           '<label class="hop-o"><input type="radio" name="cach_tra" value="coc">'
           '<span class="h-t">Đặt cọc 200.000đ giữ hàng</span>'
           '<span class="h-s">Phần còn lại trả khi nhận hàng</span></label>')
    assert cu in s, "khong tim thay o Cach thanh toan"
    s = s.replace(cu, moi, 1)

    # 2. Hai loi cam ket, dat ngay tren nut gui
    khoi = ('<div class="cam-ket-mua">'
            '<p><b>Nhận hàng, mở hộp kiểm tra rồi mới trả tiền.</b></p>'
            '<p><b>Uống hết hộp đầu không thấy khác, bên em nhận lại hộp còn nguyên.</b></p>'
            '</div>')
    neo = '<p class="truoc-nut">'
    i = s.index(neo)
    s = s[:i] + khoi + s[i:]

    css = ('.cam-ket-mua{grid-column:1/-1;margin:0 0 .7rem;padding:.75rem .9rem;'
           'border:1px solid var(--jade);border-radius:var(--r);'
           'background:var(--jade-soft)}'
           '\n.cam-ket-mua p{margin:0;font-size:.88rem;line-height:1.5;color:var(--jade)}'
           '\n.cam-ket-mua p+p{margin-top:.35rem}'
           '\n.quote{overflow-x:auto')
    s = s.replace('.quote{overflow-x:auto', css, 1)

    # 3. Ba cho trong ma chi biet 'coc' va 'du' — khong sua thi khach chon
    #    nhan hang tra tien ma don bao ve lai ghi "Dat coc 200.000d".
    nhan = ("['Cách trả', du.cach_tra === 'du' ? 'Chuyển khoản đủ'"
            " : 'Đặt cọc 200.000đ'],")
    nhan_moi = ("['Cách trả', du.cach_tra === 'du' ? 'Chuyển khoản đủ'"
                " : du.cach_tra === 'cod' ? 'Nhận hàng rồi trả tiền'"
                " : 'Đặt cọc 200.000đ'],")
    assert nhan in s, "khong tim thay nhan Cach tra"
    s = s.replace(nhan, nhan_moi, 1)

    tin = "  function tinNhan(du){\n    var t = tomTat(du);\n"
    assert tin in s, "khong tim thay tinNhan"
    s = s.replace(tin, tin + COD_TIN_NHAN, 1)

    tra = "  function khoiTra(du){\n"
    assert tra in s, "khong tim thay khoiTra"
    s = s.replace(tra, tra + COD_MAN_HINH, 1)

    return s


def dia_chi_mot_o(s):
    """Nam o dia chi gap lai gom thanh MOT o duy nhat — anh Son yeu cau 3 o.

    Truoc: ten · so dien thoai · khoi gap chua 5 o (tinh/huyen/xa/thon/so nha)
    Sau:   ten · so dien thoai · mot o dia chi

    Khach tren dien thoai go dia chi lien mot mach quen hon la nhay qua nam o.
    Doan JavaScript to sang khoi dia chi da co san "if(!kd) return;" nen bo
    khoi di la no tu tat, khong loi.
    """
    i = s.index('<div class="field full"><details class="dia-chi">')
    j = s.index('</details></div>', i) + len('</details></div>')
    o_moi = ('<div class="field full"><label for="dia_chi">Địa chỉ nhận hàng</label>'
             '<textarea id="dia_chi" name="dia_chi" rows="2" autocomplete="street-address"'
             ' placeholder="Số nhà, thôn/xóm, xã/phường, huyện/quận, tỉnh/thành phố">'
             '</textarea>'
             '<span class="dc-ghi">Ghi càng chi tiết thì bưu tá càng giao đúng ngay lần đầu.'
             '</span></div>')
    s = s[:i] + o_moi + s[j:]

    neo = '.field input,.field select{width:100%;max-width:100%;min-width:0;box-sizing:border-box}'
    assert neo in s, "khong tim thay CSS o nhap"
    css = (neo.replace('.field input,.field select',
                       '.field input,.field select,.field textarea')
           + '\n.field textarea{font:400 .95rem/1.5 "Be Vietnam Pro",sans-serif;'
             'padding:.65rem .8rem;border:1px solid var(--line);border-radius:var(--r);'
             'background:var(--paper);color:var(--ink);resize:vertical;min-height:64px}'
             '\n.field textarea::placeholder{color:var(--ink3);opacity:.65}'
             '\n.dc-ghi{display:block;margin-top:.3rem;font-size:.76rem;color:var(--ink3)}')
    s = s.replace(neo, css, 1)

    cu = ("    du.dia_chi = [du.sonha, du.thon, du.xa, du.huyen, du.tinh]\n"
          "                   .filter(function(x){ return x && x.trim(); })\n"
          "                   .join(', ');\n")
    assert cu in s, "khong tim thay doan ghep dia chi 5 cap"
    s = s.replace(cu, "    du.dia_chi = (du.dia_chi || '').trim();\n", 1)

    # tieu de nhom 'DIA CHI NHAN HANG' truoc day gom 5 o nen can; nay mot o
    # thi no lap lai chinh cai nhan ngay duoi no.
    tieu_de = '<p class="fgroup">Địa chỉ nhận hàng</p>'
    if tieu_de in s:
        s = s.replace(tieu_de, "", 1)

    assert 'class="dia-chi"' not in s, "van con khoi dia chi cu"
    assert 'name="dia_chi"' in s, "thieu o dia chi moi"
    return s


def bo_dong_trong_trong_ban_tin(s):
    """Don gui di khong con dong 'Dia chi:' bo trong.

    Dia chi khong bat buoc, nen don khong co dia chi la binh thuong. Nhung
    tomTat() luon in du nam dong, thanh ra nhan vien nhan duoc mot dong
    'Dia chi:' trong khong — trong nhu don bi loi.
    """
    cu = """  function tomTat(du){
    return 'ĐƠN HÀNG RICH COENZYME Q10'
      + '\\nHọ tên: '     + (du.ten     || '')
      + '\\nĐiện thoại: ' + (du.sdt     || '')
      + '\\nĐịa chỉ: '    + (du.dia_chi || '')
      + '\\nSố lượng: '   + (du.soluong || '')
      + '\\nThời gian: '  + (du.thoi_gian || '');
  }"""
    moi = """  function tomTat(du){
    var d = [['Họ tên', du.ten], ['Điện thoại', du.sdt], ['Địa chỉ', du.dia_chi],
             ['Số lượng', du.soluong], ['Thời gian', du.thoi_gian]];
    return 'ĐƠN HÀNG RICH COENZYME Q10\\n'
      + d.filter(function(x){ return x[1] && String(x[1]).trim(); })
         .map(function(x){ return x[0] + ': ' + x[1]; })
         .join('\\n');
  }"""
    assert cu in s, "khong tim thay tomTat"
    return s.replace(cu, moi, 1)


def sua_chu_hop_con_nguyen(s):
    """Doi 'nhan lai hop con nguyen' -> 'nhan lai so hop con nguyen'.

    Anh Son duyet 29/08. Voi don nhieu hop, khach uong het hop dau ma khong
    thay khac thi tra lai NHUNG HOP CHUA BOC. Cau cu de khach mua 1 hop hieu
    nham la duoc hoan tien hop da uong het.
    Xuat hien hai cho: khoi cam ket tren nut gui, va man hinh sau khi gui don
    khi khach chon nhan hang tra tien.
    """
    cu = "nhận lại hộp còn nguyên"
    moi = "nhận lại số hộp còn nguyên"
    n = s.count(cu)
    assert n == 2, "phai co dung 2 cho, dem duoc " + str(n)
    return s.replace(cu, moi)


THAY_DOI = [doi_cho_bao_gia, anh_canh_bang_gia, gia_moi_ngay_o_man_dau,
             bo_cau_nhan_vat_minh_hoa, bit_cua_thoat, loi_tran_an_len_tren_nut,
             cam_ket_va_nhan_hang_tra_tien, dia_chi_mot_o,
             bo_dong_trong_trong_ban_tin, sua_chu_hop_con_nguyen]

BANG = ('<div style="position:sticky;top:0;z-index:99;background:#7A1030;color:#fff;'
        'padding:.55rem .9rem;font:600 13px/1.4 system-ui,sans-serif;text-align:center">'
        'BẢN XEM TRƯỚC — chưa lên trang chính. Pixel đã tắt, số liệu quảng cáo không bị ảnh hưởng.</div>')


# Dau nhan: chuoi chi xuat hien SAU khi thay doi da duoc ap dung.
# Nho no ma chay lai duoc nhieu lan — da ap dung roi thi bo qua, khong bao loi.
DAU_NHAN = {
    "doi_cho_bao_gia": None,          # so sanh vi tri, xu ly rieng
    "anh_canh_bang_gia": 'class="bg-anh"',
    "gia_moi_ngay_o_man_dau": "bằng hai cốc cà phê",
    "bo_cau_nhan_vat_minh_hoa": None,
    "bit_cua_thoat": None,
    "loi_tran_an_len_tren_nut": None,
    "cam_ket_va_nhan_hang_tra_tien": "cam-ket-mua",
    "dia_chi_mot_o": 'name="dia_chi"',
    "bo_dong_trong_trong_ban_tin": "var d = [['Họ tên'",
    "sua_chu_hop_con_nguyen": "nhận lại số hộp còn nguyên",
}


def da_ap_dung(ten, s):
    if ten == "doi_cho_bao_gia":
        return s.index('id="dat-hang"') < s.index('id="phan-hoi"')
    if ten == "bo_cau_nhan_vat_minh_hoa":
        return "Nhân vật minh hoạ" not in s
    if ten == "bit_cua_thoat":
        return "facebook.com/profile" not in s
    if ten == "loi_tran_an_len_tren_nut":
        return s.index('<p class="truoc-nut">') < s.index('<div class="full btn-row">')
    dn = DAU_NHAN.get(ten)
    return bool(dn) and dn in s


def ap_dung(s):
    for ham in THAY_DOI:
        if da_ap_dung(ham.__name__, s):
            print("  bo qua (da co san):", ham.__name__)
            continue
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
