#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thu tao-chien-dich.py bang mot Facebook gia lap.

Khong goi ra mang. Chi kiem: --nhom loc dung, chien dich trung ten thi dung
lai chu khong tao them, nhom da co thi bo qua, va tran chi tieu thi chan lai.
"""
import io
import os
import sys
import types
import contextlib

KHO = os.path.dirname(os.path.abspath(__file__))


class FBGia:
    """Ghi lai moi cu goi, tra ve du thu cho chuong trinh chay tiep."""

    def __init__(self, tran=0, da_tieu=0, cd_co=(), nhom_co=()):
        self.da_goi = []
        self.tran, self.da_tieu = tran, da_tieu
        self.cd_co, self.nhom_co = list(cd_co), list(nhom_co)
        self.dem = 0

    def __call__(self, duong_dan, du_lieu=None, tep=None, lay=False):
        self.dem += 1
        self.da_goi.append((duong_dan, (du_lieu or {}).get('name'), lay))
        if lay and duong_dan.startswith('act_') and duong_dan.count('/') == 0:
            return {'name': 'Pham Son BM1.1', 'currency': 'VND',
                    'account_status': 1, 'spend_cap': str(self.tran),
                    'amount_spent': str(self.da_tieu)}
        if lay and duong_dan.endswith('/campaigns'):
            return {'data': [{'id': '1', 'name': c} for c in self.cd_co]}
        if lay and duong_dan.endswith('/adsets'):
            return {'data': [{'name': n} for n in self.nhom_co]}
        if duong_dan.endswith('/adimages'):
            return {'images': {'a': {'hash': 'HASH'}}}
        return {'id': 'moi-%d' % self.dem}


def nap(argv, fb):
    """Nap tao-chien-dich.py voi sys.argv cho truoc va ham goi() bi thay."""
    for k in [k for k in sys.modules if k.startswith('sp_')]:
        del sys.modules[k]
    cu_argv = sys.argv
    sys.argv = argv
    try:
        ma = open(os.path.join(KHO, 'tao-chien-dich.py'), encoding='utf-8').read()
        m = types.ModuleType('tcd')
        m.__file__ = os.path.join(KHO, 'tao-chien-dich.py')
        exec(compile(ma, m.__file__, 'exec'), m.__dict__)
        m.goi = fb
        m.TOKEN = 'x'
        m.lo_pixel = lambda act: None
        m.kiem_tra_dau_vao = lambda: None
        return m
    finally:
        sys.argv = cu_argv


def chay(argv, fb):
    """Chay trong thu muc kho, vi ANH_QC la duong dan tuong doi."""
    cu_cwd = os.getcwd()
    os.chdir(KHO)
    try:
        m = nap(argv, fb)
        ra = io.StringIO()
        try:
            with contextlib.redirect_stdout(ra):
                m.main()
        except SystemExit as e:
            return m, ra.getvalue(), e.code
        return m, ra.getvalue(), 0
    finally:
        os.chdir(cu_cwd)


def main():
    dat = hong = 0

    def can(dk, mo_ta, them=''):
        nonlocal dat, hong
        print('  %s  %s%s' % ('OK ' if dk else 'HỎNG', mo_ta,
                              '' if dk else '  — ' + str(them)))
        if dk:
            dat += 1
        else:
            hong += 1

    C = ['tao-chien-dich.py', '--san-pham', 'giam-mo']

    print('\n1 · --nhom 1 thì chỉ dựng một nhóm')
    fb = FBGia()
    m, ra, _ = chay(C + ['--nhom', '1'], fb)
    adsets = [g for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(len(adsets) == 1, 'dựng đúng 1 nhóm quảng cáo', len(adsets))
    can(adsets and adsets[0][1] == 'Nhom 1 · nu 30-45', 'đúng Nhóm 1', adsets)
    can('300,000 đ mỗi ngày' in ra, 'báo đúng tổng tiền một ngày', ra[-200:])

    print('\n2 · không ghi --nhom thì dựng cả ba, y như trước')
    fb = FBGia()
    m, ra, _ = chay(C, fb)
    adsets = [g for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(len(adsets) == 3, 'dựng đủ 3 nhóm', len(adsets))
    can('900,000 đ mỗi ngày' in ra, 'báo 900.000đ mỗi ngày', ra[-200:])

    print('\n3 · --nhom 1,3 thì lấy đúng hai nhóm đó')
    fb = FBGia()
    m, ra, _ = chay(C + ['--nhom', '1,3'], fb)
    ten = [g[1] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(ten == ['Nhom 1 · nu 30-45', 'Nhom 3 · nam 30-50'], 'đúng nhóm 1 và 3', ten)

    print('\n4 · chạy lần hai với --nhom 2 thì dùng lại chiến dịch cũ')
    fb = FBGia(cd_co=['Giam mo · Ellagic Acid · Vong 1 · 2908'],
               nhom_co=['Nhom 1 · nu 30-45'])
    m, ra, _ = chay(C + ['--nhom', '2'], fb)
    tao_cd = [g for g in fb.da_goi if g[0].endswith('/campaigns') and not g[2]]
    can(not tao_cd, 'KHÔNG dựng thêm chiến dịch trùng tên', tao_cd)
    can('DÙNG LẠI' in ra, 'nói rõ là dùng lại cái cũ')
    ten = [g[1] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(ten == ['Nhom 2 · nu 45-60'], 'chỉ thêm Nhóm 2', ten)

    print('\n5 · nhóm đã có sẵn thì bỏ qua, không dựng trùng')
    fb = FBGia(cd_co=['Giam mo · Ellagic Acid · Vong 1 · 2908'],
               nhom_co=['Nhom 1 · nu 30-45'])
    m, ra, _ = chay(C + ['--nhom', '1'], fb)
    ten = [g[1] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(not ten, 'không dựng lại Nhóm 1', ten)
    can('đã có sẵn, bỏ qua' in ra, 'nói rõ vì sao bỏ qua')

    print('\n6 · đụng trần chi tiêu thì hỏi lại chứ không lặng lẽ dựng')
    fb = FBGia(tran=5000000, da_tieu=5000000)
    m, ra, ma = chay(C + ['--nhom', '1'], fb)
    can('ĐỤNG TRẦN CHI TIÊU' in ra, 'có cảnh báo đụng trần', ra[-300:])
    can(ma not in (0, None), 'dừng lại chứ không dựng tiếp', ma)

    print('\n7 · --nhom 9 thì báo lỗi rõ ràng')
    fb = FBGia()
    try:
        _, ra, ma = chay(C + ['--nhom', '9'], fb)
        can(False, 'phải dừng vì không có nhóm 9')
    except SystemExit as e:
        can('chi co 3 nhom' in str(e.code), 'báo đúng lỗi', e.code)

    print('\n' + '=' * 56)
    print('%d đạt, %d hỏng' % (dat, hong))
    sys.exit(1 if hong else 0)


if __name__ == '__main__':
    main()
