"""WexOpen 主界面 v2.3 — 极简 UI 重设计。"""

from __future__ import annotations

import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from wexopen import __version__
from wexopen.about import AboutDialog
from wexopen.finder import WeChatLocation, find_wechat
from wexopen.launcher import LaunchError, MAX_INSTANCES, MIN_INSTANCES, launch_instances
from wexopen.meta import AUTHOR, AUTHOR_EMAIL, GITHUB_URL
from wexopen.theme import C, WIN_H_BIZ, WIN_H_PURE, WIN_W, font, ghost_btn, primary_btn

QUICK_PRESETS = ((2, "双开"), (3, "三开"), (4, "四开"), (5, "五开"))


def _asset_path(name: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / "assets" / name


def _enable_win_dpi() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def _short_path(path: str, max_len: int = 42) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3) :]


class WexOpenApp(ctk.CTk):
    def __init__(self, *, business: bool = False) -> None:
        _enable_win_dpi()
        super().__init__()

        self._business = business
        self._location: WeChatLocation | None = None
        self._busy = False
        self._chip_btns: dict[int, ctk.CTkButton] = {}
        self._active_chip: int | None = 2

        ctk.set_appearance_mode("light")
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        tag = "商业" if business else "纯净"
        self.title(f"WexOpen · {tag}")
        self._height = WIN_H_BIZ if business else WIN_H_PURE
        self.geometry(f"{WIN_W}x{self._height}")
        self.minsize(WIN_W, self._height)
        self.resizable(False, False)
        self.configure(fg_color=C["bg"])

        icon = _asset_path("icon.ico")
        if icon.is_file():
            self.iconbitmap(str(icon))

        self._build_ui()
        self._center_window()
        self.after(80, self._detect_wechat)

    def _center_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - WIN_W) // 2
        y = (self.winfo_screenheight() - self._height) // 2
        self.geometry(f"{WIN_W}x{self._height}+{x}+{y}")

    def _show_about(self) -> None:
        AboutDialog(self, business=self._business)

    def _copy_contact(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(AUTHOR_EMAIL)
        self._hint.configure(text=f"已复制 {AUTHOR_EMAIL}")

    def _build_ui(self) -> None:
        root = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        root.pack(fill="both", expand=True, padx=24, pady=22)

        # ── 顶栏 ──
        top = ctk.CTkFrame(root, fg_color=C["bg"], corner_radius=0)
        top.pack(fill="x")

        mark = ctk.CTkFrame(top, width=40, height=40, corner_radius=10, fg_color=C["green"])
        mark.pack(side="left")
        mark.pack_propagate(False)
        ctk.CTkLabel(mark, text="W", font=font(18, "bold"), text_color="white").place(
            relx=0.5, rely=0.5, anchor="center",
        )

        titles = ctk.CTkFrame(top, fg_color=C["bg"], corner_radius=0)
        titles.pack(side="left", padx=(12, 0), fill="x", expand=True)
        ctk.CTkLabel(titles, text="WexOpen", font=font(18, "bold"), text_color=C["text"], anchor="w").pack(anchor="w")
        sub = f"微信多开 · {'商业版' if self._business else '纯净版'}"
        ctk.CTkLabel(titles, text=sub, font=font(11), text_color=C["text3"], anchor="w").pack(anchor="w")

        if self._business:
            ghost_btn(top, "关于", self._show_about, width=44).pack(side="right")

        # ── 主面板（单容器，减少卡片嵌套）──
        panel = ctk.CTkFrame(root, fg_color=C["surface"], corner_radius=16)
        panel.pack(fill="x", pady=(20, 0))

        # 状态行
        status_row = ctk.CTkFrame(panel, fg_color="transparent")
        status_row.pack(fill="x", padx=18, pady=(16, 4))

        self._status_dot = ctk.CTkLabel(status_row, text="●", font=font(10), text_color=C["text3"], width=14)
        self._status_dot.pack(side="left")

        self._status_label = ctk.CTkLabel(
            status_row, text="检测中", font=font(12, "bold"), text_color=C["text2"], anchor="w",
        )
        self._status_label.pack(side="left")

        ghost_btn(status_row, "刷新", self._detect_wechat, width=40).pack(side="right")

        self._path_label = ctk.CTkLabel(
            panel, text="", font=font(10), text_color=C["text3"],
            anchor="w", wraplength=280, justify="left",
        )
        self._path_label.pack(fill="x", padx=18, pady=(0, 14))

        # 分隔
        ctk.CTkFrame(panel, height=1, fg_color=C["line"], corner_radius=0).pack(fill="x", padx=18)

        # 数量区
        ctk.CTkLabel(
            panel, text="打开数量", font=font(11), text_color=C["text3"],
        ).pack(pady=(16, 10))

        step = ctk.CTkFrame(panel, fg_color="transparent")
        step.pack()

        self._count_var = tk.StringVar(value="2")

        def _step_btn(sym: str, delta: int) -> ctk.CTkButton:
            return ctk.CTkButton(
                step, text=sym, width=40, height=40, corner_radius=20,
                fg_color=C["bg"], hover_color=C["line"], text_color=C["text"],
                font=font(18, "bold"),
                command=lambda: self._adjust_count(delta),
            )

        _step_btn("-", -1).pack(side="left")
        self._count_entry = ctk.CTkEntry(
            step, width=72, height=52, corner_radius=12,
            border_width=0, fg_color=C["bg"], text_color=C["text"],
            font=font(32, "bold"), justify="center", textvariable=self._count_var,
        )
        self._count_entry.pack(side="left", padx=16)
        self._count_entry.bind("<KeyRelease>", self._on_count_input)
        _step_btn("+", 1).pack(side="left")

        # 快捷数字芯片
        chips = ctk.CTkFrame(panel, fg_color="transparent")
        chips.pack(pady=(14, 18))
        for n, label in QUICK_PRESETS:
            btn = ctk.CTkButton(
                chips, text=label, width=58, height=32, corner_radius=16,
                fg_color=C["bg"], hover_color=C["green_soft"],
                text_color=C["text2"], font=font(13, "bold"),
                command=lambda c=n: self._pick_chip(c),
            )
            btn.pack(side="left", padx=4)
            self._chip_btns[n] = btn
        self._highlight_chip(2)

        # 启动
        self._launch_btn = primary_btn(panel, "启动微信", self._on_launch)
        self._launch_btn.pack(fill="x", padx=18, pady=(0, 18))

        # ── 商业合作（商业版）──
        if self._business:
            self._build_biz_strip(root)

        # ── 底栏 ──
        self._hint = ctk.CTkLabel(
            root, text=f"v{__version__}", font=font(10), text_color=C["text3"],
        )
        self._hint.pack(pady=(14, 0))

        if self._business:
            links = ctk.CTkFrame(root, fg_color=C["bg"], corner_radius=0)
            links.pack(pady=(6, 0))
            for i, (txt, cmd) in enumerate(
                (
                    ("学习声明", self._show_about),
                    (AUTHOR, self._show_about),
                    ("GitHub", lambda: webbrowser.open(GITHUB_URL)),
                )
            ):
                if i:
                    ctk.CTkLabel(links, text="·", font=font(10), text_color=C["line"]).pack(side="left", padx=2)
                ghost_btn(links, txt, cmd, width=56).pack(side="left")

    def _build_biz_strip(self, parent) -> None:
        strip = ctk.CTkFrame(
            parent, fg_color=C["amber_soft"], corner_radius=12,
            border_width=1, border_color=C["amber_line"],
        )
        strip.pack(fill="x", pady=(14, 0))

        ctk.CTkLabel(
            strip, text="商务合作",
            font=font(12, "bold"), text_color=C["amber"],
        ).pack(anchor="w", padx=14, pady=(12, 2))

        ctk.CTkLabel(
            strip,
            text="接广告 · 有合作意向欢迎联系",
            font=font(11), text_color=C["text2"], anchor="w",
        ).pack(anchor="w", padx=14)

        row = ctk.CTkFrame(strip, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 12))

        ctk.CTkButton(
            row, text="复制邮箱", height=30, corner_radius=8,
            fg_color=C["bg"], hover_color=C["amber_line"], text_color=C["amber"],
            border_width=1, border_color=C["amber_line"], font=font(11),
            command=self._copy_contact,
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            row, text="联系我", height=30, corner_radius=8,
            fg_color=C["amber"], hover_color="#B08820", text_color="white",
            font=font(11),
            command=lambda: webbrowser.open(GITHUB_URL),
        ).pack(side="left", expand=True, fill="x")

    def _highlight_chip(self, n: int | None) -> None:
        self._active_chip = n
        for num, btn in self._chip_btns.items():
            if num == n:
                btn.configure(fg_color=C["green_soft"], text_color=C["green"], border_width=0)
            else:
                btn.configure(fg_color=C["bg"], text_color=C["text2"], border_width=0)

    def _pick_chip(self, count: int) -> None:
        self._set_count(count)
        self._highlight_chip(count)

    def _parse_count(self) -> int | None:
        raw = self._count_var.get().strip()
        if not raw.isdigit():
            return None
        value = int(raw)
        if value < MIN_INSTANCES or value > MAX_INSTANCES:
            return None
        return value

    def _on_count_input(self, _event=None) -> None:
        value = self._parse_count()
        if value is None and self._count_var.get().strip():
            self._count_entry.configure(fg_color=C["red_soft"])
            self._highlight_chip(None)
        else:
            self._count_entry.configure(fg_color=C["bg"])
            if value in self._chip_btns:
                self._highlight_chip(value)
            else:
                self._highlight_chip(None)

    def _adjust_count(self, delta: int) -> None:
        current = self._parse_count() or MIN_INSTANCES
        n = max(MIN_INSTANCES, min(MAX_INSTANCES, current + delta))
        self._set_count(n)
        self._highlight_chip(n if n in self._chip_btns else None)

    def _set_count(self, count: int) -> None:
        n = max(MIN_INSTANCES, min(MAX_INSTANCES, count))
        self._count_var.set(str(n))
        self._count_entry.configure(fg_color=C["bg"])

    def _set_count_and_launch(self, count: int) -> None:
        self._set_count(count)
        self._pick_chip(count)
        self._on_launch()

    def _detect_wechat(self) -> None:
        self._status_dot.configure(text_color=C["text3"])
        self._status_label.configure(text="检测中")
        self._path_label.configure(text="")
        self._hint.configure(text="正在扫描...")

        def work() -> None:
            loc = find_wechat()
            self.after(0, lambda: self._apply_detection(loc))

        threading.Thread(target=work, daemon=True).start()

    def _apply_detection(self, location: WeChatLocation | None) -> None:
        self._location = location
        if location:
            self._status_dot.configure(text_color=C["green"])
            self._status_label.configure(text="微信已就绪")
            self._path_label.configure(text=_short_path(location.display_path))
            self._launch_btn.configure(state="normal")
            self._hint.configure(text=f"v{__version__}  ·  选择数量后启动")
        else:
            self._status_dot.configure(text_color=C["red"])
            self._status_label.configure(text="未找到微信")
            self._path_label.configure(text="请先安装 PC 版微信")
            self._launch_btn.configure(state="disabled")
            self._hint.configure(text=f"v{__version__}  ·  安装后点刷新")

    def _on_launch(self) -> None:
        if self._busy:
            return
        count = self._parse_count()
        if count is None:
            messagebox.showwarning("提示", f"请输入 {MIN_INSTANCES}–{MAX_INSTANCES} 的整数")
            return
        if not self._location:
            messagebox.showerror("提示", "未找到微信，请先安装后点刷新")
            return

        self._busy = True
        self._launch_btn.configure(state="disabled", text="启动中")
        path = self._location.path

        def work() -> None:
            try:
                n = launch_instances(path, count)
                self.after(0, lambda: self._launch_done(True, n))
            except LaunchError as e:
                self.after(0, lambda: self._launch_done(False, str(e)))

        threading.Thread(target=work, daemon=True).start()

    def _launch_done(self, ok: bool, detail: int | str) -> None:
        self._busy = False
        self._launch_btn.configure(state="normal", text="启动微信")
        if ok:
            self._hint.configure(text=f"已启动 {detail} 个窗口")
        else:
            messagebox.showerror("失败", str(detail))
            self._hint.configure(text="启动失败，请重试")


def run(*, business: bool = False) -> None:
    WexOpenApp(business=business).mainloop()
