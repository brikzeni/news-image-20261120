#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one newspaper-style front page that
sums up world news of Friday 20 November 2026.

Every fact in the image was verified against at least two credible news
sources on 20 Nov 2026; see RESEARCH.md in the campaign workspace for the
source list and URLs. Run: python3 draw.py  ->  writes entry.png (1024x1024,
under 1 MiB). Rendering uses Pillow + DejaVu fonts, both present in the VM.
The submitted program (main.py) only copies this PNG to the output dir, so
the graded run is byte-identical every time.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (22, 21, 19)           # near-black
RED = (178, 34, 30)          # masthead / kicker red
BLUE = (31, 78, 121)         # deep blue accent
SKY = (214, 228, 240)        # pale sky for illustration panels
GREY = (90, 86, 80)          # secondary text
LINE = (180, 172, 158)       # hairlines

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, spacing=2):
    """Draw text with extra letter tracking (for kickers)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def kicker(draw, x, y, text, size=17):
    f = font(SANS_B, size)
    tracked(draw, (x, y), text.upper(), f, RED, spacing=2)
    return y + size + 6


def headline(draw, x, y, text, size, max_w, leading=None):
    """Serif-bold headline, wrapped; returns y after last line."""
    f = font(SERIF_B, size)
    leading = leading or int(size * 1.12)
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=INK)
        y += leading
    return y


def deck(draw, x, y, text, size, max_w, leading=None, fill=INK):
    """Sans deck/summary, wrapped; returns y after last line."""
    f = font(SANS, size)
    leading = leading or int(size * 1.32)
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, fill=(255, 255, 255)):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4,
                           fill=fill, outline=LINE, width=1)


# ---------------------------------------------------------------- illustrations
# All flat vector-style drawings, no photos, no external assets.

def draw_summit(d, x, y, w, h):
    """Three flags (US, China, Russia) over a summit table, pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # big soft sun/globe disc behind the flags
    cx, cy, r = x + w // 2, y + h - 58, 118
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(233, 214, 178))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 170, 120), width=2)
    # table
    d.rectangle([x + 30, y + h - 46, x + w - 30, y + h - 30], fill=(122, 72, 40))
    d.rectangle([x + 44, y + h - 30, x + w - 44, y + h - 22], fill=(96, 56, 30))
    # three flag poles with flags, left to right: US, China, Russia
    pole_h = h - 120
    tops = [x + 92, x + w // 2, x + w - 92]
    flags = ["us", "cn", "ru"]
    for px, kind in zip(tops, flags):
        d.line([(px, y + 34), (px, y + 34 + pole_h)], fill=(70, 60, 50), width=5)
        d.ellipse([px - 5, y + 28, px + 5, y + 38], fill=(212, 175, 55))
        fw, fh = 74, 46
        fx, fy = px + 4, y + 36
        if kind == "us":
            for i in range(7):
                col = (178, 34, 30) if i % 2 == 0 else (255, 255, 255)
                d.rectangle([fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7],
                            fill=col)
            d.rectangle([fx, fy, fx + 30, fy + 24], fill=(31, 60, 120))
            for sx in (8, 19):
                for sy in (6, 15):
                    d.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2, fy + sy + 2],
                              fill=(255, 255, 255))
        elif kind == "cn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            d.ellipse([fx + 12, fy + 8, fx + 24, fy + 20], fill=(255, 222, 0))
            for sx, sy in ((34, 8), (42, 14), (42, 24), (34, 30)):
                d.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                          fill=(255, 222, 0))
        else:
            for i, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 0))):
                d.rectangle([fx, fy + i * fh // 3, fx + fw, fy + (i + 1) * fh // 3],
                            fill=col)
            d.rectangle([fx, fy, fx + fw, fy + fh], outline=(120, 120, 120), width=1)


def draw_court(d, x, y, w, h):
    """Courthouse facade with columns + scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    # pediment
    d.polygon([(x + 12, y + 52), (x + w - 12, y + 52), (x + w // 2, y + 16)],
              fill=(178, 34, 30))
    d.ellipse([x + w // 2 - 9, y + 26, x + w // 2 + 9, y + 44], fill=(247, 243, 234))
    # columns
    for i in range(4):
        cx0 = x + 22 + i * (w - 44) // 3 - 7
        d.rectangle([cx0, y + 56, cx0 + 14, y + h - 26], fill=(255, 255, 255),
                    outline=(150, 142, 128), width=1)
    # base + steps
    d.rectangle([x + 12, y + h - 26, x + w - 12, y + h - 18], fill=(90, 86, 80))
    d.rectangle([x + 6, y + h - 18, x + w - 6, y + h - 10], fill=(120, 114, 104))
    # scales, small, centred above pediment line
    sx, sy = x + w // 2, y + 6
    d.line([(sx, sy), (sx, sy + 8)], fill=INK, width=2)


def draw_bridge(d, x, y, w, h):
    """Dnipro bridge at night: skyline, river, bridge, two blasts."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 66))
    # skyline silhouettes
    for bx, bw, bh in ((8, 26, 34), (42, 18, 48), (66, 30, 28), (104, 20, 42)):
        d.rectangle([x + bx, y + h - 62 - bh, x + bx + bw, y + h - 62],
                    fill=(24, 32, 46))
    # river
    d.rectangle([x, y + h - 62, x + w, y + h], fill=(52, 96, 140))
    d.line([(x, y + h - 62), (x + w, y + h - 62)], fill=(120, 170, 210), width=2)
    # bridge deck + arch + pillars
    d.line([(x + 6, y + h - 78), (x + w - 6, y + h - 78)], fill=(220, 220, 220),
           width=5)
    d.arc([x + 18, y + h - 128, x + w - 18, y + h - 40], start=180, end=360,
          fill=(220, 220, 220), width=4)
    for px in (x + 34, x + w // 2 - 2, x + w - 38):
        d.line([(px, y + h - 78), (px, y + h - 62)], fill=(220, 220, 220), width=4)
    # explosion starbursts on the deck
    for ex, ey, r in ((x + 52, y + h - 96, 17), (x + w - 48, y + h - 100, 14)):
        for ang in range(0, 360, 30):
            import math
            a = math.radians(ang)
            d.line([(ex, ey), (ex + r * math.cos(a), ey + r * math.sin(a))],
                   fill=(255, 176, 32), width=3)
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 110, 20))


