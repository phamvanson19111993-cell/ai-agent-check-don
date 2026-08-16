"""Chế độ chạy liên tục: quét lại theo chu kỳ cho tới khi bị dừng."""

from __future__ import annotations

import logging
import signal
import threading
import time
from pathlib import Path

from . import report as report_mod
from .cleaner import run_once
from .config import Config

log = logging.getLogger(__name__)


class Watcher:
    """Vòng lặp dọn dẹp định kỳ, dừng gọn gàng khi nhận SIGINT/SIGTERM."""

    def __init__(self, cfg: Config, apply: bool | None = None) -> None:
        self.cfg = cfg
        self.apply = apply
        self._stop = threading.Event()

    def request_stop(self, *_args) -> None:
        log.info("Nhận tín hiệu dừng, sẽ kết thúc sau lượt hiện tại.")
        self._stop.set()

    def install_signal_handlers(self) -> None:
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                signal.signal(sig, self.request_stop)
            except (ValueError, OSError):  # pragma: no cover - luồng phụ
                pass

    def run(self, max_cycles: int | None = None) -> int:
        """Chạy vòng lặp. Trả về số lượt đã thực hiện."""
        interval = max(60, self.cfg.general.interval_minutes * 60)
        cycles = 0

        while not self._stop.is_set():
            cycles += 1
            try:
                rep = run_once(self.cfg, apply=self.apply)
                report_mod.save(rep, self.cfg.state_dir)
                if rep.dry_run:
                    log.info(
                        "Lượt %d: tìm thấy %d mục (%s) — chế độ chạy thử",
                        cycles, rep.found, report_mod.human_size(rep.found_bytes),
                    )
                else:
                    log.info(
                        "Lượt %d: dọn %d mục, giải phóng %s",
                        cycles, rep.cleaned, report_mod.human_size(rep.cleaned_bytes),
                    )
                if rep.errors:
                    log.warning("Lượt %d gặp %d lỗi", cycles, len(rep.errors))
            except Exception:  # noqa: BLE001 - daemon không được chết vì một lượt lỗi
                log.exception("Lượt %d thất bại", cycles)

            if max_cycles is not None and cycles >= max_cycles:
                break
            self._stop.wait(interval)

        log.info("Đã dừng sau %d lượt.", cycles)
        return cycles


def setup_logging(state_dir: Path, verbose: bool = False) -> None:
    state_dir.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    try:
        handlers.append(logging.FileHandler(state_dir / "agent.log", encoding="utf-8"))
    except OSError:
        pass
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s  %(levelname)-7s  %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
        force=True,
    )
