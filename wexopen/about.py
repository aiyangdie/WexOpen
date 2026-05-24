"""关于对话框 — 与主界面统一风格。"""

from __future__ import annotations

import webbrowser

import customtkinter as ctk

from wexopen import __version__
from wexopen.meta import AUTHOR, AUTHOR_EMAIL, DISCLAIMER, GITHUB_URL, LICENSE
from wexopen.theme import C, font, primary_btn, ghost_btn


class AboutDialog(ctk.CTkToplevel):
    WIDTH = 320
    HEIGHT = 400

    def __init__(self, parent: ctk.CTk, *, business: bool = False) -> None:
        super().__init__(parent)
        self.title("关于")
        self.configure(fg_color=C["bg"])
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        variant = "商业版" if business else "纯净版"
        pad = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        pad.pack(fill="both", expand=True, padx=24, pady=24)

        mark = ctk.CTkFrame(pad, width=56, height=56, corner_radius=14, fg_color=C["green"])
        mark.pack(pady=(0, 12))
        mark.pack_propagate(False)
        ctk.CTkLabel(mark, text="W", font=font(24, "bold"), text_color="white").place(
            relx=0.5, rely=0.5, anchor="center",
        )

        ctk.CTkLabel(pad, text="WexOpen", font=font(18, "bold"), text_color=C["text"]).pack()
        ctk.CTkLabel(pad, text=f"v{__version__} · {variant}", font=font(11), text_color=C["text3"]).pack(pady=(4, 16))

        box = ctk.CTkFrame(pad, fg_color=C["surface"], corner_radius=12)
        box.pack(fill="x", pady=(0, 16))

        texts = [DISCLAIMER, f"开发者 {AUTHOR}", f"邮箱 {AUTHOR_EMAIL}", LICENSE]
        for i, line in enumerate(texts):
            ctk.CTkLabel(
                box, text=line, font=font(11),
                text_color=C["text2"] if i == 0 else C["text"],
                wraplength=240, justify="left", anchor="w",
            ).pack(anchor="w", padx=14, pady=(14 if i == 0 else 6, 14 if i == len(texts) - 1 else 0))

        primary_btn(pad, "GitHub 开源", lambda: webbrowser.open(GITHUB_URL)).pack(fill="x", pady=(0, 8))
        ghost_btn(pad, "关闭", self.destroy, width=80).pack()

        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width() - self.WIDTH) // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.HEIGHT) // 2
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}+{px}+{py}")
