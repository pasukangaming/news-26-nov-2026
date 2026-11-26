#!/usr/bin/env python3
"""Draw the 26 November 2026 front page (build-time only).

Renders a newspaper front page as entry.png. The graded program (main.ts)
only copies this pre-drawn image; nothing is drawn at grade time.
Lead story: Trump proposes new tariffs on 14 trading partners.
Secondary: Cairo tanker fire (31 killed), Houthi strikes on Saudi Arabia,
Russian missiles hit Kyiv.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (178, 28, 28)
NAVY = (30, 58, 95)
STEEL = (70, 90, 120)
GREY = (90, 85, 75)
LIGHT = (238, 232, 218)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def center(draw, y, text, fnt, fill=INK, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer frame
d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)

# ---- masthead ----
center(d, 34, "THE WORLD TODAY", font(SERIF_B, 84))
d.line([36, 138, W - 36, 138], fill=INK, width=2)
f_date = font(SANS_B, 21)
d.text((36, 150), "THURSDAY, 26 NOVEMBER 2026", font=f_date, fill=INK)
right = "WORLD NEWS IN ONE IMAGE"
d.text((W - 36 - d.textlength(right, font=f_date), 150),
       right, font=f_date, fill=RED)
d.line([36, 182, W - 36, 182], fill=INK, width=4)
d.line([36, 189, W - 36, 189], fill=INK, width=1)

# ---- lead kicker + headline ----
d.text((36, 206), "TRADE WAR  •  WASHINGTON", font=font(SANS_B, 22), fill=RED)
f_head = font(SERIF_B, 58)
lines = wrap(d, "TRUMP HITS 14 NATIONS WITH NEW TARIFFS", f_head, W - 72)
y = 240
for line in lines:
    d.text((36, y), line, font=f_head, fill=INK)
    y += 66

f_sub = font(SANS, 25)
sub = ("Washington accuses its partners of flooding world markets with "
       "excess factory output — and answers with the biggest tariff "
       "salvo of the year.")
lines = wrap(d, sub, f_sub, W - 72)
y += 8
for line in lines:
    d.text((36, y), line, font=f_sub, fill=INK)
    y += 33

# ---- tariff chart panel ----
panel_top, panel_bot = y + 14, y + 14 + 252
d.rectangle([36, panel_top, W - 36, panel_bot], fill=LIGHT, outline=INK, width=2)
d.text((56, panel_top + 12), "THE PROPOSED TARIFFS — BY TRADING PARTNER",
       font=font(SANS_B, 22), fill=NAVY)
d.text((56, panel_top + 40), "Rates announced 26 November 2026, not yet in force",
       font=font(SANS, 19), fill=GREY)

rates = [("Vietnam", 35), ("India", 25), ("China", 20),
         ("EU", 15), ("Japan", 15), ("S. Korea", 15)]
chart_x0, chart_x1 = 56, W - 56
base_y = panel_bot - 44
max_h = 118
slot = (chart_x1 - chart_x0) / len(rates)
bar_w = 74
f_lab, f_val = font(SANS_B, 20), font(SANS_B, 22)
for i, (name, rate) in enumerate(rates):
    cx = chart_x0 + slot * i + slot / 2
    h = max_h * rate / 35.0
    color = RED if rate >= 25 else NAVY
    d.rectangle([cx - bar_w / 2, base_y - h, cx + bar_w / 2, base_y],
                fill=color)
    val = f"{rate}%"
    d.text((cx - d.textlength(val, font=f_val) / 2, base_y - h - 30),
           val, font=f_val, fill=color)
    lab = name
    d.text((cx - d.textlength(lab, font=f_lab) / 2, base_y + 8),
           lab, font=f_lab, fill=INK)
d.line([chart_x0, base_y, chart_x1, base_y], fill=INK, width=2)

# ---- secondary stories ----
y = panel_bot + 22
d.line([36, y, W - 36, y], fill=INK, width=2)
y += 16
stories = [
    ("CAIRO, EGYPT",
     "Tanker fire kills at least 31 on ring road",
     "A fuel tanker overturned and burst into flames on the Cairo ring "
     "road; 31 dead, about 21 hurt."),
    ("RED SEA  •  SAUDI ARABIA",
     "Houthis strike Saudi ports and refinery",
     "Yemen's Houthis hit Saudi ports and the Ras Tanura refinery; "
     "oil climbs as supply fears grow."),
    ("KYIV, UKRAINE",
     "Russian missiles hit Kyiv; seven wounded",
     "Ballistic missiles struck the capital overnight as diplomacy to "
     "end the war faces new uncertainty."),
]
col_w = (W - 72 - 2 * 28) / 3
f_kick, f_st, f_sum = font(SANS_B, 17), font(SERIF_B, 23), font(SANS, 17)
for i, (kick, head, summ) in enumerate(stories):
    x = 36 + i * (col_w + 28)
    d.text((x, y), kick, font=f_kick, fill=RED)
    hl = wrap(d, head, f_st, col_w)
    yy = y + 26
    for line in hl:
        d.text((x, yy), line, font=f_st, fill=INK)
        yy += 28
    sl = wrap(d, summ, f_sum, col_w)
    yy += 4
    for line in sl:
        d.text((x, yy), line, font=f_sum, fill=(60, 58, 52))
        yy += 22

# ---- footer ticker ----
fy = H - 104
d.line([36, fy, W - 36, fy], fill=INK, width=2)
f_tick = font(SANS, 18)
tick = ("ALSO TODAY:  North Korea vows more nuclear weapons  •  First "
        "Pakistani astronaut boards China's Tiangong station  •  SpaceX "
        "cleared for one million satellites")
lines = wrap(d, tick, f_tick, W - 72)
yy = fy + 12
for line in lines:
    d.text((36, yy), line, font=f_tick, fill=INK)
    yy += 24
center(d, H - 38, "—  THE WORLD TODAY  •  26 NOVEMBER 2026  —",
       font(SANS_B, 17), fill=GREY)

img.save("entry.png", "PNG", optimize=True)
print("saved entry.png", img.size)
