"""自动检测本机微信安装路径，无需手动配置。"""

from __future__ import annotations

import os
import subprocess
import winreg
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EXECUTABLES = ("Weixin.exe", "WeChat.exe")

REGISTRY_SOURCES: tuple[tuple[int, str, str], ...] = (
    (winreg.HKEY_CURRENT_USER, r"Software\Tencent\Weixin", "InstallPath"),
    (winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat", "InstallPath"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\Weixin", "InstallPath"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\WeChat", "InstallPath"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\WeChat", "InstallPath"),
)

UNINSTALL_KEYS = (
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\WeChat"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Weixin"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\WeChat"),
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall\WeChat"),
)


@dataclass(frozen=True)
class WeChatLocation:
    path: Path
    source: str

    @property
    def display_path(self) -> str:
        return str(self.path)


def _resolve_exe(install_dir: str | Path) -> Path | None:
    base = Path(install_dir)
    if not base.is_dir():
        return None
    for name in EXECUTABLES:
        candidate = base / name
        if candidate.is_file():
            return candidate.resolve()
    return None


def _read_registry_value(root: int, subkey: str, value_name: str) -> str | None:
    try:
        with winreg.OpenKey(root, subkey) as key:
            data, _ = winreg.QueryValueEx(key, value_name)
            if isinstance(data, str) and data.strip():
                return data.strip()
    except OSError:
        pass
    return None


def _from_registry() -> WeChatLocation | None:
    for root, subkey, value_name in REGISTRY_SOURCES:
        install_path = _read_registry_value(root, subkey, value_name)
        if not install_path:
            continue
        exe = _resolve_exe(install_path)
        if exe:
            hive = "HKCU" if root == winreg.HKEY_CURRENT_USER else "HKLM"
            return WeChatLocation(exe, f"注册表 ({hive})")
    return None


def _from_uninstall_registry() -> WeChatLocation | None:
    for root, subkey in UNINSTALL_KEYS:
        install_path = _read_registry_value(root, subkey, "InstallLocation")
        if not install_path:
            install_path = _read_registry_value(root, subkey, "DisplayIcon")
            if install_path:
                install_path = str(Path(install_path).parent)
        if not install_path:
            continue
        exe = _resolve_exe(install_path)
        if exe:
            return WeChatLocation(exe, "卸载信息注册表")
    return None


def _from_running_process() -> WeChatLocation | None:
    script = (
        "Get-Process Weixin,WeChat -ErrorAction SilentlyContinue | "
        "Select-Object -First 1 -ExpandProperty Path"
    )
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        line = result.stdout.strip()
        if line and Path(line).is_file():
            return WeChatLocation(Path(line).resolve(), "正在运行的进程")
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def _common_paths() -> Iterable[Path]:
    program_files = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs"),
    ]
    relative = [
        Path("Tencent") / "Weixin" / "Weixin.exe",
        Path("Tencent") / "WeChat" / "WeChat.exe",
        Path("Tencent") / "Weixin" / "WeChat.exe",
    ]
    for root in program_files:
        if not root:
            continue
        for rel in relative:
            yield Path(root) / rel


def _from_common_paths() -> WeChatLocation | None:
    for candidate in _common_paths():
        if candidate.is_file():
            return WeChatLocation(candidate.resolve(), "常见安装目录")
    return None


def _from_path_env() -> WeChatLocation | None:
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        folder = folder.strip('"')
        if not folder:
            continue
        for name in EXECUTABLES:
            candidate = Path(folder) / name
            if candidate.is_file():
                return WeChatLocation(candidate.resolve(), "系统 PATH")
    return None


def find_wechat() -> WeChatLocation | None:
    """按优先级依次尝试多种方式定位微信可执行文件。"""
    strategies = (
        _from_registry,
        _from_uninstall_registry,
        _from_running_process,
        _from_common_paths,
        _from_path_env,
    )
    seen: set[Path] = set()
    for strategy in strategies:
        location = strategy()
        if location and location.path not in seen:
            seen.add(location.path)
            return location
    return None