def draw_tower(d, x, y, w, h):
    """Riyadh PIF Tower: tall slab with broken windows on upper floors."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 214, 198))
    tw, th = 64, h - 26
    tx, ty = x + w // 2 - tw // 2, y + 14
    d.rectangle([tx, ty, tx + tw, ty + th], fill=(44, 62, 92))
    # window grid
    for r in range(9):
        for c in range(4):
            wx = tx + 8 + c * 14
            wy = ty + 10 + r * 13
            broken = r in (1, 2, 3) and c in (1, 2)
            col = (255, 150, 40) if broken else (140, 175, 210)
            d.rectangle([wx, wy, wx + 9, wy + 8], fill=col)
    # crown
    d.polygon([(tx, ty), (tx + tw, ty), (tx + tw // 2, ty - 10)], fill=(30, 44, 68))
    # shorter neighbours
    d.rectangle([x + 10, y + h - 66, x + 34, y + h - 12], fill=(90, 104, 128))
    d.rectangle([x + w - 34, y + h - 80, x + w - 10, y + h - 12], fill=(70, 86, 110))
    # smoke wisp from the broken floors
    d.ellipse([tx + tw - 6, ty + 22, tx + tw + 16, ty + 40], fill=(150, 150, 150))
    d.ellipse([tx + tw + 2, ty + 8, tx + tw + 22, ty + 26], fill=(170, 170, 170))


def draw_chart(d, x, y, w, h):
    """Falling market line + ANT +17% green chip vs NIKKEI -4.8% red chip."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 236))
    # axes
    d.line([(x + 12, y + h - 30), (x + w - 10, y + h - 30)], fill=GREY, width=2)
    d.line([(x + 12, y + 12), (x + 12, y + h - 30)], fill=GREY, width=2)
    # falling line
    pts = [(x + 16, y + 26), (x + 44, y + 40), (x + 70, y + 34),
           (x + 96, y + 62), (x + 122, y + 78), (x + 146, y + 96)]
    d.line(pts, fill=(178, 34, 30), width=4, joint="curve")
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 12, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] - 12)], fill=(178, 34, 30))
    # chips: ANT green chip bottom-left, Nikkei red label top-right
    f = font(SANS_B, 14)
    chip_txt = "ANT +17%"
    cw = int(d.textlength(chip_txt, font=f)) + 14
    d.rounded_rectangle([x + 12, y + h - 26, x + 12 + cw, y + h - 4], radius=3,
                        fill=(27, 120, 60))
    d.text((x + 19, y + h - 23), chip_txt, font=f, fill=(255, 255, 255))
    f2 = font(SANS_B, 14)
    nk = "NIKKEI -4.8%"
    d.text((x + w - 10 - d.textlength(nk, font=f2), y + 8), nk, font=f2,
           fill=(178, 34, 30))


