#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thu tao-chien-dich.py bang mot Facebook gia lap.

Khong goi ra mang. Chi kiem: --nhom loc dung, chien dich trung ten thi dung
lai chu khong tao them, nhom da co thi bo qua, va tran chi tieu thi chan lai.
"""
import io
import json
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
        self.da_goi.append((duong_dan, (du_lieu or {}).get('name'), lay,
                            dict(du_lieu or {})))
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


class KhongPhaiBanPhim:
    """Gia lam dau vao cua may chu: khong co ai ngoi go phim."""
    def isatty(self):
        return False

    def readline(self):
        raise AssertionError('chuong trinh dang doi go phim tren may chu')


def chay(argv, fb, may_chu=False):
    """Chay trong thu muc kho, vi ANH_QC la duong dan tuong doi."""
    cu_cwd, cu_in = os.getcwd(), sys.stdin
    os.chdir(KHO)
    if may_chu:
        sys.stdin = KhongPhaiBanPhim()
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
        sys.stdin = cu_in


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
    can(adsets and adsets[0][1] == 'Nhom 1 · nu 35-55', 'đúng Nhóm 1', adsets)
    nham = json.loads(adsets[0][3]['targeting']) if adsets else {}
    can(nham.get('age_min') == 35 and nham.get('age_max') == 55,
        'nhắm đúng tuổi 35–55', (nham.get('age_min'), nham.get('age_max')))
    can(nham.get('genders') == [2],
        'CHỈ nhắm nữ — lời quảng cáo xưng "chị"', nham.get('genders'))
    can(not nham.get('interests') and not nham.get('flexible_spec'),
        'sở thích để trống (broad), đúng SOP Phòng 7')
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
    can(ten == ['Nhom 1 · nu 35-55', 'Nhom 3 · nam 30-50'], 'đúng nhóm 1 và 3', ten)

    print('\n4 · chạy lần hai với --nhom 2 thì dùng lại chiến dịch cũ')
    fb = FBGia(cd_co=['Giam mo · Ellagic Acid · Vong 1 · 2908'],
               nhom_co=['Nhom 1 · nu 35-55'])
    m, ra, _ = chay(C + ['--nhom', '2'], fb)
    tao_cd = [g for g in fb.da_goi if g[0].endswith('/campaigns') and not g[2]]
    can(not tao_cd, 'KHÔNG dựng thêm chiến dịch trùng tên', tao_cd)
    can('DÙNG LẠI' in ra, 'nói rõ là dùng lại cái cũ')
    ten = [g[1] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(ten == ['Nhom 2 · nu 56-65'], 'chỉ thêm Nhóm 2', ten)

    print('\n5 · nhóm đã có sẵn thì bỏ qua, không dựng trùng')
    fb = FBGia(cd_co=['Giam mo · Ellagic Acid · Vong 1 · 2908'],
               nhom_co=['Nhom 1 · nu 35-55'])
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

    print('\n8 · --so-ngay 1 thì nhóm tự hết hạn sau một ngày')
    fb = FBGia()
    m, ra, _ = chay(C + ['--nhom', '1', '--so-ngay', '1'], fb)
    du = [g[3] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]][0]
    can('start_time' in du and 'end_time' in du, 'có đặt mốc bắt đầu và kết thúc', du)
    if 'end_time' in du:
        import datetime as dt
        cach = dt.datetime.fromisoformat(du['end_time']) \
            - dt.datetime.fromisoformat(du['start_time'])
        can(cach == dt.timedelta(days=1), 'cách nhau đúng 1 ngày', cach)
    can('300,000 đ/ngày' in ra, 'ngân sách vẫn 300.000đ mỗi ngày')
    can('tự hết hạn' in ra, 'nói rõ là tự hết hạn')

    print('\n9 · không ghi --so-ngay thì không đặt hạn, y như trước')
    fb = FBGia()
    chay(C + ['--nhom', '1'], fb)
    du = [g[3] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]][0]
    can('end_time' not in du, 'không đặt hạn kết thúc', du)

    print('\n10 · --bat thì bật đủ ba tầng, đúng thứ tự')
    fb = FBGia()
    m, ra, _ = chay(C + ['--nhom', '1', '--so-ngay', '1', '--bat'], fb)
    bat = [(g[0], g[3].get('status')) for g in fb.da_goi
           if not g[2] and g[3].get('status') == 'ACTIVE']
    can(len(bat) == 3, 'bật đúng 3 thứ: chiến dịch, nhóm, quảng cáo', bat)
    # Chien dich duoc dung o cu goi thu may, thi ma cua no la 'moi-<so do>'.
    thu = [i for i, g in enumerate(fb.da_goi, 1)
           if g[0].endswith('/campaigns') and not g[2]]
    can(bat and thu and bat[0][0] == 'moi-%d' % thu[0],
        'bật chiến dịch TRƯỚC, rồi mới tới nhóm và quảng cáo', bat)
    can('ĐANG CHẠY THẬT' in ra, 'nói thẳng là đang tiêu tiền thật')
    can('300,000 đ mỗi ngày, trong 1 ngày' in ra, 'báo đúng tiền và hạn', ra[-300:])

    print('\n11 · không ghi --bat thì không bật gì — mặc định vẫn an toàn')
    fb = FBGia()
    m, ra, _ = chay(C + ['--nhom', '1'], fb)
    bat = [g for g in fb.da_goi if not g[2] and g[3].get('status') == 'ACTIVE']
    can(not bat, 'không bật thứ gì', bat)
    can('TẠM DỪNG' in ra, 'vẫn báo mọi thứ đang tạm dừng')

    print('\n12 · đụng trần mà chạy trên máy chủ thì dừng, không hỏi vào khoảng không')
    fb = FBGia(tran=5000000, da_tieu=5000000)
    m, ra, ma = chay(C + ['--nhom', '1', '--bat'], fb, may_chu=True)
    can(isinstance(ma, str) and 'khong co nguoi tra loi' in ma,
        'dừng với lời giải thích, không kẹt chờ gõ phím', ma)
    can(not [g for g in fb.da_goi if not g[2] and g[3].get('status') == 'ACTIVE'],
        'không bật gì khi đang đụng trần')

    print('\n13 · --vao-chien-dich thì nhét nhóm vào chiến dịch Q10 có sẵn')
    fb = FBGia(cd_co=['Q10 · T9 · Tiếp cận mới'])
    m, ra, _ = chay(C + ['--nhom', '1', '--vao-chien-dich', 'Q10 · T9 · Tiếp cận mới'], fb)
    tao_cd = [g for g in fb.da_goi if g[0].endswith('/campaigns') and not g[2]]
    can(not tao_cd, 'KHÔNG dựng chiến dịch mới', tao_cd)
    can('DÙNG LẠI' in ra, 'nói rõ là dùng lại chiến dịch Q10')
    ten = [g[1] for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]]
    can(ten == ['Nhom 1 · nu 35-55'], 'nhóm giảm mỡ nằm trong chiến dịch Q10', ten)

    print('\n14 · gõ sai tên chiến dịch thì DỪNG, không lặng lẽ dựng cái trùng tên')
    fb = FBGia(cd_co=['Q10 · T9 · Tiếp cận mới'])
    m, ra, ma = chay(C + ['--nhom', '1', '--vao-chien-dich', 'Q10 T9'], fb)
    can(not [g for g in fb.da_goi if g[0].endswith('/campaigns') and not g[2]],
        'không dựng chiến dịch nào')
    can(not [g for g in fb.da_goi if g[0].endswith('/adsets') and not g[2]],
        'không dựng nhóm nào')
    can('KHONG TIM THAY' in ra, 'báo không tìm thấy tên đó')
    can('Q10 · T9 · Tiếp cận mới' in ra, 'liệt kê tên đang có để chép lại')

    print('\n' + '=' * 56)
    print('%d đạt, %d hỏng' % (dat, hong))
    sys.exit(1 if hong else 0)


if __name__ == '__main__':
    main()
