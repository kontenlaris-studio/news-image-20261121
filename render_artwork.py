#!/usr/bin/env python3
"""Render the entry artwork for make.fun's "Sum up 21 November's world
news in one image" bounty.

Draws a 1024x1024 editorial front-page poster with PIL: a masthead, a
stylised globe, and six captioned story tiles covering the day's main
stories (Gulf flashpoint, Shenzhen summit, COP31 deadlock, Peru quake,
the AI sell-off, and GTA VI's record launch). Fully deterministic: no
randomness, no clock, no network. Output: artwork.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "artwork.png"

INK = (13, 27, 38)
PAPER = (246, 239, 221)
RED = (198, 52, 44)
ORANGE = (224, 122, 46)
GOLD = (222, 174, 76)
TEAL = (36, 128, 122)
OCEAN = (26, 84, 110)
LAND = (126, 168, 92)
GREY = (84, 96, 104)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN)
    # graticule
    for k in (-0.66, -0.33, 0.0, 0.33, 0.66):
        y = cy + k * r
        half = (r * r - (k * r) ** 2) ** 0.5
        draw.line([cx - half, y, cx + half, y], fill=(52, 116, 140), width=2)
        x = cx + k * r
        draw.line([x, cy - half, x, cy + half], fill=(52, 116, 140), width=2)
    # crude continent blobs (stylised, not a map)
    blobs = [
        [(-0.62, -0.30), (-0.30, -0.52), (-0.12, -0.30), (-0.28, -0.02), (-0.52, -0.02)],
        [(-0.34, 0.10), (-0.14, 0.06), (-0.10, 0.34), (-0.24, 0.52), (-0.34, 0.30)],
        [(0.02, -0.42), (0.30, -0.50), (0.42, -0.26), (0.24, -0.12), (0.04, -0.20)],
        [(0.10, 0.02), (0.34, -0.02), (0.40, 0.28), (0.22, 0.48), (0.08, 0.26)],
        [(0.52, 0.30), (0.74, 0.26), (0.78, 0.48), (0.58, 0.54)],
    ]
    for blob in blobs:
        pts = [(cx + dx * r, cy + dy * r) for dx, dy in blob]
        draw.polygon(pts, fill=LAND)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=6)


def flame(draw, x, y, s, color):
    draw.polygon([(x, y - s), (x + 0.45 * s, y + 0.3 * s), (x + 0.2 * s, y + s),
                  (x - 0.2 * s, y + s), (x - 0.45 * s, y + 0.3 * s)], fill=color)
    draw.polygon([(x, y - 0.2 * s), (x + 0.22 * s, y + 0.4 * s), (x, y + 0.85 * s),
                  (x - 0.22 * s, y + 0.4 * s)], fill=GOLD)


def tile(draw, x, y, w, h, accent, kicker, caption, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 252, 244),
                           outline=accent, width=3)
    draw.rounded_rectangle([x, y, x + w, y + 44], radius=14, fill=accent)
    draw.rectangle([x, y + 24, x + w, y + 44], fill=accent)
    draw.text((x + 14, y + 10), kicker, font=font(SANS_B, 24), fill=(255, 255, 255))
    icon(draw, x + 48, y + 108)
    lines = wrap(draw, caption, font(SANS_B, 21), w - 104)
    ty = y + 64
    for line in lines[:3]:
        draw.text((x + 98, ty), line, font=font(SANS_B, 21), fill=INK)
        ty += 29


def main():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)
    draw.rectangle([18, 18, W - 18, H - 18], fill=PAPER)
    draw.rectangle([18, 18, W - 18, H - 18], outline=GOLD, width=4)

    centered(draw, W // 2, 44, "THE WORLD IN A DAY", font(SERIF_B, 74), INK)
    draw.rectangle([70, 140, W - 70, 148], fill=RED)
    centered(draw, W // 2, 160, "SATURDAY · 21 NOVEMBER 2026", font(SANS_B, 30), RED)

    draw_globe(draw, W // 2, 408, 168)

    def icon_flame(d, x, y):
        d.rectangle([x - 34, y + 8, x + 34, y + 34], fill=GREY)
        flame(d, x, y - 6, 30, RED)

    def icon_flags(d, x, y):
        d.line([x - 20, y - 30, x - 20, y + 32], fill=INK, width=5)
        d.polygon([(x - 20, y - 30), (x + 14, y - 20), (x - 20, y - 10)], fill=RED)
        d.line([x + 22, y - 30, x + 22, y + 32], fill=INK, width=5)
        d.polygon([(x + 22, y - 30), (x + 52, y - 20), (x + 22, y - 10)], fill=TEAL)

    def icon_factory(d, x, y):
        d.rectangle([x - 36, y - 2, x + 36, y + 32], fill=GREY)
        d.polygon([(x - 36, y - 2), (x - 10, y - 22), (x + 16, y - 2)], fill=GREY)
        d.rectangle([x + 18, y - 34, x + 30, y - 2], fill=GREY)
        d.ellipse([x + 12, y - 52, x + 30, y - 36], fill=(170, 170, 170))
        d.ellipse([x + 26, y - 60, x + 48, y - 42], fill=(170, 170, 170))

    def icon_quake(d, x, y):
        d.text((x - 40, y - 44), "6.9", font=font(SANS_B, 40), fill=RED)
        d.line([x - 40, y + 14, x - 14, y + 2, x + 2, y + 22, x + 20, y + 4, x + 42, y + 16],
               fill=INK, width=5)

    def icon_chart(d, x, y):
        d.rectangle([x - 14, y - 34, x + 16, y - 4], outline=TEAL, width=4)
        d.line([x - 38, y + 6, x - 12, y + 14, x + 8, y + 22, x + 38, y + 34], fill=RED, width=6)
        d.polygon([(x + 38, y + 34), (x + 22, y + 32), (x + 34, y + 20)], fill=RED)

    def icon_game(d, x, y):
        d.rounded_rectangle([x - 40, y - 18, x + 40, y + 22], radius=18, fill=INK)
        d.line([x - 24, y + 2, x - 8, y + 2], fill=GOLD, width=5)
        d.line([x - 16, y - 6, x - 16, y + 10], fill=GOLD, width=5)
        d.ellipse([x + 14, y - 8, x + 24, y + 2], fill=RED)
        d.ellipse([x + 24, y + 4, x + 34, y + 14], fill=TEAL)

    tiles = [
        (RED, "GULF FLASHPOINT", "Iran hits US bases; Trump warns Tehran", icon_flame),
        (TEAL, "SHENZHEN SUMMIT", "Trump-Xi summit; 82 missiles downed", icon_flags),
        (ORANGE, "COP31 DEADLOCK", "Climate talks stall over fossil fuels", icon_factory),
        (RED, "PERU QUAKE", "Strong quake empties Peru cinemas", icon_quake),
        (TEAL, "AI SELLOFF", "Anthropic slide hits tech stocks", icon_chart),
        (ORANGE, "GTA VI", "$2.36B: biggest game launch ever", icon_game),
    ]
    tw, th, gap, x0, y0 = 302, 168, 14, 40, 612
    for i, (accent, kicker, caption, icon) in enumerate(tiles):
        tile(draw, x0 + (i % 3) * (tw + gap), y0 + (i // 3) * (th + gap),
             tw, th, accent, kicker, caption, icon)

    centered(draw, W // 2, 972, "One planet. One day. Six stories.", font(SERIF_B, 27), INK)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
