#!/usr/bin/env python3
"""Assemble entry.png: a one-page newspaper front page summing up
Wednesday 18 November 2026 in six illustrated stories.

Layout (1024x1024): a dark masthead band, a 2x3 grid of story panels
(illustration on top, kicker + headline caption below), and a dark
footer strip with the day's other headlines.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
HEADER_H = 120
FOOTER_H = 56
MARGIN = 16
GUTTER = 12

PAPER = (247, 243, 234)      # warm newsprint
INK = (24, 28, 36)          # near-black
HEADER_BG = (26, 35, 50)    # deep navy
HEADER_FG = (247, 243, 234)
KICKER_RED = (185, 28, 28)
ACCENT_GOLD = (198, 160, 72)    # thin rule under the masthead
PANEL_BG = (255, 255, 255)
RULE = (180, 175, 162)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_SUB = font("DejaVuSans.ttf", 17)
F_KICKER = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSans-Bold.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 15)

PANELS = [
    ("media-generation-panel-quad-0-dc021daf-8b96-4872-a96f-768fed29403f.webp",
     "DIPLOMACY \u00b7 MANILA",
     "Trump joins Quad leaders in Manila; bloc unveils new maritime exercise"),
    ("media-generation-panel-bahrain-0-292d340d-cec9-4829-b288-d251c4644c45.webp",
     "MIDDLE EAST \u00b7 BAHRAIN",
     "Iran says it hit a US radar site in Bahrain with drones"),
    ("media-generation-panel-bridge-0-bdbb07bf-cddf-4c0a-bf56-a6ca080c3102.webp",
     "WAR IN UKRAINE",
     "Ukraine damages the Crimean bridge as Russia hits Kyiv bridges"),
    ("media-generation-panel-nvidia-0-99070e84-a637-4a4c-ab4f-45aea5e69e17.webp",
     "TECH \u00b7 EARNINGS",
     "Nvidia beats forecasts in first results without Jensen Huang"),
    ("media-generation-panel-siberia-0-9655605a-e477-432e-93cc-fcc81f1e5264.webp",
     "RUSSIA \u00b7 SIBERIA",
     "Military plane crashes in Siberia; 19 killed"),
    ("media-generation-panel-measles-0-375c979e-eef2-4884-b221-715bc5265a5b.webp",
     "HEALTH \u00b7 USA",
     "US loses measles-free status as cases mount"),
]

FOOTER = ("ALSO: Dhoni retires from the IPL \u00b7 Mongolia's president resigns "
          "amid graft charges \u00b7 Japan protests Russian airspace violation "
          "\u00b7 Britain sanctions Israeli settlement firms")


def crop_fill(img, tw, th):
    """Centre-crop img to exactly tw x th (cover fit)."""
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    nw, nh = int(iw * scale + 0.5), int(ih * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Header band -------------------------------------------------
    d.rectangle([0, 0, W, HEADER_H], fill=HEADER_BG)
    d.text((W / 2, 12), "THE WORLD IN ONE IMAGE", font=F_MASTHEAD,
           fill=HEADER_FG, anchor="ma")
    d.text((W / 2, 66), "Wednesday 18 November 2026", font=F_DATE,
           fill=HEADER_FG, anchor="ma")
    d.text((W / 2, 94), "Six stories that defined the day", font=F_SUB,
           fill=(200, 205, 215), anchor="ma")
    d.rectangle([0, HEADER_H - 3, W, HEADER_H - 1], fill=ACCENT_GOLD)

    # ---- Grid --------------------------------------------------------
    grid_top = HEADER_H + 8
    grid_bottom = H - FOOTER_H - 8
    grid_h = grid_bottom - grid_top
    panel_w = (W - 2 * MARGIN - GUTTER) // 2
    panel_h = (grid_h - 2 * GUTTER) // 3
    caption_h = 72

    for i, (fname, kicker, headline) in enumerate(PANELS):
        row, col = divmod(i, 2)
        x = MARGIN + col * (panel_w + GUTTER)
        y = grid_top + row * (panel_h + GUTTER)

        # panel card
        d.rectangle([x, y, x + panel_w - 1, y + panel_h - 1], fill=PANEL_BG,
                    outline=RULE, width=1)

        # illustration, cropped to fill the top of the panel
        img = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
        img = crop_fill(img, panel_w - 2, panel_h - caption_h - 2)
        page.paste(img, (x + 1, y + 1))

        # caption band
        cap_y = y + panel_h - caption_h
        d.line([x + 1, cap_y, x + panel_w - 2, cap_y], fill=RULE, width=1)
        tx = x + 10
        tw = panel_w - 20
        d.text((tx, cap_y + 6), kicker, font=F_KICKER, fill=KICKER_RED)
        lines = wrap(d, headline, F_HEAD, tw)
        ly = cap_y + 26
        for line in lines[:2]:
            d.text((tx, ly), line, font=F_HEAD, fill=INK)
            ly += 22

    # ---- Footer strip ------------------------------------------------
    fy = H - FOOTER_H
    d.rectangle([0, fy, W, H], fill=HEADER_BG)
    lines = wrap(d, FOOTER, F_FOOT, W - 2 * MARGIN)
    ly = fy + 8
    for line in lines[:2]:
        d.text((W / 2, ly), line, font=F_FOOT, fill=HEADER_FG, anchor="ma")
        ly += 20

    page.save(OUT, format="JPEG", quality=88)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