def draw_globe(d, x, y, w, h):
    """Small globe with a leaf: COP31."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 226))
    cx, cy, r = x + w // 2 - 8, y + h // 2 + 4, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(74, 144, 190))
    d.ellipse([cx - 20, cy - 26, cx + 2, cy - 2], fill=(86, 160, 90))
    d.ellipse([cx - 6, cy + 4, cx + 22, cy + 26], fill=(86, 160, 90))
    d.ellipse([cx - 30, cy + 8, cx - 12, cy + 22], fill=(86, 160, 90))
    # leaf sprout
    d.line([(cx + 26, cy - 30), (cx + 40, cy - 44)], fill=(46, 110, 50), width=3)
    d.ellipse([cx + 30, cy - 52, cx + 52, cy - 34], fill=(86, 160, 90))


# ---------------------------------------------------------------- page layout
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28                      # outer margin
    CW = W - 2 * M              # content width

    # ---- masthead ------------------------------------------------------
    y = 26
    tracked(d, (M, y), "THE WORLD IN ONE DAY", font(SANS_B, 18), RED, spacing=4)
    y += 30
    title = "FRIDAY  20 NOVEMBER 2026"
    tf = font(SERIF_B, 58)
    d.text((M, y), title, font=tf, fill=INK)
    y += 76
    rule(d, M, y, W - M, w=3)
    rule(d, M, y + 6, W - M, w=1)
    y += 16

    # ---- lead: Shenzhen summit ----------------------------------------
    lead_y, lead_h = y, 268
    panel(d, M, lead_y, CW, lead_h)
    ix, iy, iw, ih = M + 12, lead_y + 12, 430, lead_h - 24
    draw_summit(d, ix, iy, iw, ih)
    tx = M + 12 + iw + 20
    tw = W - M - tx
    ty = lead_y + 18
    ty = kicker(d, tx, ty, "SHENZHEN, CHINA  ·  THE SUMMIT", size=16)
    ty = headline(d, tx, ty, "TRUMP, XI AND PUTIN MEET FACE TO FACE",
                  34, tw, leading=40)
    ty += 8
    ty = deck(d, tx, ty,
              "First three-way summit of the US, Chinese and Russian leaders "
              "ends in a four-point \u201cpeace declaration\u201d: nuclear war "
              "\u201cmust never be fought\u201d.",
              20, tw, leading=27)
    ty += 6
    deck(d, tx, ty,
         "No deal on Ukraine or Iran. No arms-control talks agreed.",
         20, tw, leading=27, fill=GREY)

    # ---- grid 2x2 ------------------------------------------------------
    gy = lead_y + lead_h + 16
    gw, gh, gap = (CW - 16) // 2, 196, 16
    stories = [
        ("THE HAGUE  ·  JUSTICE", "WORLD COURT: MYANMAR GUILTY OF GENOCIDE",
         "ICJ: Myanmar committed genocide against the Rohingya in 2017 — a "
         "first for any state. Myanmar calls it \u201cunfair\u201d.",
         draw_court),
        ("KYIV  ·  THE WAR", "MISSILES HIT KYIV\u2019S BRIDGES",
         "Overnight barrage of 400+ drones and 110 missiles kills 8 and "
         "strikes three Dnipro bridges. Russian objects also violate "
         "Polish airspace.", draw_bridge),
        ("RIYADH  ·  THE GULF", "MISSILE HITS RIYADH\u2019S TALLEST TOWER",
         "A Houthi strike damages 7–8 floors of the PIF Tower, HQ of the "
         "Saudi wealth fund. No injuries reported.", draw_tower),
        ("MARKETS  ·  THE ECONOMY", "AI SELL-OFF DEEPENS",
         "Anthropic\u2019s record IPO closes +17% at $97.17 — but the Nikkei "
         "falls 4.8% and the S&P 500 logs a fifth straight loss.",
         draw_chart),
    ]
    for i, (kick, head, body, art) in enumerate(stories):
        gx = M + (i % 2) * (gw + gap)
        gyy = gy + (i // 2) * (gh + gap)
        panel(d, gx, gyy, gw, gh)
        art(d, gx + 10, gyy + 10, 158, gh - 20)
        tx2 = gx + 180
        tw2 = gx + gw - 12 - tx2
        ty2 = gyy + 12
        ty2 = kicker(d, tx2, ty2, kick, size=13)
        ty2 = headline(d, tx2, ty2, head, 21, tw2, leading=25)
        ty2 += 4
        deck(d, tx2, ty2, body, 15, tw2, leading=20)

    # ---- COP31 wide strip ----------------------------------------------
    cy = gy + 2 * gh + gap + 16
    ch = 104
    panel(d, M, cy, CW, ch)
    draw_globe(d, M + 12, cy + 10, 96, ch - 20)
    tx3 = M + 124
    tw3 = W - M - 12 - tx3
    ty3 = cy + 12
    ty3 = kicker(d, tx3, ty3, "ANTALYA, TURKEY  ·  CLIMATE", size=13)
    ty3 = headline(d, tx3, ty3, "COP31 DRAFT DROPS FOSSIL FUELS", 24, tw3,
                   leading=28)
    deck(d, tx3, ty3 + 2,
         "The new draft text strips every mention of ending fossil-fuel use — "
         "and admits 1.5\u00b0C will be overshot.", 16, tw3, leading=21)

    # ---- footer ticker --------------------------------------------------
    fy = cy + ch + 14
    rule(d, M, fy, W - M, w=1, fill=LINE)
    f_tick = font(SANS_B, 14)
    tick = ("SENATE PASSES ENERGY BILL 62–33   ·   WHITE HOUSE CYBER CHIEF "
            "OUT   ·   IRAQ MOVES ON MILITIA STRONGHOLD")
    d.text((M, fy + 10), tick, font=f_tick, fill=INK)
    f_src = font(SANS, 12)
    src = "Sources: Reuters · WSJ · The Times · UN News · CNN"
    d.text((W - M - d.textlength(src, font=f_src), fy + 34), src,
           font=f_src, fill=GREY)
    return img


if __name__ == "__main__":
    out = build()
    out.save("entry.png", optimize=True)
    import os
    print("wrote entry.png", os.path.getsize("entry.png"), "bytes",
          out.size)
