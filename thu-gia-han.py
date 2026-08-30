#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thu viec gia_han bang mot Facebook gia lap. Khong goi ra mang."""
import datetime, io, sys, types

class GiaFB(object):
    """Dung lai dung nhung gi thuc-thi.py can: doc, lay_het, sua."""
    def __init__(self, du):
        self.du = du
        self.da_sua = []

    def doc(self, duong, tham=None):
        return {"data": self.du.get(duong, [])}

    def lay_het(self, duong, tham=None):
        return list(self.du.get(duong, []))

    def sua(self, duong, tham):
        self.da_sua.append((duong, dict(tham)))
        print("  [gia lap] SUA %s -> %s" % (duong, tham))
        return True


def nap(gia, lam_that=True, tra_loi="CO"):
    import importlib.util
    sp = importlib.util.spec_from_file_location("tt", "thuc-thi.py")
    m = importlib.util.module_from_spec(sp)
    m.__dict__["requests"] = types.SimpleNamespace()
    sp.loader.exec_module(m)
    m.doc, m.lay_het, m.sua = gia.doc, gia.lay_het, gia.sua
    m.LAM_THAT = lam_that
    m.hoi_lam = lambda mo_ta: lam_that
    return m


HOM_NAY = datetime.datetime.now(datetime.timezone.utc)
HAN_1_9 = (HOM_NAY + datetime.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S+0000")
HAN_CU  = (HOM_NAY - datetime.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%S+0000")

DU = {
 "act_1/campaigns": [{"id": "cd1", "name": "Q10 · T9 · Tiep can moi", "status": "ACTIVE"},
                     {"id": "cd9", "name": "Aztlan gi do", "status": "ACTIVE"}],
 "cd1/adsets": [{"id": "nh1", "name": "Nhom 1 · nu 45-60", "status": "ACTIVE",
                 "end_time": HAN_1_9, "daily_budget": "300000"}],
 "nh1/ads": [{"id": "qc1", "name": "Doanh so moi",   "status": "ACTIVE"},
             {"id": "qc2", "name": "Doanh so moi 1", "status": "PAUSED"},
             {"id": "qc3", "name": "Doanh so moi 2", "status": "PAUSED"}],
}

loi = []
def dat(ten, dk):
    print(("  dat  " if dk else "  HONG ") + ten)
    if not dk: loi.append(ten)

print("═" * 62)
print("1. Gia han 3 ngay cho chien dich Q10 — truong hop thuong")
g = GiaFB(DU); m = nap(g)
m.viec_gia_han("act_1", {"ten": "Q10", "so_ngay": 3})
dat("goi dung 1 lenh sua", len(g.da_sua) == 1)
dat("sua dung nhom nh1", g.da_sua and g.da_sua[0][0] == "nh1")
dat("chi doi end_time, khong dung toi status",
    g.da_sua and list(g.da_sua[0][1].keys()) == ["end_time"])
if g.da_sua:
    moi = datetime.datetime.strptime(g.da_sua[0][1]["end_time"], "%Y-%m-%dT%H:%M:%S+0000")
    cu  = datetime.datetime.strptime(HAN_1_9, "%Y-%m-%dT%H:%M:%S+0000")
    dat("han moi = han cu + 3 ngay", abs((moi - cu).days - 3) <= 0)
dat("khong dung toi mau quang cao dang tat",
    all(d[0] not in ("qc1", "qc2", "qc3") for d in g.da_sua))
dat("khong dung toi chien dich Aztlan", all(d[0] != "cd9" for d in g.da_sua))

print("\n2. Nhom da HET HAN 3 ngay truoc — phai tinh tu bay gio, khong tu han cu")
D2 = dict(DU); D2["cd1/adsets"] = [dict(DU["cd1/adsets"][0], end_time=HAN_CU)]
g2 = GiaFB(D2); m2 = nap(g2)
m2.viec_gia_han("act_1", {"ten": "Q10", "so_ngay": 3})
if g2.da_sua:
    moi = datetime.datetime.strptime(g2.da_sua[0][1]["end_time"], "%Y-%m-%dT%H:%M:%S+0000")
    dat("han moi nam o TUONG LAI", moi.replace(tzinfo=datetime.timezone.utc) > HOM_NAY)
else:
    dat("co goi lenh sua", False)

print("\n3. CHAY THU — khong duoc goi lenh sua nao")
g3 = GiaFB(DU); m3 = nap(g3, lam_that=False)
m3.viec_gia_han("act_1", {"ten": "Q10", "so_ngay": 3})
dat("chay thu khong sua gi", len(g3.da_sua) == 0)

print("\n4. Chan so ngay vo ly")
for n in (0, 31, -5):
    g4 = GiaFB(DU); m4 = nap(g4)
    m4.viec_gia_han("act_1", {"ten": "Q10", "so_ngay": n})
    dat("so_ngay=%s bi chan" % n, len(g4.da_sua) == 0)

print("\n5. Go sai ten chien dich — khong duoc sua bua")
g5 = GiaFB(DU); m5 = nap(g5)
m5.viec_gia_han("act_1", {"ten": "khong-co-ten-nay", "so_ngay": 3})
dat("ten sai thi khong sua gi", len(g5.da_sua) == 0)

print("\n6. Nhom chay lien tuc (khong co end_time) — khong phai gia han")
D6 = dict(DU); D6["cd1/adsets"] = [{"id": "nh1", "name": "Nhom lien tuc",
                                    "status": "ACTIVE", "daily_budget": "300000"}]
g6 = GiaFB(D6); m6 = nap(g6)
m6.viec_gia_han("act_1", {"ten": "Q10", "so_ngay": 3})
dat("khong end_time thi bo qua", len(g6.da_sua) == 0)

print("\n" + "═" * 62)
print("KET QUA: %d hong" % len(loi))
for x in loi: print("  - " + x)
sys.exit(1 if loi else 0)
