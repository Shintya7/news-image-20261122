#!/usr/bin/env python3
"""Draw entry.png for news-image-20261122: a newspaper front page summing up
Sunday 22 November 2026 world news as reported on the morning of that day.
Six story panels (3 columns x 2 rows), each with a flat drawn illustration,
a headline and one factual sub-line. No photos, no logos, no copied artwork.
Run: python3 draw.py  (writes entry.png beside this file, 1024x1024)."""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (246, 242, 233)
NAVY = (22, 38, 70)
GOLD = (230, 180, 74)
INK = (22, 22, 22)
MUTED = (92, 89, 81)
PANEL_BG = (255, 255, 255)
BORDER = (198, 190, 170)
RED = (198, 42, 42)
TEAL = (24, 120, 110)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_REG = FONT_DIR + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
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


def fit_text(draw, text, fnt_path, size, max_w, max_lines):
    """Shrink the font until the text fits in max_lines at max_w."""
    while size > 10:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(fnt_path, size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def tag_chip(draw, x, y, text, color):
    fnt = font(F_BOLD, 15)
    tw = draw.textlength(text, font=fnt)
    pad = 8
    draw.rectangle([x, y, x + tw + pad * 2, y + 22], fill=color)
    draw.text((x + pad, y + 3), text, font=fnt, fill=(255, 255, 255))


def draw_gulf(d, x, y, w, h):
    # Night sky over the Gulf: radar dish, missile streaks, tanker on fire
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 78))
    for sx, sy in [(30, 26), (90, 52), (150, 20), (230, 44), (280, 80)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    # radar dish on a base
    d.line([x + 52, y + 150, x + 52, y + 176], fill=(190, 200, 215), width=5)
    d.pieslice([x + 22, y + 108, x + 82, y + 168], start=200, end=340,
               fill=(190, 200, 215))
    d.line([x + 52, y + 138, x + 96, y + 108], fill=(230, 180, 74), width=3)
    # two missile streaks with warheads
    d.line([x + 130, y + 60, x + 230, y + 120], fill=(230, 180, 74), width=6)
    d.polygon([(x + 230, y + 120), (x + 248, y + 128), (x + 234, y + 138)],
              fill=RED)
    d.line([x + 180, y + 30, x + 268, y + 84], fill=(255, 240, 200), width=3)
    # sea
    d.rectangle([x, y + h - 52, x + w, y + h], fill=(24, 90, 120))
    # tanker: hull, deck, funnel, flames
    d.rectangle([x + 96, y + h - 44, x + 258, y + h - 14], fill=(70, 70, 74))
    d.rectangle([x + 210, y + h - 66, x + 236, y + h - 44], fill=(200, 200, 200))
    for fx, fy, fr in [(140, 132, 16), (168, 124, 20), (196, 134, 14)]:
        d.ellipse([x + fx, y + fy, x + fx + fr, y + fy + fr], fill=(240, 120, 30))
        d.ellipse([x + fx + 5, y + fy + 4, x + fx + fr - 5, y + fy + fr - 2],
                  fill=(250, 200, 60))


def draw_climate(d, x, y, w, h):
    # Pale sky, a globe, a rising thermometer, a gavel striking deadlock
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 224))
    # sun
    cx, cy = x + w - 58, y + 44
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(240, 170, 60))
    # globe
    gx, gy = x + 66, y + 46
    d.ellipse([gx - 52, gy - 52, gx + 52, gy + 52], fill=(60, 130, 180))
    d.ellipse([gx - 52, gy - 52, gx + 52, gy + 52], outline=(255, 255, 255),
              width=3)
    d.arc([gx - 52, gy - 20, gx + 52, gy + 20], start=300, end=60,
          fill=(90, 180, 110), width=10)
    d.arc([gx - 30, gy - 52, gx + 30, gy + 52], start=90, end=270,
          fill=(90, 180, 110), width=10)
    d.ellipse([gx - 12, gy - 44, gx + 14, gy - 18], fill=(90, 180, 110))
    # thermometer, mercury high
    tx = x + 210
    d.rounded_rectangle([tx, y + 34, tx + 30, y + 150], radius=14,
                        fill=(255, 255, 255), outline=RED, width=3)
    d.rectangle([tx + 8, y + 52, tx + 22, y + 146], fill=RED)
    d.ellipse([tx - 8, y + 138, tx + 38, y + 184], fill=RED)
    # gavel on its block, lower right
    d.line([x + 40, y + h - 34, x + 92, y + h - 62], fill=(100, 76, 52),
           width=5)
    d.rectangle([x + 84, y + h - 72, x + 118, y + h - 54], fill=(130, 100, 66))
    d.rectangle([x + 150, y + h - 26, x + 250, y + h - 12], fill=(130, 100, 66))


