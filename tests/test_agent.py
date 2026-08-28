"""Kiểm thử nhanh: python -m unittest discover -s tests"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent import compliance, kb, planner, prompts  # noqa: E402


class TestKnowledgeBase(unittest.TestCase):
    def test_du_ba_san_pham(self):
        ids = {p["id"] for p in kb.products()}
        self.assertEqual(ids, {"coenzyme-q10", "dha-epa-sq", "nattokinase"})

    def test_du_bon_trieu_chung(self):
        ids = {s["id"] for s in kb.symptoms()}
        self.assertEqual(ids, {"dau-dau", "chong-mat", "mat-ngu", "te-bi-chan-tay"})

    def test_moi_trieu_chung_deu_co_san_pham_hop_le(self):
        hop_le = {p["id"] for p in kb.products()}
        for s in kb.symptoms():
            for pid in s["san_pham_lien_quan"]:
                self.assertIn(pid, hop_le, f"{s['id']} trỏ tới sản phẩm lạ: {pid}")

    def test_nattokinase_co_canh_bao_thuoc_chong_dong(self):
        natto = kb.get_product("nattokinase")
        self.assertTrue(
            any("chống đông" in x for x in natto["luu_y_an_toan"]),
            "Nattokinase bắt buộc phải có cảnh báo về thuốc chống đông máu",
        )

    def test_bao_loi_ro_rang_khi_sai_khoa(self):
        with self.assertRaises(KeyError):
            kb.get_symptom("khong-ton-tai")


class TestCompliance(unittest.TestCase):
    def test_bat_duoc_tu_cam(self):
        r = compliance.check("Sản phẩm chữa khỏi mất ngủ.")
        self.assertFalse(r.dat)
        self.assertTrue(any("Từ ngữ" in i.loai for i in r.issues))

    def test_khong_bao_nham_cau_khuyen_cao(self):
        text = (
            "Sản phẩm hỗ trợ tuần hoàn máu. Nếu đang dùng thuốc điều trị hãy hỏi ý kiến bác sĩ.\n"
            "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."
        )
        self.assertTrue(compliance.check(text).dat)

    def test_thieu_khuyen_cao_thi_truot(self):
        r = compliance.check("Sản phẩm hỗ trợ tuần hoàn máu.")
        self.assertFalse(r.dat)
        self.assertTrue(any("khuyến cáo" in i.loai for i in r.issues))

    def test_bat_cam_ket_thoi_gian(self):
        r = compliance.check("Cam kết hết tê bì sau 7 ngày.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat)

    def test_bat_danh_nghia_bac_si(self):
        r = compliance.check("Bác sĩ khuyên dùng sản phẩm này.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat)

    def test_go_so_1_khong_bi_bao_nham(self):
        r = compliance.check("Ai mất ngủ thì gõ số 1 nhé.", yeu_cau_khuyen_cao=False)
        self.assertTrue(r.dat, r.to_text())

    def test_danh_dau_bo_qua_thi_khong_soat(self):
        text = compliance.BO_QUA_MARKER + "\nTài liệu này liệt kê từ chữa khỏi làm ví dụ."
        r = compliance.check(text)
        self.assertTrue(r.dat)
        self.assertTrue(r.bo_qua)
        self.assertEqual(r.issues, [])

    def test_khong_danh_dau_thi_van_soat_binh_thuong(self):
        r = compliance.check("Sản phẩm chữa khỏi mất ngủ.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat)
        self.assertFalse(r.bo_qua)

    def test_bat_sai_su_that_ve_gia(self):
        r = compliance.check("Mua nhiều rẻ hơn nhé cô chú.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat, r.to_text())

    def test_bat_sai_su_that_ve_lieu_trinh(self):
        r = compliance.check("Một hộp chưa kịp thấy gì đâu ạ.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat, r.to_text())

    def test_bat_sai_thanh_phan_thia_la_den(self):
        r = compliance.check("Trong sản phẩm có thìa là đen.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat, r.to_text())

    def test_bat_gan_ubiquinol_cho_giay_to_viet_nam(self):
        r = compliance.check("Nhãn phụ ghi rõ ubiquinol.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat, r.to_text())

    def test_noi_dang_khu_dan_nguon_hop_nhat_van_dat(self):
        r = compliance.check(
            "Hộp gốc Nhật in chữ 還元型, nghĩa là dạng khử.", yeu_cau_khuyen_cao=False
        )
        self.assertTrue(r.dat, r.to_text())

    def test_tu_xung_so_1_bi_bat(self):
        r = compliance.check("Đây là sản phẩm số 1 Việt Nam.", yeu_cau_khuyen_cao=False)
        self.assertFalse(r.dat)


class TestKichBanCoSan(unittest.TestCase):
    def test_tat_ca_kich_ban_mau_deu_dat(self):
        thu_muc = Path(__file__).resolve().parent.parent / "scripts"
        files = sorted(thu_muc.glob("*.md"))
        self.assertTrue(files, "Không tìm thấy kịch bản mẫu nào")
        for f in files:
            with self.subTest(kich_ban=f.name):
                r = compliance.check(f.read_text(encoding="utf-8"))
                self.assertTrue(r.dat, f"{f.name}:\n{r.to_text()}")


class TestChayDocLap(unittest.TestCase):
    """Bộ soát là công cụ dùng chung - phải chạy được trên máy không cài anthropic."""

    def test_cac_lenh_offline_khong_cham_toi_anthropic(self):
        import subprocess

        chan = (
            "import sys, os;"
            "sys.path.insert(0, os.getcwd());"
            "\nclass C:\n"
            "    def find_module(self, n, p=None):\n"
            "        return self if n.split('.')[0] == 'anthropic' else None\n"
            "    def load_module(self, n):\n"
            "        raise ImportError(n)\n"
            "sys.meta_path.insert(0, C())\n"
            "import runpy; sys.argv = ['cli'] + sys.argv[1:];"
            "runpy.run_module('agent.cli', run_name='__main__')"
        )
        goc = str(Path(__file__).resolve().parent.parent)
        for args in (["list"], ["plan", "--so-ngay", "2"], ["hooks", "--so-luong", "3"]):
            with self.subTest(lenh=args[0]):
                r = subprocess.run(
                    [sys.executable, "-c", chan, *args],
                    cwd=goc, capture_output=True, text=True,
                    env={"PATH": os.environ.get("PATH", "")},
                )
                self.assertEqual(r.returncode, 0, r.stderr[-500:])


class TestPrompt(unittest.TestCase):
    def test_system_co_cau_khuyen_cao_va_tu_cam(self):
        s = prompts.build_system()
        self.assertIn("không phải là thuốc", s)
        self.assertIn("chữa khỏi", s)

    def test_brief_co_du_thanh_phan(self):
        b = prompts.build_brief(
            symptom_key="te-bi-chan-tay",
            persona_key="nguoi-cao-tuoi-60",
            format_key="hook-noi-dau-giai-phap",
            platform="facebook",
        )
        self.assertIn("Tê bì chân tay", b)
        self.assertIn("Người cao tuổi", b)
        self.assertIn("Nattokinase", b)
        self.assertIn("chống đông", b)


class TestPlanner(unittest.TestCase):
    def test_lich_du_ngay_va_khong_lap_lien_tuc(self):
        ke_hoach = planner.build(30)
        self.assertEqual(len(ke_hoach), 30)
        for a, b in zip(ke_hoach, ke_hoach[1:]):
            self.assertNotEqual(
                (a.trieu_chung, a.dinh_dang), (b.trieu_chung, b.dinh_dang)
            )

    def test_lich_lap_lai_duoc(self):
        self.assertEqual(planner.to_markdown(planner.build(10)),
                         planner.to_markdown(planner.build(10)))


class _FakeBlock:
    type = "text"

    def __init__(self, text):
        self.text = text


class _FakeMessage:
    def __init__(self, text):
        self.content = [_FakeBlock(text)]
        self.stop_reason = "end_turn"
        self.usage = mock.Mock(input_tokens=10, output_tokens=20, cache_read_input_tokens=0)


class TestVongTuSua(unittest.TestCase):
    """Kiểm tra vòng lặp tự sửa mà không cần gọi API thật."""

    def test_tu_sua_khi_dinh_tu_cam(self):
        from agent import generator

        xau = "Sản phẩm chữa khỏi mất ngủ."
        tot = (
            "Sản phẩm hỗ trợ cải thiện giấc ngủ.\n"
            "Thực phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."
        )
        lan_goi = {"n": 0}

        def gia_lap(client, system, messages, **kwargs):
            lan_goi["n"] += 1
            return _FakeMessage(xau if lan_goi["n"] == 1 else tot)

        with mock.patch.object(generator, "_client", lambda: object()), \
             mock.patch.object(generator, "_call", gia_lap):
            kq = generator.generate(
                symptom_key="mat-ngu",
                persona_key="phu-nu-45-55",
                format_key="ke-chuyen",
            )

        self.assertEqual(lan_goi["n"], 2, "Phải gọi lại model để sửa lỗi tuân thủ")
        self.assertEqual(kq.so_lan_sua, 1)
        self.assertTrue(kq.report.dat)


if __name__ == "__main__":
    unittest.main()
