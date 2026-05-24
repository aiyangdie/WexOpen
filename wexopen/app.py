"""WexOpen 主界面 — 纯净版 / 商业版。"""

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
from wexopen.meta import AUTHOR, AUTHOR_EMAIL, DISCLAIMER, GITHUB_URL

# ── 配色 ──
GREEN = "#07C160"
GREEN_HOVER = "#06AD56"
GREEN_BG = "#E8F8EF"
BG = "#F4F5F7"
WHITE = "#FFFFFF"
TEXT = "#1A1A1A"
SUB = "#666666"
MUTED = "#999999"
BORDER = "#E8E8E8"
RED = "#FA5151"
RED_BG = "#FFF0F0"
GOLD = "#D4A017"
GOLD_BG = "#FFF8E7"
GOLD_BORDER = "#F0D78C"

FONT = "Microsoft YaHei UI"


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


class WexOpenApp(ctk.CTk):
    WIDTH = 380
    HEIGHT_PURE = 580
    HEIGHT_BUSINESS = 660

    def __init__(self, *, business: bool = False) -> None:
        _enable_win_dpi()
        super().__init__()

        self._business = business
        self._location: WeChatLocation | None = None
        self._busy = False
        self._fonts: dict[str, ctk.CTkFont] = {}
        self._footer_default = ""

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)

        suffix = "商业版" if business else "纯净版"
        self.title(f"WexOpen 微信多开 · {suffix}")
        self._height = self.HEIGHT_BUSINESS if business else self.HEIGHT_PURE
        self.geometry(f"{self.WIDTH}x{self._height}")
        self.minsize(self.WIDTH, self._height)
        self.resizable(False, False)
        self.configure(fg_color=BG)

        icon = _asset_path("icon.ico")
        if icon.is_file():
            self.iconbitmap(str(icon))

        self._register_fonts()
        self._build_ui()
        self._center_window()
        self.after(80, self._detect_wechat)

    def _register_fonts(self) -> None:
        specs: dict[str, tuple[int, str]] = {
            "logo": (22, "bold"),
            "title": (20, "bold"),
            "subtitle": (12, "normal"),
            "section": (13, "bold"),
            "body": (12, "normal"),
            "small": (11, "normal"),
            "count": (26, "bold"),
            "btn_main": (15, "bold"),
            "btn_quick": (13, "normal"),
            "btn_small": (12, "normal"),
            "btn_tiny": (11, "normal"),
            "minus": (20, "bold"),
            "biz_title": (13, "bold"),
        }
        for key, (size, weight) in specs.items():
            self._fonts[key] = ctk.CTkFont(family=FONT, size=size, weight=weight)

    def _font(self, key: str) -> ctk.CTkFont:
        return self._fonts[key]

    def _center_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.WIDTH) // 2
        y = (self.winfo_screenheight() - self._height) // 2
        self.geometry(f"{self.WIDTH}x{self._height}+{x}+{y}")

    def _card(self, parent) -> ctk.CTkFrame:
        return ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER,
        )

    def _show_about(self) -> None:
        AboutDialog(self, business=self._business)

    def _copy_contact(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(AUTHOR_EMAIL)
        self._set_footer(f"已复制邮箱：{AUTHOR_EMAIL}")

    def _set_footer(self, text: str) -> None:
        self._footer.configure(text=text)

    def _build_ui(self) -> None:
        pad = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        # ── 顶栏 ──
        header = ctk.CTkFrame(pad, fg_color=BG, corner_radius=0)
        header.pack(fill="x", pady=(0, 16))

        left = ctk.CTkFrame(header, fg_color=BG, corner_radius=0)
        left.pack(side="left", fill="x", expand=True)

        logo = ctk.CTkFrame(left, width=52, height=52, corner_radius=14, fg_color=GREEN)
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(
            logo, text="W", font=self._font("logo"), text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        title_box = ctk.CTkFrame(left, fg_color=BG, corner_radius=0)
        title_box.pack(side="left", padx=(14, 0))

        tag = "商业版" if self._business else "纯净版"
        ctk.CTkLabel(title_box, text="WexOpen", font=self._font("title"), text_color=TEXT, anchor="w").pack(anchor="w")
        ctk.CTkLabel(title_box, text=f"微信多开助手 · {tag}", font=self._font("subtitle"), text_color=SUB, anchor="w").pack(anchor="w", pady=(2, 0))
        ctk.CTkLabel(title_box, text="自动识别路径，无需配置", font=self._font("small"), text_color=MUTED, anchor="w").pack(anchor="w", pady=(2, 0))

        if self._business:
            ctk.CTkButton(
                header,
                text="关于",
                width=52,
                height=30,
                corner_radius=8,
                fg_color=WHITE,
                hover_color=GREEN_BG,
                text_color=SUB,
                border_width=1,
                border_color=BORDER,
                font=self._font("btn_tiny"),
                command=self._show_about,
            ).pack(side="right", padx=(8, 0))

        # ── 微信状态 ──
        status = self._card(pad)
        status.pack(fill="x", pady=(0, 12))

        status_top = ctk.CTkFrame(status, fg_color="transparent")
        status_top.pack(fill="x", padx=16, pady=(14, 8))

        self._status_dot = ctk.CTkLabel(status_top, text="●", font=self._font("small"), text_color=MUTED, width=16)
        self._status_dot.pack(side="left")

        self._status_label = ctk.CTkLabel(
            status_top, text="正在检测微信...", font=self._font("section"), text_color=TEXT, anchor="w",
        )
        self._status_label.pack(side="left", fill="x", expand=True)

        self._path_label = ctk.CTkLabel(
            status, text="", font=self._font("small"), text_color=MUTED,
            anchor="w", justify="left", wraplength=300,
        )
        self._path_label.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkButton(
            status, text="重新检测", height=32, width=96, corner_radius=8,
            fg_color=GREEN_BG, hover_color="#D4F3E3", text_color=GREEN,
            font=self._font("btn_small"), command=self._detect_wechat,
        ).pack(pady=(0, 14))

        # ── 数量 ──
        count_card = self._card(pad)
        count_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(count_card, text="打开数量", font=self._font("section"), text_color=TEXT).pack(anchor="w", padx=16, pady=(14, 12))

        stepper = ctk.CTkFrame(count_card, fg_color="transparent")
        stepper.pack()
        self._count_var = tk.StringVar(value="2")

        ctk.CTkButton(
            stepper, text="-", width=46, height=46, corner_radius=10,
            fg_color=BG, hover_color=BORDER, text_color=TEXT,
            font=self._font("minus"), command=lambda: self._adjust_count(-1),
        ).pack(side="left")

        self._count_entry = ctk.CTkEntry(
            stepper, width=64, height=46, corner_radius=10,
            border_width=1, border_color=BORDER, fg_color=WHITE, text_color=TEXT,
            font=self._font("count"), justify="center", textvariable=self._count_var,
        )
        self._count_entry.pack(side="left", padx=12)
        self._count_entry.bind("<KeyRelease>", self._on_count_input)

        ctk.CTkButton(
            stepper, text="+", width=46, height=46, corner_radius=10,
            fg_color=BG, hover_color=BORDER, text_color=TEXT,
            font=self._font("minus"), command=lambda: self._adjust_count(1),
        ).pack(side="left")

        ctk.CTkLabel(
            count_card, text=f"支持 {MIN_INSTANCES} - {MAX_INSTANCES} 个窗口",
            font=self._font("small"), text_color=MUTED,
        ).pack(pady=(10, 14))

        # ── 快捷 ──
        quick = ctk.CTkFrame(pad, fg_color=BG, corner_radius=0)
        quick.pack(fill="x", pady=(0, 12))
        for i, (n, label) in enumerate(((2, "双开"), (3, "三开"), (4, "四开"), (5, "五开"))):
            ctk.CTkButton(
                quick, text=label, height=36, corner_radius=8,
                fg_color=WHITE, hover_color=GREEN_BG, text_color=GREEN,
                border_width=1, border_color=BORDER, font=self._font("btn_quick"),
                command=lambda c=n: self._set_count_and_launch(c),
            ).pack(side="left", expand=True, fill="x", padx=(0 if i == 0 else 6, 0))

        # ── 商业版：合作广告位 ──
        if self._business:
            self._build_business_card(pad)

        # ── 启动 ──
        self._launch_btn = ctk.CTkButton(
            pad, text="启动微信", height=48, corner_radius=10,
            fg_color=GREEN, hover_color=GREEN_HOVER, text_color="white",
            font=self._font("btn_main"), command=self._on_launch,
        )
        self._launch_btn.pack(fill="x", pady=(4, 0))

        # ── 底部信息 ──
        bottom = ctk.CTkFrame(pad, fg_color=BG, corner_radius=0)
        bottom.pack(fill="x", pady=(10, 0))

        self._footer = ctk.CTkLabel(
            bottom, text="", font=self._font("small"), text_color=MUTED,
        )
        self._footer.pack()

        if self._business:
            link_row = ctk.CTkFrame(bottom, fg_color=BG, corner_radius=0)
            link_row.pack(pady=(4, 0))

            ctk.CTkButton(
                link_row, text="仅供参考学习", width=88, height=24, corner_radius=6,
                fg_color=BG, hover_color=BORDER, text_color=MUTED,
                font=self._font("btn_tiny"), command=self._show_about,
            ).pack(side="left")

            ctk.CTkLabel(link_row, text=f"  ·  {AUTHOR}  ·  ", font=self._font("btn_tiny"), text_color=MUTED).pack(side="left")

            ctk.CTkButton(
                link_row, text="开源链接", width=72, height=24, corner_radius=6,
                fg_color=BG, hover_color=GREEN_BG, text_color=GREEN,
                font=self._font("btn_tiny"), command=lambda: webbrowser.open(GITHUB_URL),
            ).pack(side="left")

        self._footer_default = f"版本 {__version__}"
        self._set_footer(self._footer_default)

    def _build_business_card(self, parent) -> None:
        card = ctk.CTkFrame(
            parent, fg_color=GOLD_BG, corner_radius=14,
            border_width=1, border_color=GOLD_BORDER,
        )
        card.pack(fill="x", pady=(0, 12))

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(14, 6))

        ctk.CTkLabel(
            top, text="商务合作", font=self._font("biz_title"), text_color=GOLD,
        ).pack(side="left")

        ctk.CTkLabel(
            top, text="广告位", font=self._font("btn_tiny"), text_color=GOLD,
            fg_color=WHITE, corner_radius=6, width=48, height=22,
        ).pack(side="right")

        ctk.CTkLabel(
            card,
            text="本版本接受广告投放 · 有合作意向欢迎联系",
            font=self._font("body"),
            text_color=TEXT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 4))

        ctk.CTkLabel(
            card,
            text=f"联系邮箱：{AUTHOR_EMAIL}",
            font=self._font("small"),
            text_color=SUB,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 10))

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        ctk.CTkButton(
            btn_row, text="复制联系方式", height=32, corner_radius=8,
            fg_color=WHITE, hover_color=GOLD_BORDER, text_color=GOLD,
            border_width=1, border_color=GOLD_BORDER, font=self._font("btn_small"),
            command=self._copy_contact,
        ).pack(side="left", expand=True, fill="x", padx=(0, 6))

        ctk.CTkButton(
            btn_row, text="GitHub 联系", height=32, corner_radius=8,
            fg_color=GOLD, hover_color="#B8890F", text_color="white",
            font=self._font("btn_small"),
            command=lambda: webbrowser.open(GITHUB_URL),
        ).pack(side="left", expand=True, fill="x")

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
            self._count_entry.configure(border_color=RED)
        else:
            self._count_entry.configure(border_color=BORDER)

    def _adjust_count(self, delta: int) -> None:
        current = self._parse_count() or MIN_INSTANCES
        self._count_var.set(str(max(MIN_INSTANCES, min(MAX_INSTANCES, current + delta))))
        self._count_entry.configure(border_color=BORDER)

    def _set_count(self, count: int) -> None:
        self._count_var.set(str(max(MIN_INSTANCES, min(MAX_INSTANCES, count))))
        self._count_entry.configure(border_color=BORDER)

    def _set_count_and_launch(self, count: int) -> None:
        self._set_count(count)
        self._on_launch()

    def _detect_wechat(self) -> None:
        self._status_dot.configure(text_color=MUTED)
        self._status_label.configure(text="正在检测微信...")
        self._path_label.configure(text="扫描本机安装路径...")
        self._set_footer("检测中...")

        def work() -> None:
            location = find_wechat()
            self.after(0, lambda: self._apply_detection(location))

        threading.Thread(target=work, daemon=True).start()

    def _apply_detection(self, location: WeChatLocation | None) -> None:
        self._location = location
        if location:
            self._status_dot.configure(text_color=GREEN)
            self._status_label.configure(text="已找到微信")
            self._path_label.configure(text=location.display_path, text_color=SUB)
            self._launch_btn.configure(state="normal")
            self._set_footer(f"版本 {__version__}  |  点击启动或快捷多开")
        else:
            self._status_dot.configure(text_color=RED)
            self._status_label.configure(text="未检测到微信")
            self._path_label.configure(text="请先安装 PC 版微信，再点「重新检测」", text_color=SUB)
            self._launch_btn.configure(state="disabled")
            self._set_footer(f"版本 {__version__}  |  支持 Weixin / WeChat")

    def _on_launch(self) -> None:
        if self._busy:
            return
        count = self._parse_count()
        if count is None:
            messagebox.showwarning("数量无效", f"请输入 {MIN_INSTANCES} 到 {MAX_INSTANCES} 之间的整数")
            return
        if not self._location:
            messagebox.showerror("未找到微信", "请先安装 PC 版微信，然后点击「重新检测」")
            return

        self._busy = True
        self._launch_btn.configure(state="disabled", text="启动中...")
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
            self._set_footer(f"版本 {__version__}  |  已启动 {detail} 个窗口")
        else:
            messagebox.showerror("启动失败", str(detail))
            self._set_footer(f"版本 {__version__}  |  启动失败，请重试")


def run(*, business: bool = False) -> None:
    app = WexOpenApp(business=business)
    app.mainloop()
