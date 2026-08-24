"""Client gọi API Pancake (có retry, phân trang, chịu được thay đổi payload)."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "pancake-export/1.0 (+https://github.com)"


class PancakeError(RuntimeError):
    pass


class PancakeClient:
    def __init__(self, access_token, page_id, api_base, timeout=30, debug=False):
        self.access_token = access_token
        self.page_id = str(page_id)
        self.api_base = api_base.rstrip("/")
        self.timeout = timeout
        self.debug = debug

    # ---------- hạ tầng ----------

    def _get(self, path, params=None, retries=4):
        params = dict(params or {})
        params.setdefault("access_token", self.access_token)
        url = "%s%s?%s" % (self.api_base, path, urllib.parse.urlencode(params))

        delay = 2
        last_error = None
        for attempt in range(retries):
            try:
                request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    body = response.read().decode("utf-8", "replace")
                if self.debug:
                    print("[debug] GET %s -> %s ký tự" % (path, len(body)))
                return json.loads(body)
            except urllib.error.HTTPError as error:
                detail = error.read().decode("utf-8", "replace")[:400]
                if error.code in (401, 403):
                    raise PancakeError(
                        "Pancake từ chối truy cập (HTTP %s). Kiểm tra lại API key/quyền của page.\n%s"
                        % (error.code, detail)
                    )
                if error.code == 404:
                    raise PancakeError("Không tìm thấy endpoint %s (HTTP 404).\n%s" % (path, detail))
                last_error = PancakeError("HTTP %s tại %s: %s" % (error.code, path, detail))
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                last_error = PancakeError("Lỗi kết nối %s: %s" % (path, error))

            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
        raise last_error

    @staticmethod
    def _items(payload):
        """Lấy danh sách bản ghi từ payload dù Pancake bọc ở khoá nào."""
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            return []
        for key in ("conversations", "data", "tags", "categories", "items", "result"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                for inner_key in ("conversations", "data", "items"):
                    inner = value.get(inner_key)
                    if isinstance(inner, list):
                        return inner
        return []

    # ---------- endpoint ----------

    def get_tags(self):
        """Danh sách nhãn của page. Trả về (list nhãn, dict tra id -> nhãn)."""
        payload = self._get("/v1/pages/%s/tags" % self.page_id)
        tags = self._items(payload)
        lookup = {}
        for tag in tags:
            if isinstance(tag, dict):
                for key in ("id", "tag_id", "value"):
                    if tag.get(key) is not None:
                        lookup[str(tag[key])] = tag
        return tags, lookup

    def iter_conversations(self, since=None, until=None, max_pages=200, page_size=50):
        """Duyệt toàn bộ hội thoại theo trang, dừng khi hết dữ liệu."""
        seen_ids = set()
        for page_number in range(1, max_pages + 1):
            params = {"page_number": page_number, "page_size": page_size}
            if since:
                params["since"] = int(since)
            if until:
                params["until"] = int(until)

            payload = self._get("/v1/pages/%s/conversations" % self.page_id, params)
            batch = self._items(payload)
            if not batch:
                return

            fresh = 0
            for conversation in batch:
                if not isinstance(conversation, dict):
                    continue
                conversation_id = str(
                    conversation.get("id")
                    or conversation.get("conversation_id")
                    or conversation.get("thread_id")
                    or ""
                )
                if conversation_id and conversation_id in seen_ids:
                    continue
                if conversation_id:
                    seen_ids.add(conversation_id)
                fresh += 1
                yield conversation

            # Không còn bản ghi mới -> API đang lặp lại trang, thoát để khỏi vòng vô hạn.
            if fresh == 0:
                return

    def get_messages(self, conversation_id, customer_id=None, limit=30):
        """Lấy tin nhắn của một hội thoại (dùng để dò số điện thoại trong nội dung)."""
        params = {"limit": limit}
        if customer_id:
            params["customer_id"] = customer_id
        try:
            payload = self._get(
                "/v1/pages/%s/conversations/%s/messages" % (self.page_id, conversation_id),
                params,
                retries=2,
            )
        except PancakeError:
            return []
        return self._items(payload)