def draw_baltic(d, x, y, w, h):
    # Cold Baltic sea, a cargo ship burning, smoke, rescue helicopter
    d.rectangle([x, y, x + w, y + h], fill=(176, 200, 220))
    # clouds
    for cx, cy in [(60, 30), (180, 22), (260, 44)]:
        d.ellipse([x + cx, y + cy, x + cx + 54, y + cy + 20], fill=(255, 255, 255))
    # helicopter
    hx, hy = x + 196, y + 30
    d.ellipse([hx, hy, hx + 76, hy + 22], fill=(200, 40, 50))
    d.line([hx + 8, hy + 8, hx - 26, hy + 4], fill=(80, 80, 80), width=4)
    d.line([hx + 20, hy - 6, hx + 56, hy - 6], fill=(80, 80, 80), width=3)
    d.line([hx + 30, hy + 22, hx + 30, hy + 44], fill=(80, 80, 80), width=3)
    d.line([hx + 46, hy + 22, hx + 46, hy + 44], fill=(80, 80, 80), width=3)
    # sea
    d.rectangle([x, y + h - 70, x + w, y + h], fill=(40, 90, 130))
    d.line([x, y + h - 58, x + w, y + h - 58], fill=(255, 255, 255), width=3)
    # cargo ship: hull, containers, bridge
    d.rectangle([x + 40, y + h - 62, x + 268, y + h - 30], fill=(60, 60, 66))
    for i, c in enumerate([(200, 60, 50), (230, 180, 74), (60, 130, 180)]):
        d.rectangle([x + 52 + i * 44, y + h - 96, x + 90 + i * 44, y + h - 62],
                    fill=c, outline=(255, 255, 255), width=2)
    d.rectangle([x + 226, y + h - 96, x + 262, y + h - 62], fill=(240, 240, 240))
    # fire and smoke from the bridge
    for fx, fy, fr in [(228, 96, 14), (246, 84, 18), (262, 98, 12)]:
        d.ellipse([x + fx, y + fy, x + fx + fr, y + fy + fr], fill=(240, 120, 30))
    for sx, sy, sr in [(240, 52, 14), (256, 34, 18), (272, 18, 12)]:
        d.ellipse([x + sx, y + sy, x + sx + sr, y + sy + sr], fill=(120, 120, 120))


def draw_mexico(d, x, y, w, h):
    # Desert dusk: road, burning roadblock, helicopter, handcuffs
    d.rectangle([x, y, x + w, y + h], fill=(232, 190, 130))
    # sun low on the horizon
    d.ellipse([x + 34, y + 26, x + 86, y + 78], fill=(240, 140, 60))
    # distant hills
    d.polygon([(x, y + 110), (x + 90, y + 66), (x + 180, y + 110)],
              fill=(190, 130, 90))
    d.polygon([(x + 150, y + 110), (x + 240, y + 58), (x + w, y + 110)],
              fill=(170, 115, 80))
    # road
    d.polygon([(x + 60, y + h), (x + 130, y + 110), (x + 190, y + 110),
               (x + 260, y + h)], fill=(90, 88, 86))
    d.line([x + 158, y + 120, x + 160, y + h], fill=(255, 220, 80), width=4)
    # burning barricade on the road
    bx, by = x + 116, y + 132
    d.rectangle([bx, by, bx + 88, by + 18], fill=(60, 60, 60))
    for fx, fy, fr in [(126, 108, 14), (146, 100, 18), (168, 110, 12)]:
        d.ellipse([x + fx, y + fy, x + fx + fr, y + fy + fr], fill=(240, 120, 30))
    # helicopter above
    hx, hy = x + 216, y + 34
    d.ellipse([hx, hy, hx + 70, hy + 20], fill=(40, 40, 44))
    d.line([hx + 14, hy - 6, hx + 56, hy - 6], fill=(40, 40, 44), width=3)
    # handcuffs, lower left
    cx, cy = x + 52, y + h - 52
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], outline=(60, 60, 66),
              width=6)
    d.ellipse([cx + 34, cy - 16, cx + 66, cy + 16], outline=(60, 60, 66),
              width=6)
    d.line([cx + 14, cy, cx + 36, cy], fill=(60, 60, 66), width=5)


