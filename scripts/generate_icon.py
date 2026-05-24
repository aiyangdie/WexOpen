"""生成 WexOpen 应用图标。"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "icon.ico"
SIZE = 256


def _draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = size * 0.08
    r = size * 0.22
    draw.rounded_rectangle(
        (pad, pad, size - pad, size - pad),
        radius=r,
        fill="#07C160",
    )
    inner = size * 0.28
    bubble = size * 0.19
    draw.ellipse(
        (inner, inner * 1.05, inner + bubble, inner + bubble * 1.15),
        fill="white",
    )
    draw.ellipse(
        (size * 0.52, inner * 0.95, size * 0.52 + bubble, inner * 0.95 + bubble * 1.15),
        fill="white",
    )
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", int(size * 0.24))
    except OSError:
        try:
            font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", int(size * 0.24))
        except OSError:
            font = ImageFont.load_default()
    draw.text((size * 0.36, size * 0.58), "W", fill="white", font=font)
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base = _draw_icon(SIZE)
    base.save(
        OUT,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    png = OUT.with_suffix(".png")
    base.save(png, format="PNG")
    print(f"Icon saved: {OUT}")


if __name__ == "__main__":
    main()
