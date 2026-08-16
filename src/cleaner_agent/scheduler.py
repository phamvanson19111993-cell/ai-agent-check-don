"""Cài agent chạy nền cùng hệ điều hành (systemd / launchd / Task Scheduler)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SERVICE_NAME = "cleaner-agent"


def _python() -> str:
    return shutil.which("python3") or sys.executable


def _command(apply: bool) -> list[str]:
    cmd = [_python(), "-m", "cleaner_agent", "watch"]
    if apply:
        cmd.append("--apply")
    return cmd


def systemd_unit(apply: bool) -> str:
    exec_start = " ".join(_command(apply))
    return f"""\
[Unit]
Description=AI Agent don rac may tinh
After=network.target

[Service]
Type=simple
ExecStart={exec_start}
Restart=on-failure
RestartSec=60
Nice=10
IOSchedulingClass=idle

[Install]
WantedBy=default.target
"""


def launchd_plist(apply: bool, interval_minutes: int) -> str:
    args = "".join(f"        <string>{part}</string>\n" for part in _command(apply))
    return f"""\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.local.{SERVICE_NAME}</string>
    <key>ProgramArguments</key>
    <array>
{args}    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>{interval_minutes * 60}</integer>
    <key>LowPriorityIO</key>
    <true/>
    <key>Nice</key>
    <integer>10</integer>
</dict>
</plist>
"""


def install(apply: bool, interval_minutes: int, write: bool = False) -> str:
    """Trả về hướng dẫn cài đặt; `write=True` thì ghi luôn file cấu hình dịch vụ."""
    if sys.platform == "win32":
        cmd = " ".join(f'"{p}"' if " " in p else p for p in _command(apply))
        return (
            "Windows — chạy lệnh sau trong PowerShell (quyền người dùng thường):\n\n"
            f"  schtasks /Create /SC ONLOGON /TN {SERVICE_NAME} "
            f'/TR "{cmd}" /F\n\n'
            f"Gỡ bỏ:  schtasks /Delete /TN {SERVICE_NAME} /F"
        )

    if sys.platform == "darwin":
        target = Path.home() / "Library" / "LaunchAgents" / f"com.local.{SERVICE_NAME}.plist"
        content = launchd_plist(apply, interval_minutes)
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            return (
                f"Đã ghi {target}\n\n"
                f"Bật:  launchctl load -w {target}\n"
                f"Tắt:  launchctl unload -w {target}"
            )
        return f"Nội dung cho {target}:\n\n{content}"

    target = Path.home() / ".config" / "systemd" / "user" / f"{SERVICE_NAME}.service"
    content = systemd_unit(apply)
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return (
            f"Đã ghi {target}\n\n"
            "Bật:\n"
            "  systemctl --user daemon-reload\n"
            f"  systemctl --user enable --now {SERVICE_NAME}\n\n"
            f"Xem log:  journalctl --user -u {SERVICE_NAME} -f\n"
            f"Tắt:      systemctl --user disable --now {SERVICE_NAME}"
        )
    return f"Nội dung cho {target}:\n\n{content}"
