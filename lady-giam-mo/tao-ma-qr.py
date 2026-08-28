#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sinh ma VietQR dang SVG de nhung thang vao index.html.

Vi sao co file nay: trang khong goi ra Internet de lay anh QR — ma nam san
trong file, khong phu thuoc dich vu nao. Nhung moi so tien la mot ma khac
nhau, nen khi anh Son chot bang gia thi phai sinh lai.

Cach dung:
    pip install segno
    python3 lady-giam-mo/tao-ma-qr.py 200000 2490000 4980000

In ra man hinh tung dong JavaScript, chep thang vao bien QR_TIEN trong
index.html. Rieng so tien coc thi chep vao QR_COC.
"""
import sys
import segno

NGAN_HANG_BIN = "970423"        # TPBank, ma NAPAS
SO_TAI_KHOAN  = "38691388888"   # viet lien, khong dau cach


def tlv(ma: str, gia_tri: str) -> str:
    """Mot o theo chuan EMVCo: ma 2 chu so + do dai 2 chu so + noi dung."""
    return f"{ma}{len(gia_tri):02d}{gia_tri}"


def crc16(chuoi: str) -> str:
    """CRC-16/CCITT-FALSE — o 63 cua chuan EMVCo."""
    crc = 0xFFFF
    for byte in chuoi.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return f"{crc:04X}"


NOI_DUNG_MAC_DINH = "DILIM GIAM MO"   # chu nhung san trong ma, khong dau


def payload(so_tien: int, noi_dung: str = NOI_DUNG_MAC_DINH) -> str:
    ben_nhan = tlv("00", NGAN_HANG_BIN) + tlv("01", SO_TAI_KHOAN)
    o38 = tlv("00", "A000000727") + tlv("01", ben_nhan) + tlv("02", "QRIBFTTA")

    p = tlv("00", "01")
    p += tlv("01", "12" if so_tien else "11")   # 12 = co so tien, 11 = de trong
    p += tlv("38", o38)
    p += tlv("52", "0000")                       # nhom nganh, de trong
    p += tlv("53", "704")                        # VND
    if so_tien:
        p += tlv("54", str(int(so_tien)))
    p += tlv("58", "VN")
    if noi_dung:
        p += tlv("62", tlv("08", noi_dung))
    p += "6304"
    return p + crc16(p)


def ra_svg(so_tien: int, noi_dung: str = NOI_DUNG_MAC_DINH) -> str:
    """Ve ma ra SVG mot mach, khong vien — vien trang do trang tu them khi
    doi sang PNG. viewBox bang dung so o cua ma, trang doc lai tu day nen
    ma to hay nho cung ve dung."""
    qr = segno.make(payload(so_tien, noi_dung), error="m")
    luoi = [list(hang) for hang in qr.matrix]
    canh = len(luoi)

    duong = []
    for y, hang in enumerate(luoi):
        x = 0
        while x < canh:
            if hang[x]:
                dai = 1
                while x + dai < canh and hang[x + dai]:
                    dai += 1
                duong.append(f"M{x} {y}h{dai}v1h-{dai}z")
                x += dai
            else:
                x += 1

    return (
        f'<svg class=\\"qr\\" viewBox=\\"0 0 {canh} {canh}\\" shape-rendering=\\"crispEdges\\" '
        f'xmlns=\\"http://www.w3.org/2000/svg\\" role=\\"img\\" '
        f'aria-label=\\"Ma VietQR chuyen khoan TPBank {SO_TAI_KHOAN}\\">'
        f'<rect width=\\"{canh}\\" height=\\"{canh}\\" fill=\\"#fff\\"></rect>'
        f'<path fill=\\"#000\\" d=\\"{"".join(duong)}\\"></path></svg>'
    )


if __name__ == "__main__":
    cac_so = [int(x) for x in sys.argv[1:]] or [200000]
    print("var QR_TIEN = {")
    for i, so in enumerate(cac_so):
        dau_phay = "," if i < len(cac_so) - 1 else ""
        print(f'  "{so}": "{ra_svg(so)}"{dau_phay}')
    print("};")