def draw_denmark(d, x, y, w, h):
    # Concert stage: microphone, shield, Danish flag, suitcase of the expelled
    d.rectangle([x, y, x + w, y + h], fill=(224, 214, 196))
    # stage curtains
    d.polygon([(x, y), (x + 56, y), (x + 30, y + h - 60), (x, y + h - 60)],
              fill=(160, 40, 50))
    d.polygon([(x + w, y), (x + w - 56, y), (x + w - 30, y + h - 60),
               (x + w, y + h - 60)], fill=(160, 40, 50))
    # microphone on a stand
    mx, my = x + w // 2, y + 44
    d.ellipse([mx - 20, my - 20, mx + 20, my + 20], fill=(70, 70, 76))
    for i in range(3):
        d.line([mx - 14 + i * 14, my - 12, mx - 14 + i * 14, my + 12],
               fill=(200, 200, 200), width=2)
    d.line([mx, my + 20, mx, y + 140], fill=(70, 70, 76), width=5)
    d.line([mx - 26, y + 140, mx + 26, y + 140], fill=(70, 70, 76), width=5)
    # shield with a check, lower left
    sx, sy = x + 52, y + h - 96
    d.polygon([(sx, sy), (sx + 52, sy), (sx + 52, sy + 34), (sx + 26, sy + 58),
               (sx, sy + 34)], fill=(30, 90, 170))
    d.line([sx + 12, sy + 28, sx + 22, sy + 38], fill=(255, 255, 255), width=4)
    d.line([sx + 22, sy + 38, sx + 42, sy + 14], fill=(255, 255, 255), width=4)
    # Danish flag (red, white cross), lower right
    fx, fy = x + w - 108, y + h - 66
    d.rectangle([fx, fy, fx + 84, fy + 48], fill=(200, 40, 50))
    d.rectangle([fx + 26, fy, fx + 38, fy + 48], fill=(255, 255, 255))
    d.rectangle([fx, fy + 18, fx + 84, fy + 30], fill=(255, 255, 255))
    # suitcase of the expelled attache
    bx, by = x + 150, y + h - 52
    d.rectangle([bx, by, bx + 64, by + 40], fill=(120, 90, 60))
    d.rectangle([bx + 22, by - 8, bx + 42, by], outline=(120, 90, 60), width=4)
    d.line([bx + 32, by, bx + 32, by + 40], fill=(90, 66, 44), width=3)


def draw_fbi(d, x, y, w, h):
    # A laptop flashing a warning, database cylinders, a padlock
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 238))
    # database cylinders, left
    for i, cy in enumerate([52, 108]):
        d.ellipse([x + 30, y + cy, x + 96, y + cy + 24], fill=(90, 110, 150))
        d.rectangle([x + 30, y + cy + 12, x + 96, y + cy + 44],
                    fill=(70, 90, 130))
        d.ellipse([x + 30, y + cy + 32, x + 96, y + cy + 56], fill=(50, 70, 110))
        d.line([x + 30, y + cy + 12, x + 30, y + cy + 44], fill=(255, 255, 255),
               width=2)
    # laptop screen with a warning triangle
    lx, ly = x + 130, y + 44
    d.rectangle([lx, ly, lx + 156, ly + 104], fill=(30, 34, 44),
                outline=(120, 120, 130), width=3)
    d.polygon([(lx + 78, ly + 18), (lx + 44, ly + 78), (lx + 112, ly + 78)],
              fill=(240, 180, 40))
    fnt = font(F_BOLD, 30)
    d.text((lx + 71, ly + 46), "!", font=fnt, fill=(30, 34, 44))
    # laptop base
    d.polygon([(lx - 14, ly + 104), (lx + 170, ly + 104), (lx + 184, ly + 122),
               (lx - 28, ly + 122)], fill=(120, 124, 132))
    # padlock, lower right
    px, py = x + 216, y + h - 74
    d.arc([px, py - 22, px + 56, py + 14], start=180, end=360,
          fill=(60, 60, 66), width=7)
    d.rectangle([px, py, px + 56, py + 46], fill=RED)
    d.ellipse([px + 22, py + 12, px + 34, py + 24], fill=(255, 255, 255))
    d.rectangle([px + 25, py + 22, px + 31, py + 36], fill=(255, 255, 255))


