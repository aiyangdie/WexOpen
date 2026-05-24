"""关于对话框。"""

from __future__ import annotations

import webbrowser

import customtkinter as ctk

from wexopen import __version__
from wexopen.meta import AUTHOR, AUTHOR_EMAIL, DISCLAIMER, GITHUB_URL, LICENSE

GREEN = "#07C160"
GREEN_BG = "#E8F8EF"
BG = "#F4F5F7"
WHITE = "#FFFFFF"
TEXT = "#1A1A1A"
SUB = "#666666"
MUTED = "#999999"
BORDER = "#E8E8E8"
FONT = "Microsoft YaHei UI"


class AboutDialog(ctk.CTkToplevel):
    WIDTH = 340
    HEIGHT = 420

    def __init__(self, parent: ctk.CTk, *, business: bool = False) -> None:
        super().__init__(parent)
        self.title("关于 WexOpen")
        self.configure(fg_color=BG)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        variant = "商业版" if business else "纯净版"
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        pad = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        pad.pack(fill="both", expand=True, padx=24, pady=24)

        logo = ctk.CTkFrame(pad, width=64, height=64, corner_radius=16, fg_color=GREEN)
        logo.pack(pady=(0, 12))
        logo.pack_propagate(False)
        ctk.CTkLabel(
            logo, text="W",
            font=ctk.CTkFont(family=FONT, size=28, weight="bold"),
            text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            pad, text="WexOpen",
            font=ctk.CTkFont(family=FONT, size=20, weight="bold"),
            text_color=TEXT,
        ).pack()

        ctk.CTkLabel(
            pad, text=f"版本 {__version__} · {variant}",
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=MUTED,
        ).pack(pady=(4, 16))

        info = ctk.CTkFrame(pad, fg_color=WHITE, corner_radius=12, border_width=1, border_color=BORDER)
        info.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            info,
            text=DISCLAIMER,
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=SUB,
            wraplength=260,
            justify="left",
        ).pack(padx=16, pady=(14, 10), anchor="w")

        ctk.CTkLabel(
            info,
            text=f"开发者：{AUTHOR}",
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=TEXT,
            anchor="w",
        ).pack(padx=16, pady=(0, 6), anchor="w")

        ctk.CTkLabel(
            info,
            text=f"联系邮箱：{AUTHOR_EMAIL}",
            font=ctk.CTkFont(family=FONT, size=12),
            text_color=TEXT,
            anchor="w",
        ).pack(padx=16, pady=(0, 6), anchor="w")

        ctk.CTkLabel(
            info,
            text=f"开源协议：{LICENSE}",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=MUTED,
            anchor="w",
        ).pack(padx=16, pady=(0, 14), anchor="w")

        ctk.CTkButton(
            pad,
            text="访问 GitHub 开源仓库",
            height=40,
            corner_radius=10,
            fg_color=GREEN,
            hover_color="#06AD56",
            text_color="white",
            font=ctk.CTkFont(family=FONT, size=13, weight="bold"),
            command=lambda: webbrowser.open(GITHUB_URL),
        ).pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            pad,
            text="关闭",
            height=36,
            corner_radius=10,
            fg_color=WHITE,
            hover_color=GREEN_BG,
            text_color=SUB,
            border_width=1,
            border_color=BORDER,
            font=ctk.CTkFont(family=FONT, size=12),
            command=self.destroy,
        ).pack(fill="x")

        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() - self.WIDTH) // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.HEIGHT) // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{px}+{py}")
