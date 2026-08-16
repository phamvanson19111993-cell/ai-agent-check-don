"""Khu cách ly: 'xoá' = chuyển vào đây, có thể khôi phục trong N ngày."""

from __future__ import annotations

import json
import shutil
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

MANIFEST_NAME = "manifest.jsonl"


@dataclass
class QuarantineEntry:
    id: str
    original_path: str
    stored_path: str
    size: int
    quarantined_at: float
    rule_id: str

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "original_path": self.original_path,
            "stored_path": self.stored_path,
            "size": self.size,
            "quarantined_at": self.quarantined_at,
            "rule_id": self.rule_id,
        }


class Quarantine:
    """Quản lý vòng đời của khu cách ly."""

    def __init__(self, directory: Path, retention_days: int = 7) -> None:
        self.dir = directory
        self.retention_days = retention_days
        self.manifest = self.dir / MANIFEST_NAME

    def _ensure(self) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)

    def store(self, path: Path, rule_id: str, size: int) -> QuarantineEntry:
        """Chuyển `path` vào khu cách ly và ghi lại thông tin khôi phục."""
        self._ensure()
        entry_id = uuid.uuid4().hex[:12]
        bucket = self.dir / time.strftime("%Y-%m-%d") / entry_id
        bucket.mkdir(parents=True, exist_ok=True)
        target = bucket / path.name

        shutil.move(str(path), str(target))

        entry = QuarantineEntry(
            id=entry_id,
            original_path=str(path),
            stored_path=str(target),
            size=size,
            quarantined_at=time.time(),
            rule_id=rule_id,
        )
        with self.manifest.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry.as_dict(), ensure_ascii=False) + "\n")
        return entry

    def entries(self) -> list[QuarantineEntry]:
        if not self.manifest.exists():
            return []
        out: list[QuarantineEntry] = []
        for line in self.manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                out.append(QuarantineEntry(**json.loads(line)))
            except (json.JSONDecodeError, TypeError):
                continue
        return out

    def restore(self, entry_id: str) -> Path:
        """Đưa một mục về đúng vị trí cũ."""
        for entry in self.entries():
            if entry.id != entry_id:
                continue
            stored = Path(entry.stored_path)
            original = Path(entry.original_path)
            if not stored.exists():
                raise FileNotFoundError(f"mục {entry_id} không còn trong khu cách ly")
            original.parent.mkdir(parents=True, exist_ok=True)
            if original.exists():
                original = original.with_name(f"{original.name}.restored")
            shutil.move(str(stored), str(original))
            self._drop(entry_id)
            return original
        raise KeyError(f"không tìm thấy mục {entry_id}")

    def _drop(self, entry_id: str) -> None:
        remaining = [e for e in self.entries() if e.id != entry_id]
        with self.manifest.open("w", encoding="utf-8") as fh:
            for e in remaining:
                fh.write(json.dumps(e.as_dict(), ensure_ascii=False) + "\n")

    def purge(self, now: float | None = None) -> tuple[int, int]:
        """Xoá hẳn những mục đã quá hạn. Trả về (số mục, số byte)."""
        now = now if now is not None else time.time()
        cutoff = now - self.retention_days * 86400
        kept: list[QuarantineEntry] = []
        removed = freed = 0

        for entry in self.entries():
            if entry.quarantined_at > cutoff:
                kept.append(entry)
                continue
            stored = Path(entry.stored_path)
            try:
                if stored.is_dir() and not stored.is_symlink():
                    shutil.rmtree(stored, ignore_errors=True)
                elif stored.exists() or stored.is_symlink():
                    stored.unlink(missing_ok=True)
                removed += 1
                freed += entry.size
                parent = stored.parent
                if parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()
            except OSError:
                kept.append(entry)

        if self.manifest.exists() or kept:
            self._ensure()
            with self.manifest.open("w", encoding="utf-8") as fh:
                for e in kept:
                    fh.write(json.dumps(e.as_dict(), ensure_ascii=False) + "\n")

        return removed, freed

    def usage_bytes(self) -> int:
        total = 0
        for entry in self.entries():
            total += entry.size
        return total