STORIES = [
    dict(tag="GULF", color=(27, 42, 74),
         draw=draw_gulf,
         headline="IRAN HITS US BASES IN BAHRAIN",
         sub="IRGC claims two Patriot radars destroyed; Bahrain reports fire, no injuries"),
    dict(tag="CLIMATE", color=(24, 120, 110),
         draw=draw_climate,
         headline="COP31 DEADLOCKS IN OVERTIME",
         sub="Antalya draft drops fossil fuels and $120bn finance; 1.5C goal missed"),
    dict(tag="BALTIC", color=(40, 90, 130),
         draw=draw_baltic,
         headline="RUSSIAN SHIP ABLAZE OFF FINLAND",
         sub="Sparta II hit by drones; crew of 16 evacuated as ship drifts into Finnish waters"),
    dict(tag="MEXICO", color=(150, 70, 30),
         draw=draw_mexico,
         headline="FBI'S MOST-WANTED CARTEL BOSS SEIZED",
         sub="'El Chapo Isidro' captured in Sinaloa; gun battles and burning roadblocks follow"),
    dict(tag="EUROPE", color=(160, 40, 50),
         draw=draw_denmark,
         headline="DENMARK FOILS PLOT TO KILL RAPPER",
         sub="Russia accused over Kyivstoner hit; two charged, defence attache expelled"),
    dict(tag="USA", color=(60, 70, 110),
         draw=draw_fbi,
         headline="FBI PROBES HACK OF CRIME DATABASE",
         sub="Apparent breach of the NCIC system under investigation, AP source says"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    f_mast = font(F_BOLD, 52)
    mast = "THE WORLD IN ONE DAY"
    tw = d.textlength(mast, font=f_mast)
    d.text(((W - tw) / 2, 10), mast, font=f_mast, fill=(255, 255, 255))
    f_date = font(F_BOLD, 32)
    date = "SUNDAY, 22 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 80), date, font=f_date, fill=GOLD)
    f_sub = font(F_REG, 17)
    tagline = "Six stories from around the world  •  One day's news"
    tw = d.textlength(tagline, font=f_sub)
    d.text(((W - tw) / 2, 120), tagline, font=f_sub, fill=(200, 205, 220))

    # Grid of panels: 3 columns x 2 rows
    px = [12, 349, 686]
    py = [160, 572]
    pw, ph = 326, 400
    ill_h = 196
    for i, s in enumerate(STORIES):
        x = px[i % 3]
        y = py[i // 3]
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL_BG, outline=BORDER,
                    width=2)
        s["draw"](d, x + 8, y + 8, pw - 16, ill_h)
        tag_chip(d, x + 8, y + 8, s["tag"], s["color"])
        # Headline, up to two lines
        hfnt, hlines = fit_text(d, s["headline"], F_BOLD, 27, pw - 24, 2)
        hy = y + 8 + ill_h + 14
        for line in hlines:
            d.text((x + 12, hy), line, font=hfnt, fill=INK)
            hy += hfnt.size + 4
        # Sub-line, pinned to the panel bottom
        sfnt, slines = fit_text(d, s["sub"], F_REG, 19, pw - 24, 2)
        sy = y + ph - 14 - len(slines) * (sfnt.size + 3)
        for line in slines:
            d.text((x + 12, sy), line, font=sfnt, fill=MUTED)
            sy += sfnt.size + 3

    # Footer ticker
    d.rectangle([0, 980, W, H], fill=NAVY)
    tick = ("ALSO TODAY:  Peru shaken by a 6.9 quake, no damage reported  •  "
            "Trump, Xi and Putin met in Shenzhen  •  Modi opens Nitish Setu in Bihar")
    f_tick = font(F_REG, 17)
    while d.textlength(tick, font=f_tick) > W - 16 and f_tick.size > 10:
        f_tick = font(F_REG, f_tick.size - 1)
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 995), tick, font=f_tick, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
