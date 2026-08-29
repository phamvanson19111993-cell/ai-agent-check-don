#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soát hồ sơ quảng cáo TRƯỚC khi đẩy lên Facebook.

Chạy trước mỗi lần tạo chiến dịch:

    python3 kiem-quang-cao.py giam-mo
    python3 kiem-quang-cao.py q10

Cái này không thay được mắt người, nhưng nó bắt được đúng những lỗi
làm mất tài khoản: quên dòng khuyến cáo, lỡ tay viết "cam kết",
"giảm cân", nêu số cân số ngày, hay tiêu đề dài quá Facebook cắt mất.

Ra 0 là đi tiếp. Ra 1 là dừng, sửa xong chạy lại.
"""

import importlib.util as iu
import os
import re
import sys

GOC = os.path.dirname(os.path.abspath(__file__))

# Chữ cấm với thực phẩm bảo vệ sức khoẻ. Nguồn: Nghị định 15/2018 và
# chính sách quảng cáo Meta, đã tóm trong sop/phong-7-set-quang-cao.md mục 3.
CAM = [
    'chữa khỏi', 'đặc trị', 'điều trị', 'hết hẳn', 'khỏi hẳn', 'dứt điểm',
    'cam kết', 'đảm bảo', 'hiệu quả 100', 'tốt nhất', 'số 1', 'duy nhất',
    'giảm cân', 'mỡ nội tạng', 'vòng eo', 'trước và sau', 'before',
    'thần dược', 'đánh bay', 'tiêu mỡ', 'đốt mỡ',
]

# Câu ám chỉ thẳng vào thân thể người đọc — Meta cấm riêng khoản này,
# và nhóm giảm béo bị soi gắt nhất.
AM_CHI = [
    r'bạn (đang |có )?(bị )?béo', r'bạn (đang |có )?(bị )?thừa cân',
    r'anh chị (đang |có )?(bị )?béo', r'bạn (có )?tự ti',
]

# Hứa con số — không được, dù có thật.
HUA_SO = [
    r'giảm\s+\d+\s*(kg|cân|kí|ký)', r'\d+\s*(kg|cân|kí|ký)\s*(trong|sau)',
    r'sau\s+\d+\s*ngày\s+(giảm|xuống|hết)', r'-\s*\d+\s*(cm|kg)',
]


def nap(ten):
    d = os.path.join(GOC, 'san-pham', ten.replace('-', '_') + '.py')
    if not os.path.exists(d):
        sys.exit('Khong co ho so san pham %r' % ten)
    s = iu.spec_from_file_location('sp', d)
    m = iu.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    ten = sys.argv[1] if len(sys.argv) > 1 else 'giam-mo'
    m = nap(ten)
    loi = []

    def can(dieu_kien, mo_ta):
        print('  %s  %s' % ('OK ' if dieu_kien else 'HỎNG', mo_ta))
        if not dieu_kien:
            loi.append(mo_ta)

    def bo_qua(mo_ta):
        """Hồ sơ cũ chưa có ô này. Nói ra chứ không lặng lẽ coi như đạt."""
        print('  BỎ QUA  %s — hồ sơ chưa khai ô này' % mo_ta)

    CONG_DUNG  = getattr(m, 'CONG_DUNG', '')
    SO_CONG_BO = getattr(m, 'SO_CONG_BO', '')
    KHUYEN_CAO = getattr(m, 'KHUYEN_CAO', '')

    print('\nSOÁT HỒ SƠ QUẢNG CÁO: %s\n' % ten)
    print('Chung')
    can(m.LINK.startswith('https://'), 'trang đích chạy https')
    can(bool(SO_CONG_BO) and 'CAN_DIEN' not in SO_CONG_BO,
        'có số tiếp nhận công bố')
    can(m.NGAN_SACH >= 50000, 'ngân sách mỗi nhóm không thấp tới mức không ra số')
    can(os.path.exists(os.path.join(GOC, m.ANH_QC)), 'ảnh quảng cáo có thật: %s' % m.ANH_QC)
    can(all(n['tuoi'][0] >= 18 for n in m.NHOM),
        'không nhóm nào nhắm dưới 18 tuổi')

    for n in m.NHOM:
        print('\n%s' % n['ten'])
        t = n['chu']
        low = t.lower()
        # bỏ dòng khuyến cáo bắt buộc ra, không thì chữ "chữa bệnh" trong đó
        # lại bị chính bộ lọc này bắt
        than = low.replace(KHUYEN_CAO.lower(), '') if KHUYEN_CAO else low

        if KHUYEN_CAO:
            can(KHUYEN_CAO in t, 'có đủ dòng khuyến cáo bắt buộc')
        else:
            bo_qua('dòng khuyến cáo bắt buộc')
        if CONG_DUNG:
            can(CONG_DUNG.lower().rstrip('.') in low, 'có nêu đúng câu công dụng trên nhãn')
        else:
            bo_qua('câu công dụng trên nhãn')
        if SO_CONG_BO:
            can(SO_CONG_BO.split(' ')[0].lower() in low, 'có nêu số công bố')
        else:
            bo_qua('số công bố')
        can('phụ nữ có thai' in low, 'có nêu đối tượng không dùng được')

        dinh = [c for c in CAM if c in than]
        can(not dinh, 'không dùng chữ cấm%s' % (' — dính: %s' % ', '.join(dinh) if dinh else ''))

        am = [p for p in AM_CHI if re.search(p, than)]
        can(not am, 'không ám chỉ thẳng vào thân thể người đọc')

        hua = [p for p in HUA_SO if re.search(p, than)]
        can(not hua, 'không hứa số cân, số phân, số ngày')

        can(len(n['tieu_de']) <= 40, 'tiêu đề %d ký tự, trong mức 40' % len(n['tieu_de']))
        can(len(n['mo_ta']) <= 90, 'mô tả %d ký tự, trong mức 90' % len(n['mo_ta']))

    print('\n' + '=' * 58)
    if loi:
        print('DỪNG — %d chỗ hỏng, chưa được đẩy lên Facebook:' % len(loi))
        for x in loi:
            print('   ·', x)
        sys.exit(1)
    print('ĐẠT — hồ sơ %s soát sạch, chạy tạo chiến dịch được.' % ten)
    print('Nhắc: %s đ mỗi nhóm mỗi ngày, bật cả 3 nhóm là %s đ mỗi ngày.'
          % (format(m.NGAN_SACH, ','), format(m.NGAN_SACH * 3, ',')))


if __name__ == '__main__':
    main()
