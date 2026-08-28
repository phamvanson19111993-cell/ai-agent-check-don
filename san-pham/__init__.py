# -*- coding: utf-8 -*-
"""Hồ sơ từng sản phẩm cho tao-chien-dich.py.

Mỗi sản phẩm là một file trong thư mục này. Thêm sản phẩm mới thì chép
`mau.py` ra rồi điền, KHÔNG sửa tao-chien-dich.py.

Bắt buộc mỗi hồ sơ phải có:
    TEN_CD  LINK  NGAN_SACH  ANH_QC  NHOM
Ô nào chưa có nguồn thì để nguyên chuỗi bắt đầu bằng "CAN_DIEN" —
chương trình sẽ dừng và liệt kê ra, thay vì đăng một câu bịa lên quảng cáo.
"""
import importlib, os, sys

DAU_CHUA_DIEN = 'CAN_DIEN'


def nap(ten):
    duong = os.path.join(os.path.dirname(__file__), ten.replace('-', '_') + '.py')
    if not os.path.exists(duong):
        co = sorted(f[:-3].replace('_', '-') for f in os.listdir(os.path.dirname(__file__))
                    if f.endswith('.py') and not f.startswith('__'))
        sys.exit("Khong co ho so san pham '%s'. Dang co: %s" % (ten, ', '.join(co)))
    hs = importlib.import_module('san_pham_tam_' + ten.replace('-', '_'), None) \
        if False else _nap_file(duong, ten)
    thieu = _do_thieu(hs)
    if thieu:
        print("KHONG CHAY DUOC — ho so '%s' con %d o chua dien:" % (ten, len(thieu)))
        for d in thieu:
            print("   -", d)
        print("\nDien vao %s roi chay lai." % duong)
        print("TUYET DOI khong tu bia so cong bo, gia, hay cong dung —")
        print("khach tra ra khong khop la mat uy tin ca trang.")
        sys.exit(1)
    return hs


def _nap_file(duong, ten):
    spec = importlib.util.spec_from_file_location('sp_' + ten.replace('-', '_'), duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for k in ('TEN_CD', 'LINK', 'NGAN_SACH', 'ANH_QC', 'NHOM'):
        if not hasattr(m, k):
            sys.exit("Ho so %s thieu bien bat buoc: %s" % (duong, k))
    return m


def _do_thieu(m, duong=''):
    """Đi khắp hồ sơ tìm mọi chuỗi còn để CAN_DIEN."""
    ra = []

    def di(gt, ten):
        if isinstance(gt, str):
            if gt.strip().startswith(DAU_CHUA_DIEN):
                ra.append('%s  ->  %s' % (ten, gt.strip()))
        elif isinstance(gt, dict):
            for k, v in gt.items():
                di(v, '%s[%r]' % (ten, k))
        elif isinstance(gt, (list, tuple)):
            for i, v in enumerate(gt):
                di(v, '%s[%d]' % (ten, i))

    for k in dir(m):
        if k.startswith('_'):
            continue
        di(getattr(m, k), k)
    return ra
