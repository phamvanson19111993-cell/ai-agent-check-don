"""Đồng bộ kết quả lên Google Sheet trên Drive (chỉ thêm số chưa có)."""

import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEET_COLUMNS = ["ten", "sdt", "tinh_trang", "ngay", "ghi_chu"]


class SheetsUnavailable(RuntimeError):
    pass


def _service(service_account_file):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as error:
        raise SheetsUnavailable(
            "Chưa cài thư viện Google. Chạy:\n"
            "  pip install google-api-python-client google-auth\n(%s)" % error
        )
    if not service_account_file or not os.path.exists(service_account_file):
        raise SheetsUnavailable(
            "Chưa có file credentials service account.\n"
            "Đặt đường dẫn vào GOOGLE_SERVICE_ACCOUNT_FILE trong .env, "
            "và chia sẻ Google Sheet cho email của service account (quyền Editor)."
        )
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=credentials, cache_discovery=False)


def existing_phones(service, sheet_id, tab=""):
    """Đọc cột SĐT đang có trên sheet để không ghi trùng."""
    range_name = ("%s!B:B" % tab) if tab else "B:B"
    response = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=sheet_id, range=range_name)
        .execute()
    )
    phones = set()
    for row in response.get("values", []):
        if not row:
            continue
        value = str(row[0]).strip()
        if not value:
            continue
        digits = "".join(ch for ch in value if ch.isdigit())
        if digits:
            # Sheet cũ lưu số mất số 0 đầu -> chuẩn hoá lại để so sánh.
            phones.add(digits if digits.startswith("0") else "0" + digits)
    return phones


def append_rows(sheet_id, rows, service_account_file, tab=""):
    """Thêm các dòng chưa có vào cuối sheet. Trả về số dòng đã thêm."""
    service = _service(service_account_file)
    already = existing_phones(service, sheet_id, tab)

    payload = []
    for row in rows:
        if row["sdt"] in already:
            continue
        already.add(row["sdt"])
        payload.append([row.get(column, "") for column in SHEET_COLUMNS])

    if not payload:
        return 0

    range_name = ("%s!A:E" % tab) if tab else "A:E"
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_name,
        # RAW để số điện thoại giữ nguyên số 0 đầu, không bị Sheets đổi thành số.
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": payload},
    ).execute()
    return len(payload)
