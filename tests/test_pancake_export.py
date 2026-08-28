"""Chạy: python3 -m unittest discover -s tests -v"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pancake_export import exporter, extract, phones, tagging
from pancake_export.client import PancakeClient


class TestPhones(unittest.TestCase):
    def test_cac_dinh_dang_thuong_gap(self):
        self.assertEqual(phones.extract("Bên Thịnh gọi mình số 0913.351.394"), ["0913351394"])
        self.assertEqual(phones.extract("gọi số 09666.111.04"), ["0966611104"])
        self.assertEqual(phones.extract("Oanh trần 0913060754 tư vấn giúp em"), ["0913060754"])
        self.assertEqual(phones.extract("sđt +84 913 351 394"), ["0913351394"])
        self.assertEqual(phones.extract("số 0913-351-394 nhé"), ["0913351394"])

    def test_dau_so_11_so_cu_doi_sang_moi(self):
        self.assertEqual(phones.normalize("01682345678"), "0382345678")
        self.assertEqual(phones.normalize("01234567890"), "0834567890")

    def test_so_co_dinh_va_84(self):
        self.assertEqual(phones.normalize("02439998888"), "02439998888")
        self.assertEqual(phones.normalize("84913351394"), "0913351394")

    def test_bo_qua_chuoi_khong_phai_sdt(self):
        self.assertEqual(phones.extract("đơn PKE1503852"), [])
        self.assertEqual(phones.extract("ngày 12.08.2026"), [])
        self.assertIsNone(phones.normalize("123"))
        self.assertIsNone(phones.normalize("0111222333"))  # đầu số không tồn tại

    def test_gom_nhieu_nguon_va_khong_trung(self):
        result = phones.extract_many(
            ["0913351394", {"phone": "0913351394"}], "gọi lại 0966611104"
        )
        self.assertEqual(result, ["0913351394", "0966611104"])


class TestTagging(unittest.TestCase):
    def test_khop_ten_nhan_bo_dau(self):
        self.assertTrue(tagging.matches({"text": "Đã chốt đơn"}, ["CHỐT ĐƠN"]))
        self.assertTrue(tagging.matches({"name": "chot don"}, ["CHỐT ĐƠN"]))
        self.assertFalse(tagging.matches({"text": "CHAT TAY"}, ["CHỐT ĐƠN"]))
        self.assertFalse(tagging.matches({"text": "Hiếu no SĐT"}, ["CHỐT ĐƠN"]))

    def test_nhan_chi_co_id_thi_tra_bang_lookup(self):
        conversation = {"tags": ["7", "12"]}
        lookup = {"7": {"text": "CHỐT ĐƠN"}, "12": {"text": "Seeding"}}
        self.assertTrue(tagging.has_closed_tag(conversation, ["CHỐT ĐƠN"], tag_lookup=lookup))
        self.assertFalse(tagging.has_closed_tag({"tags": ["12"]}, ["CHỐT ĐƠN"], tag_lookup=lookup))

    def test_nhan_mau_vang(self):
        self.assertTrue(tagging.is_yellow({"color": "#FFC107"}))
        self.assertFalse(tagging.is_yellow({"color": "#8e44ad"}))
        self.assertTrue(tagging.matches({"text": "x", "color": "#ffc107"}, [], match_yellow=True))


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.conversations = [
            {"id": "c1", "customer_name": "Oanh Tran", "updated_at": "2026-08-24T22:10:00",
             "snippet": "Bên Thịnh gọi mình số 0913.351.394",
             "tags": [{"text": "SĐT RICH NATTO"}]},
            {"id": "c2", "customer_name": "Đã mua rồi", "updated_at": "2026-08-24T21:00:00",
             "recent_phone_numbers": ["0966611104"], "tags": [{"text": "CHỐT ĐƠN"}]},
            {"id": "c3", "customer_name": "Không số", "updated_at": "2026-08-24T20:00:00",
             "snippet": "chị xem lại giúp em", "tags": []},
            {"id": "c4", "customer_name": "Trùng số", "updated_at": "2026-08-24T19:00:00",
             "recent_phone_numbers": ["0913351394"], "tags": []},
        ]

    def test_loc_dung_hoi_thoai_chua_chot(self):
        rows, stats = extract.collect(self.conversations, "123", ["CHỐT ĐƠN"])
        self.assertEqual([row["sdt"] for row in rows], ["0913351394"])
        self.assertEqual(stats["tong"], 4)
        self.assertEqual(stats["da_chot"], 1)
        self.assertEqual(stats["khong_co_sdt"], 1)
        self.assertEqual(rows[0]["tinh_trang"], "Chưa chốt")
        self.assertEqual(rows[0]["ngay"], "24/08")
        self.assertIn("pancake.vn/123", rows[0]["link"])

    def test_deep_lay_so_tu_tin_nhan(self):
        rows, _ = extract.collect(
            [self.conversations[2]], "123", ["CHỐT ĐƠN"],
            fetch_messages=lambda conv: [{"message": "em ghi số 0975216011 nhé"}],
        )
        self.assertEqual([row["sdt"] for row in rows], ["0975216011"])

    def test_thoi_gian_dang_epoch(self):
        row = extract.build_row(
            {"id": "x", "customer_name": "A", "updated_at": 1756055400,
             "recent_phone_numbers": ["0913351394"]}, "123")
        self.assertTrue(row["ngay"])


class TestExporter(unittest.TestCase):
    def test_gop_khong_trung_va_giu_ghi_chu_cu(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "out.csv")
            first = [{"ten": "A", "sdt": "0913351394", "tinh_trang": "Chưa chốt",
                      "ngay": "24/08", "ghi_chu": "", "thoi_gian": "2026-08-24 22:10", "link": "l1"}]
            merged, new_rows = exporter.merge(exporter.read_existing(path), first)
            exporter.write_csv(path, merged)
            self.assertEqual(len(new_rows), 1)

            # người dùng tự sửa ghi chú trong file
            saved = exporter.read_existing(path)
            saved["0913351394"]["ghi_chu"] = "hẹn gọi lại 17h"

            second = first + [{"ten": "B", "sdt": "0966611104", "tinh_trang": "Chưa chốt",
                               "ngay": "24/08", "ghi_chu": "mới", "thoi_gian": "2026-08-24 21:00",
                               "link": "l2"}]
            merged, new_rows = exporter.merge(saved, second)
            exporter.write_csv(path, merged)

            self.assertEqual(len(merged), 2)
            self.assertEqual([row["sdt"] for row in new_rows], ["0966611104"])
            final = exporter.read_existing(path)
            self.assertEqual(final["0913351394"]["ghi_chu"], "hẹn gọi lại 17h")


class TestClientParsing(unittest.TestCase):
    def test_doc_duoc_nhieu_kieu_payload(self):
        self.assertEqual(PancakeClient._items({"conversations": [1, 2]}), [1, 2])
        self.assertEqual(PancakeClient._items({"data": [3]}), [3])
        self.assertEqual(PancakeClient._items({"data": {"conversations": [4]}}), [4])
        self.assertEqual(PancakeClient._items([5]), [5])
        self.assertEqual(PancakeClient._items({"khong_biet": 1}), [])

    def test_phan_trang_dung_va_khong_lap_vo_han(self):
        pages = {
            1: {"conversations": [{"id": "a"}, {"id": "b"}]},
            2: {"conversations": [{"id": "b"}]},   # API trả lại trang trùng
            3: {"conversations": []},
        }
        client = PancakeClient("token", "123", "https://x")
        client._get = lambda path, params=None, retries=4: pages.get(params["page_number"], {})
        result = list(client.iter_conversations(max_pages=10))
        self.assertEqual([item["id"] for item in result], ["a", "b"])

    def test_tags_tao_bang_tra_id(self):
        client = PancakeClient("token", "123", "https://x")
        client._get = lambda path, params=None, retries=4: {
            "tags": [{"id": 7, "text": "CHỐT ĐƠN"}, {"id": 12, "text": "Seeding"}]
        }
        tags, lookup = client.get_tags()
        self.assertEqual(len(tags), 2)
        self.assertEqual(lookup["7"]["text"], "CHỐT ĐƠN")


if __name__ == "__main__":
    unittest.main()


class TestPhonesDungChung(unittest.TestCase):
    """phones.py là công cụ dùng chung -> phải chạy độc lập, không dính Pancake."""

    def _source(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "pancake_export", "phones.py",
        )
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()

    def test_khong_import_gi_trong_goi_pancake(self):
        source = self._source()
        for cam in ("from .", "from pancake_export", "import pancake_export"):
            self.assertNotIn(cam, source,
                             "phones.py không được phụ thuộc phần Pancake (%s)" % cam)

    def test_chi_dung_thu_vien_chuan(self):
        source = self._source()
        modules = re.findall(r"^\s*import\s+(\w+)", source, re.MULTILINE)
        self.assertTrue(set(modules).issubset({"re", "sys"}),
                        "phones.py chỉ được dùng thư viện chuẩn, đang có: %s" % modules)

    def test_copy_rieng_file_van_chay_duoc(self):
        """Copy nguyên file sang chỗ khác, import bằng tên trần vẫn phải chạy."""
        with tempfile.TemporaryDirectory() as folder:
            shutil.copy(
                os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "pancake_export", "phones.py",
                ),
                os.path.join(folder, "phones.py"),
            )
            ket_qua = subprocess.run(
                [sys.executable, "-c",
                 "import phones; print(phones.normalize('0913.351.394'))"],
                cwd=folder, capture_output=True, text=True,
            )
            self.assertEqual(ket_qua.returncode, 0, ket_qua.stderr)
            self.assertEqual(ket_qua.stdout.strip(), "0913351394")
