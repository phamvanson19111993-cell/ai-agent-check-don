# ai-agent-check-don

Bộ công cụ **chăm sóc khách hàng qua Zalo theo chu kỳ 10 ngày**: kịch bản, thư viện
tin nhắn và script tính lịch nhắn tin cho từng khách.

## Nội dung

| Tệp | Mô tả |
|---|---|
| [`docs/playbook-cskh-zalo-10-ngay.md`](docs/playbook-cskh-zalo-10-ngay.md) | Quy trình đầy đủ: nguyên tắc, lịch 36 lượt/năm, phân khúc khách, xử lý phản hồi, chống spam |
| [`docs/thu-vien-tin-nhan.md`](docs/thu-vien-tin-nhan.md) | 50+ mẫu tin nhắn tiếng Việt theo 8 nhóm chủ đề + mẫu trả lời nhanh |
| [`docs/huong-dan-thao-tac-tren-zalo.md`](docs/huong-dan-thao-tac-tren-zalo.md) | Thao tác thật trên Zalo PC: đặt tên hội thoại, thẻ phân loại, tin nhắn nhanh, quy trình 15 phút/sáng, lưu ý pháp lý ngành TPCN |
| [`data/mau_tin_nhan.json`](data/mau_tin_nhan.json) | Mẫu tin dạng dữ liệu để tự động hoá |
| [`data/danh_sach_khach_mau.csv`](data/danh_sach_khach_mau.csv) | File theo dõi khách mẫu (chép ra rồi điền khách thật) |
| [`docs/dang-ky-zalo-oa-zns.md`](docs/dang-ky-zalo-oa-zns.md) | Checklist hồ sơ đăng ký Zalo OA + ZBS (ZNS), 5 mẫu tin soạn sẵn để nộp duyệt, và phân định việc nào nhắn tay việc nào dùng ZNS |
| [`scripts/lich_cskh.py`](scripts/lich_cskh.py) | Script in ra khách đến hạn nhắn hôm nay + gợi ý tin nhắn |

## Cách dùng nhanh

```bash
# Xem khách cần nhắn hôm nay
python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv

# Xem lịch của một ngày bất kỳ
python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv --ngay 2026-09-02

# Xem toàn bộ khách, kể cả chưa tới hạn
python3 scripts/lich_cskh.py data/danh_sach_khach_mau.csv --tat-ca
```

Script không cần cài thêm thư viện (chỉ dùng Python 3 chuẩn).

## Quy tắc cốt lõi

1. **10 ngày/lần** – VIP 7 ngày, khách ngủ đông 20 ngày, khách im lặng 30 ngày.
2. **Tỷ lệ 3–1** – 3 tin hỏi thăm/hữu ích mới có 1 tin nhắc bán hàng.
3. **Khách không rep 3 lượt liên tiếp** → tự động giãn chu kỳ, tránh bị chặn.
4. **Luôn cá nhân hoá** – script chỉ gợi ý, người gửi phải sửa ít nhất 1 chi tiết riêng.
5. **Giờ vàng** – 8h30–11h · 14h–17h · 19h30–21h.

## Cột trong file theo dõi khách

`ten, xung_ho, so_dien_thoai, ngay_lien_he_cuoi, ngay_mua_cuoi, san_pham, phan_khuc,
so_lan_khong_rep, sinh_nhat, ghi_chu`

Giá trị `phan_khuc`: `moi` · `than_thiet` · `vip` · `ngu_dong` · `im_lang`
