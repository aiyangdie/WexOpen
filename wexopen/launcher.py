"""启动多个微信实例。"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
MAX_INSTANCES = 20
MIN_INSTANCES = 1
LAUNCH_INTERVAL_SEC = 0.28


class LaunchError(Exception):
    pass


def clamp_count(count: int) -> int:
    return max(MIN_INSTANCES, min(MAX_INSTANCES, int(count)))


def launch_instances(exe_path: Path, count: int) -> int:
    """启动指定数量的微信窗口，返回实际启动次数。"""
    path = Path(exe_path)
    if not path.is_file():
        raise LaunchError(f"找不到微信程序：{path}")

    total = clamp_count(count)
    launched = 0
    for _ in range(total):
        subprocess.Popen(
            [str(path)],
            shell=False,
            cwd=str(path.parent),
            creationflags=CREATE_NO_WINDOW,
            close_fds=True,
        )
        launched += 1
        if launched < total:
            time.sleep(LAUNCH_INTERVAL_SEC)
    return launched
