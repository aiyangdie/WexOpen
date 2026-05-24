"""WexOpen 设计系统 — 颜色、字体、尺寸。"""

from __future__ import annotations

import customtkinter as ctk

# 色彩
C = {
    "green": "#07C160",
    "green_hover": "#06AD56",
    "green_soft": "#E8F8EF",
    "green_muted": "#B8E6C8",
    "bg": "#FFFFFF",
    "surface": "#F7F8FA",
    "text": "#111111",
    "text2": "#5C5C5C",
    "text3": "#A8A8A8",
    "line": "#EEEEEE",
    "red": "#FA5151",
    "red_soft": "#FFF5F5",
    "amber": "#C9A227",
    "amber_soft": "#FFFBF0",
    "amber_line": "#F5E6C4",
}

FONT = "Microsoft YaHei UI"

# 尺寸
WIN_W = 360
WIN_H_PURE = 500
WIN_H_BIZ = 580
RADIUS = 12
RADIUS_LG = 16


def font(size: int, weight: str = "normal") -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT, size=size, weight=weight)


def ghost_btn(parent, text: str, command, **kw) -> ctk.CTkButton:
    """文字链接风格按钮。"""
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=28,
        corner_radius=6,
        fg_color="transparent",
        hover_color=C["surface"],
        text_color=C["text3"],
        font=font(12),
        **kw,
    )


def primary_btn(parent, text: str, command, **kw) -> ctk.CTkButton:
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        height=50,
        corner_radius=RADIUS,
        fg_color=C["green"],
        hover_color=C["green_hover"],
        text_color="white",
        font=font(16, "bold"),
        **kw,
    )
