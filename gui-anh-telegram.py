#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gửi ảnh báo cáo mới nhất sang Telegram.

Chạy trên máy chủ GitHub, không phải máy anh Sơn — máy anh tắt thì vẫn chạy.
Lấy mã từ biến môi trường, KHÔNG bao giờ ghi mã vào file trong kho.

    TG_TOKEN   mã bot, lấy từ @BotFather
    TG_CHAT    mã cuộc trò chuyện, lấy từ @userinfobot
"""
import os, sys, glob, json, urllib.request, urllib.parse, uuid, pathlib

TOKEN = os.environ.get('TG_TOKEN', '').strip()
CHAT  = os.environ.get('TG_CHAT', '').strip()
GOC   = 'https://api.telegram.org/bot' + TOKEN


def goi(ham, truong, tep=None):
    """POST multipart/form-data — đủ dùng, không cần thư viện ngoài."""
    bien = uuid.uuid4().hex
    than = b''
    for k, v in truong.items():
        than += ('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n'
                 % (bien, k, v)).encode('utf-8')
    if tep:
        ten, noi_dung = tep
        than += ('--%s\r\nContent-Disposition: form-data; name="photo"; filename="%s"\r\n'
                 'Content-Type: image/png\r\n\r\n' % (bien, ten)).encode('utf-8')
        than += noi_dung + b'\r\n'
    than += ('--%s--\r\n' % bien).encode('utf-8')

    yc = urllib.request.Request(
        GOC + '/' + ham, data=than,
        headers={'Content-Type': 'multipart/form-data; boundary=' + bien})
    with urllib.request.urlopen(yc, timeout=60) as tl:
        return json.loads(tl.read().decode('utf-8'))


def anh_moi_nhat():
    ds = sorted(glob.glob('bao-cao/anh/*.png'), key=os.path.getmtime)
    return ds[-1] if ds else None


def loi_dan(duong_dan):
    """Một dòng chú thích lấy từ tên file, để nhìn Telegram là biết kỳ nào."""
    ten = pathlib.Path(duong_dan).stem            # 2026-08-28-16h
    phan = ten.split('-')
    if len(phan) >= 4 and phan[0].isdigit():
        return 'Báo cáo Q10 · %s/%s · %s' % (phan[2], phan[1], '-'.join(phan[3:]))
    return 'Báo cáo Q10 · ' + ten


def main():
    thieu = [t for t, v in (('TG_TOKEN', TOKEN), ('TG_CHAT', CHAT)) if not v]
    if thieu:
        print('::error::Chua co ma bi mat: ' + ', '.join(thieu))
        print('Vao: Settings > Secrets and variables > Actions > New repository secret')
        return 1

    duong_dan = anh_moi_nhat()
    if not duong_dan:
        print('Khong co anh nao trong bao-cao/anh/ — khong gui gi.')
        return 0

    noi_dung = pathlib.Path(duong_dan).read_bytes()
    print('Gui:', duong_dan, '(%d byte)' % len(noi_dung))

    kq = goi('sendPhoto',
             {'chat_id': CHAT, 'caption': loi_dan(duong_dan)},
             (pathlib.Path(duong_dan).name, noi_dung))

    if not kq.get('ok'):
        print('::error::Telegram tu choi: %s' % kq.get('description', kq))
        return 1
    print('Da gui xong. message_id =', kq['result']['message_id'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
