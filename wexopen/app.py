"""WexOpen 主界面 — 简约风格微信多开工具。"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from wexopen.finder import WeChatLocation, find_wechat
from wexopen.launcher import LaunchError, MAX_INSTANCES, MIN_INSTANCES, launch_instances

# 微信品牌色 + 简约浅色主题
WECHAT_GREEN = "#07C160"
WECHAT_GREEN_HOVER = "#06AD56"
WECHAT_GREEN_LIGHT = "#E8F8EF"
BG = "#F5F6F8"
CARD = "#FFFFFF"
TEXT = "#1D1D1F"
TEXT_MUTED = "#86868B"
BORDER = "#E5E5EA"
DANGER = "#FF3B30"
DANGER_LIGHT = "#FFF0EF"


class WexOpenApp(ctk.CTk):
    WIDTH = 420
    HEIGHT = 520

    def __init__(self) -> None:
        super().__init__()
        self._location: WeChatLocation | None = None
        self._busy = False

        self.title("WexOpen · 微信多开")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.configure(fg_color=BG)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self._build_ui()
        self.after(120, self._detect_wechat)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # ── 顶栏 ──
        header = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(28, 0))

        ctk.CTkLabel(
            header,
            text="WexOpen",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="微信多开助手 · 自动识别 · 即开即用",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED,
        ).pack(anchor="w", pady=(4, 0))

        # ── 微信路径卡片 ──
        path_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16, border_width=1, border_color=BORDER)
        path_card.grid(row=1, column=0, sticky="ew", padx=28, pady=(24, 0))
        path_card.grid_columnconfigure(0, weight=1)

        row_top = ctk.CTkFrame(path_card, fg_color="transparent")
        row_top.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 6))

        self._status_dot = ctk.CTkLabel(
            row_top, text="●", font=ctk.CTkFont(size=14), text_color=TEXT_MUTED, width=20,
        )
        self._status_dot.pack(side="left")

        self._status_label = ctk.CTkLabel(
            row_top,
            text="正在检测微信…",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT,
            anchor="w",
        )
        self._status_label.pack(side="left", fill="x", expand=True)

        self._path_label = ctk.CTkLabel(
            path_card,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
            anchor="w",
            wraplength=340,
            justify="left",
        )
        self._path_label.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 14))

        ctk.CTkButton(
            path_card,
            text="重新检测",
            width=80,
            height=28,
            corner_radius=8,
            fg_color="transparent",
            hover_color=WECHAT_GREEN_LIGHT,
            text_color=WECHAT_GREEN,
            border_width=1,
            border_color=WECHAT_GREEN,
            font=ctk.CTkFont(size=12),
            command=self._detect_wechat,
        ).grid(row=0, column=1, rowspan=2, padx=(0, 14), pady=14)

        # ── 数量选择卡片 ──
        count_card = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16, border_width=1, border_color=BORDER)
        count_card.grid(row=2, column=0, sticky="ew", padx=28, pady=(16, 0))

        ctk.CTkLabel(
            count_card,
            text="打开数量",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", padx=18, pady=(16, 8))

        stepper = ctk.CTkFrame(count_card, fg_color="transparent")
        stepper.pack(pady=(0, 6))

        self._count_var = tk.StringVar(value="2")

        ctk.CTkButton(
            stepper, text="−", width=44, height=44, corner_radius=12,
            fg_color=BG, hover_color=BORDER, text_color=TEXT,
            font=ctk.CTkFont(size=22, weight="bold"),
            command=lambda: self._adjust_count(-1),
        ).pack(side="left", padx=(0, 12))

        self._count_entry = ctk.CTkEntry(
            stepper,
            width=80,
            height=44,
            corner_radius=12,
            border_width=1,
            border_color=BORDER,
            fg_color=BG,
            text_color=TEXT,
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="center",
            textvariable=self._count_var,
        )
        self._count_entry.pack(side="left")
        self._count_entry.bind("<KeyRelease>", self._on_count_input)

        ctk.CTkButton(
            stepper, text="+", width=44, height=44, corner_radius=12,
            fg_color=BG, hover_color=BORDER, text_color=TEXT,
            font=ctk.CTkFont(size=22, weight="bold"),
            command=lambda: self._adjust_count(1),
        ).pack(side="left", padx=(12, 0))

        ctk.CTkLabel(
            count_card,
            text=f"可输入 {MIN_INSTANCES}–{MAX_INSTANCES}，默认双开",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED,
        ).pack(pady=(4, 16))

        # ── 快捷双开 ──
        quick_row = ctk.CTkFrame(self, fg_color="transparent")
        quick_row.grid(row=3, column=0, sticky="ew", padx=28, pady=(14, 0))

        for n, label in ((2, "双开"), (3, "三开"), (4, "四开")):
            ctk.CTkButton(
                quick_row,
                text=label,
                height=36,
                corner_radius=10,
                fg_color=CARD,
                hover_color=WECHAT_GREEN_LIGHT,
                text_color=WECHAT_GREEN,
                border_width=1,
                border_color=BORDER,
                font=ctk.CTkFont(size=13),
                command=lambda c=n: self._set_count_and_launch(c),
            ).pack(side="left", expand=True, fill="x", padx=(0 if n == 2 else 6, 0))

        # ── 主按钮 ──
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=4, column=0, sticky="sew", padx=28, pady=(20, 28))

        self._launch_btn = ctk.CTkButton(
            btn_frame,
            text="启  动  微  信",
            height=52,
            corner_radius=14,
            fg_color=WECHAT_GREEN,
            hover_color=WECHAT_GREEN_HOVER,
            font=ctk.CTkFont(size=17, weight="bold"),
            command=self._on_launch,
        )
        self._launch_btn.pack(fill="x")

        self._footer = ctk.CTkLabel(
            btn_frame,
            text="首次使用请先安装 PC 版微信",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
        )
        self._footer.pack(pady=(10, 0))

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
        value = self._parse_count()
        if value is None and self._count_var.get().strip():
            self._count_entry.configure(border_color=DANGER)
        else:
            self._count_entry.configure(border_color=BORDER)

    def _adjust_count(self, delta: int) -> None:
        current = self._parse_count() or MIN_INSTANCES
        self._count_var.set(str(clamp := max(MIN_INSTANCES, min(MAX_INSTANCES, current + delta))))
        self._count_entry.configure(border_color=BORDER)

    def _set_count(self, count: int) -> None:
        self._count_var.set(str(max(MIN_INSTANCES, min(MAX_INSTANCES, count))))
        self._count_entry.configure(border_color=BORDER)

    def _set_count_and_launch(self, count: int) -> None:
        self._set_count(count)
        self._on_launch()

    def _detect_wechat(self) -> None:
        self._status_dot.configure(text_color=TEXT_MUTED)
        self._status_label.configure(text="正在检测微信…")
        self._path_label.configure(text="")
        self._footer.configure(text="扫描注册表、常见路径与运行进程…")

        def work() -> None:
            location = find_wechat()
            self.after(0, lambda: self._apply_detection(location))

        threading.Thread(target=work, daemon=True).start()

    def _apply_detection(self, location: WeChatLocation | None) -> None:
        self._location = location
        if location:
            self._status_dot.configure(text_color=WECHAT_GREEN)
            self._status_label.configure(text="已找到微信")
            self._path_label.configure(text=f"{location.display_path}\n来源：{location.source}")
            self._launch_btn.configure(state="normal")
            self._footer.configure(text="点击启动，或选择上方快捷多开")
        else:
            self._status_dot.configure(text_color=DANGER)
            self._status_label.configure(text="未检测到微信")
            self._path_label.configure(
                text="请确认已安装 PC 版微信，安装后点「重新检测」",
                text_color=DANGER,
            )
            self._launch_btn.configure(state="disabled")
            self._footer.configure(text="支持 Weixin / WeChat 各版本，无需手动填写路径")

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
        self._launch_btn.configure(state="normal", text="启  动  微  信")
        if ok:
            self._footer.configure(text=f"已成功启动 {detail} 个微信窗口")
        else:
            messagebox.showerror("启动失败", str(detail))
            self._footer.configure(text="启动失败，请重试或重新检测微信路径")


def run() -> None:
    app = WexOpenApp()
    app.mainloop()
