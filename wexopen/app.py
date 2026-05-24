"""WexOpen 主界面 — 简约精致风格。"""

from __future__ import annotations

import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

from wexopen import __version__
from wexopen.finder import WeChatLocation, find_wechat
from wexopen.launcher import LaunchError, MAX_INSTANCES, MIN_INSTANCES, launch_instances

# ── 设计系统 ──
GREEN = "#07C160"
GREEN_DARK = "#059A4E"
GREEN_SOFT = "#E7F9EF"
GREEN_MID = "#B8ECD0"
BG = "#FAFAFA"
SURFACE = "#FFFFFF"
TEXT = "#111111"
TEXT_SEC = "#6B6B6B"
TEXT_TER = "#A3A3A3"
LINE = "#EBEBEB"
RED = "#FF453A"
RED_SOFT = "#FFF1F0"

FONT = "Microsoft YaHei UI"
FONT_EN = "Segoe UI"


def _asset_path(name: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / "assets" / name


class WexOpenApp(ctk.CTk):
    WIDTH = 400
    HEIGHT = 580

    def __init__(self) -> None:
        super().__init__()
        self._location: WeChatLocation | None = None
        self._busy = False

        self.title("WexOpen")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        icon = _asset_path("icon.ico")
        if icon.is_file():
            self.iconbitmap(str(icon))

        self._center_window()
        self._build_ui()
        self.after(100, self._detect_wechat)

    def _center_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.WIDTH) // 2
        y = (self.winfo_screenheight() - self.HEIGHT) // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def _card(self, parent, **kw) -> ctk.CTkFrame:
        return ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=LINE,
            **kw,
        )

    def _build_ui(self) -> None:
        root = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        root.pack(fill="both", expand=True, padx=24, pady=24)

        # ── Logo 区 ──
        hero = ctk.CTkFrame(root, fg_color=BG, corner_radius=0, height=96)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        badge = ctk.CTkFrame(hero, width=56, height=56, corner_radius=16, fg_color=GREEN)
        badge.place(relx=0.5, rely=0, anchor="n")

        ctk.CTkLabel(
            badge, text="W", font=ctk.CTkFont(family=FONT_EN, size=26, weight="bold"), text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            hero,
            text="WexOpen",
            font=ctk.CTkFont(family=FONT_EN, size=24, weight="bold"),
            text_color=TEXT,
        ).place(relx=0.5, rely=0.62, anchor="n")

        ctk.CTkLabel(
            hero,
            text="微信多开 · 自动识别 · 无需配置",
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=TEXT_SEC,
        ).place(relx=0.5, rely=0.82, anchor="n")

        # ── 状态卡片 ──
        status_card = self._card(root)
        status_card.pack(fill="x", pady=(18, 0))

        status_inner = ctk.CTkFrame(status_card, fg_color="transparent")
        status_inner.pack(fill="x", padx=18, pady=16)

        self._status_pill = ctk.CTkFrame(status_inner, fg_color=LINE, corner_radius=20, height=32)
        self._status_pill.pack(anchor="w")

        pill_content = ctk.CTkFrame(self._status_pill, fg_color="transparent")
        pill_content.pack(padx=12, pady=6)

        self._status_dot = ctk.CTkLabel(
            pill_content, text="●", font=ctk.CTkFont(size=10), text_color=TEXT_TER, width=14,
        )
        self._status_dot.pack(side="left")

        self._status_label = ctk.CTkLabel(
            pill_content,
            text="正在检测微信…",
            font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
            text_color=TEXT_SEC,
        )
        self._status_label.pack(side="left")

        self._path_label = ctk.CTkLabel(
            status_card,
            text="",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=TEXT_TER,
            anchor="w",
            wraplength=320,
            justify="left",
        )
        self._path_label.pack(fill="x", padx=18, pady=(0, 12))

        ctk.CTkButton(
            status_card,
            text="↻  重新检测",
            height=30,
            width=100,
            corner_radius=15,
            fg_color=GREEN_SOFT,
            hover_color=GREEN_MID,
            text_color=GREEN_DARK,
            font=ctk.CTkFont(family=FONT, size=12),
            command=self._detect_wechat,
        ).pack(pady=(0, 16))

        # ── 数量卡片 ──
        count_card = self._card(root)
        count_card.pack(fill="x", pady=(12, 0))

        ctk.CTkLabel(
            count_card,
            text="打开数量",
            font=ctk.CTkFont(family=FONT, size=13, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", padx=18, pady=(18, 10))

        stepper = ctk.CTkFrame(count_card, fg_color="transparent")
        stepper.pack()

        self._count_var = tk.StringVar(value="2")

        ctk.CTkButton(
            stepper, text="−", width=48, height=48, corner_radius=24,
            fg_color=BG, hover_color=LINE, text_color=TEXT,
            font=ctk.CTkFont(size=24, weight="bold"),
            command=lambda: self._adjust_count(-1),
        ).pack(side="left")

        self._count_entry = ctk.CTkEntry(
            stepper,
            width=72,
            height=48,
            corner_radius=16,
            border_width=0,
            fg_color=BG,
            text_color=TEXT,
            font=ctk.CTkFont(family=FONT_EN, size=28, weight="bold"),
            justify="center",
            textvariable=self._count_var,
        )
        self._count_entry.pack(side="left", padx=16)
        self._count_entry.bind("<KeyRelease>", self._on_count_input)

        ctk.CTkButton(
            stepper, text="+", width=48, height=48, corner_radius=24,
            fg_color=BG, hover_color=LINE, text_color=TEXT,
            font=ctk.CTkFont(size=24, weight="bold"),
            command=lambda: self._adjust_count(1),
        ).pack(side="left")

        ctk.CTkLabel(
            count_card,
            text=f"支持 {MIN_INSTANCES} – {MAX_INSTANCES} 个窗口",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=TEXT_TER,
        ).pack(pady=(10, 16))

        # ── 快捷按钮 ──
        quick = ctk.CTkFrame(root, fg_color="transparent")
        quick.pack(fill="x", pady=(14, 0))

        for i, (n, label) in enumerate(((2, "双开"), (3, "三开"), (4, "四开"), (5, "五开"))):
            btn = ctk.CTkButton(
                quick,
                text=label,
                height=38,
                corner_radius=19,
                fg_color=SURFACE,
                hover_color=GREEN_SOFT,
                text_color=GREEN_DARK,
                border_width=1,
                border_color=LINE,
                font=ctk.CTkFont(family=FONT, size=13, weight="bold"),
                command=lambda c=n: self._set_count_and_launch(c),
            )
            btn.pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 5, 0))

        # ── 主按钮 ──
        self._launch_btn = ctk.CTkButton(
            root,
            text="启动微信",
            height=54,
            corner_radius=27,
            fg_color=GREEN,
            hover_color=GREEN_DARK,
            font=ctk.CTkFont(family=FONT, size=16, weight="bold"),
            command=self._on_launch,
        )
        self._launch_btn.pack(fill="x", pady=(22, 0))

        self._footer = ctk.CTkLabel(
            root,
            text=f"v{__version__}  ·  请先安装 PC 版微信",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=TEXT_TER,
        )
        self._footer.pack(pady=(12, 0))

    # ── 逻辑 ──

    def _parse_count(self) -> int | None:
        raw = self._count_var.get().strip()
        if not raw.isdigit():
            return None
        value = int(raw)
        if value < MIN_INSTANCES or value > MAX_INSTANCES:
            return None
        return value

    def _on_count_input(self, _event=None) -> None:
        if self._parse_count() is None and self._count_var.get().strip():
            self._count_entry.configure(fg_color=RED_SOFT)
        else:
            self._count_entry.configure(fg_color=BG)

    def _adjust_count(self, delta: int) -> None:
        current = self._parse_count() or MIN_INSTANCES
        self._count_var.set(str(max(MIN_INSTANCES, min(MAX_INSTANCES, current + delta))))
        self._count_entry.configure(fg_color=BG)

    def _set_count(self, count: int) -> None:
        self._count_var.set(str(max(MIN_INSTANCES, min(MAX_INSTANCES, count))))
        self._count_entry.configure(fg_color=BG)

    def _set_count_and_launch(self, count: int) -> None:
        self._set_count(count)
        self._on_launch()

    def _set_status_pill(self, bg: str, dot: str, text: str, text_color: str) -> None:
        self._status_pill.configure(fg_color=bg)
        self._status_dot.configure(text_color=dot)
        self._status_label.configure(text=text, text_color=text_color)

    def _detect_wechat(self) -> None:
        self._set_status_pill(LINE, TEXT_TER, "正在检测微信…", TEXT_SEC)
        self._path_label.configure(text="扫描注册表与常见安装路径…", text_color=TEXT_TER)
        self._footer.configure(text=f"v{__version__}  ·  检测中…")

        def work() -> None:
            location = find_wechat()
            self.after(0, lambda: self._apply_detection(location))

        threading.Thread(target=work, daemon=True).start()

    def _apply_detection(self, location: WeChatLocation | None) -> None:
        self._location = location
        if location:
            self._set_status_pill(GREEN_SOFT, GREEN, "已找到微信", GREEN_DARK)
            self._path_label.configure(
                text=location.display_path,
                text_color=TEXT_SEC,
            )
            self._launch_btn.configure(state="normal")
            self._footer.configure(text=f"v{__version__}  ·  点击启动或选择快捷多开")
        else:
            self._set_status_pill(RED_SOFT, RED, "未检测到微信", RED)
            self._path_label.configure(
                text="请安装 PC 版微信后，点击「重新检测」",
                text_color=TEXT_SEC,
            )
            self._launch_btn.configure(state="disabled")
            self._footer.configure(text=f"v{__version__}  ·  支持 Weixin / WeChat 全版本")

    def _on_launch(self) -> None:
        if self._busy:
            return
        count = self._parse_count()
        if count is None:
            messagebox.showwarning("数量无效", f"请输入 {MIN_INSTANCES} 到 {MAX_INSTANCES} 之间的整数。")
            return
        if not self._location:
            messagebox.showerror("未找到微信", "请先安装 PC 版微信，然后点击「重新检测」。")
            return

        self._busy = True
        self._launch_btn.configure(state="disabled", text="启动中…")
        path = self._location.path

        def work() -> None:
            try:
                launched = launch_instances(path, count)
                self.after(0, lambda: self._launch_done(True, launched))
            except LaunchError as exc:
                self.after(0, lambda: self._launch_done(False, str(exc)))

        threading.Thread(target=work, daemon=True).start()

    def _launch_done(self, ok: bool, detail: int | str) -> None:
        self._busy = False
        self._launch_btn.configure(state="normal", text="启动微信")
        if ok:
            self._footer.configure(text=f"v{__version__}  ·  已成功启动 {detail} 个窗口")
        else:
            messagebox.showerror("启动失败", str(detail))
            self._footer.configure(text=f"v{__version__}  ·  启动失败，请重试")


def run() -> None:
    app = WexOpenApp()
    app.mainloop()
