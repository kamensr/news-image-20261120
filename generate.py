#!/usr/bin/env python3
"""Poster builder for the news-image-20261120 make.fun entry.

Draws a 1024x1024 flat news-poster for Friday 20 November 2026 using PIL
only. All story text comes from the research brief: 4 illustrated features,
12 mini-stories, 33 one-liners (49 stories total), a UTC timeline strip,
a world map with 12 numbered pins, a DATE CHECK box and a sources footer.
"""

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W, H = 1024, 1024

# --- palette (flat newsprint) ---------------------------------------------
INK = (17, 24, 39)
PAPER = (247, 245, 238)
NAVY = (11, 31, 58)
NAVY_SOFT = (27, 58, 95)
RED = (178, 34, 34)
RED_SOFT = (214, 90, 90)
GOLD = (176, 132, 24)
TEAL = (14, 116, 110)
GREY = (90, 96, 108)
LIGHT_LINE = (203, 205, 198)
CARD = (255, 255, 255)
SEA = (214, 231, 240)
LAND = (196, 214, 178)
LAND_EDGE = (150, 172, 132)
AMBER_BG = (255, 243, 205)
GREEN_TAG = (22, 101, 52)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap_text(text, fnt, width):
    """Greedy word wrap using real font metrics."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if fnt.getlength(trial) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None, max_lines=None):
    lines = wrap_text(text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    step = leading if leading else int(fnt.size * 1.28)
    for i, ln in enumerate(lines):
        draw.text((x, y + i * step), ln, font=fnt, fill=fill)
    return y + len(lines) * step


def fit_size(draw, text, start, floor, width, fname="DejaVuSans.ttf"):
    """Largest font size >= floor that fits `text` in `width`."""
    size = start
    while size > floor:
        f = font(fname, size)
        if f.getlength(text) <= width:
            return f
        size -= 1
    return font(fname, floor)


# --- story data (from the research brief, 20 Nov 2026) --------------------
FEATURES = [
    {
        "num": "1", "tag": "EUROPE / CONFLICT", "accent": RED,
        "head": "RUSSIA'S BIGGEST ATTACK ON UKRAINE THIS YEAR",
        "body": ("Overnight into Fri, Russia fired 110+ missiles (27 ballistic, only 3 "
                 "intercepted) + ~400 drones at Ukraine \u2014 Zelensky: \u201cthe biggest "
                 "this year.\u201d Three Dnipro bridges hit; 9 killed, 28+ hurt; power "
                 "cuts in Kyiv + 3 regions; a hospital hit in Kharkiv. UNICEF: child "
                 "casualties at a near-4-year high."),
        "verdict": "CONFIRMED", "src": "CNN \u00b7 Kyiv Independent \u00b7 Reuters",
        "glyph": "\u2601",
    },
    {
        "num": "2", "tag": "ASIA-PACIFIC / WEATHER", "accent": TEAL,
        "head": "CYCLONE AKVAN SLAMS INDIA'S EAST COAST",
        "body": ("Severe cyclone crossed the north Andhra Pradesh / south Odisha coasts "
                 "near Gopalpur 02:00\u201303:00 UTC; winds 70\u201380 km/h, gusts 90. "
                 "300,000+ evacuated across 20 Odisha districts. No deaths or major "
                 "damage in the initial assessment; 209mm rain at Patrapur. Third "
                 "cyclone in under a month; deep depression by 09:00 UTC."),
        "verdict": "CONFIRMED", "src": "Reuters \u00b7 Watchers.news \u00b7 Hindu BusinessLine",
        "glyph": "\u2601",
    },
    {
        "num": "3", "tag": "GLOBAL / CLIMATE", "accent": GOLD,
        "head": "COP31: NO DEAL BY FRIDAY'S DEADLINE",
        "body": ("The final scheduled day in Antalya, T\u00fcrkiye ended with NO deal "
                 "\u2014 talks in overtime into the weekend (median finish ~Sun 22:35). "
                 "The draft drops ALL fossil-fuel language and the $120bn/yr "
                 "adaptation target. 23+ countries object; a Germany-led coalition "
                 "pushes to restore it; Panama may block. First COP to acknowledge a "
                 "1.5\u00b0C overshoot."),
        "verdict": "CONFIRMED \u00b7 OUTCOME PENDING", "src": "Reuters \u00b7 UN News \u00b7 Carbon Brief",
        "glyph": "\u2600",
    },
    {
        "num": "4", "tag": "EUROPE / SECURITY", "accent": NAVY_SOFT,
        "head": "RUSSIAN MISSILES VIOLATE POLISH AIRSPACE",
        "body": ("Three Russian objects crossed into Poland overnight: a Kh-101 near "
                 "Nowy Lipowiec (~05:40 GMT), a 2nd missile near Rudnik nad Sanem, a "
                 "jet-powered drone near Mo\u0142odycz. No injuries or damage. Polish "
                 "F-16s + Swedish Gripens scrambled, Patriots activated, "
                 "Rzesz\u00f3w-Jasionka tower evacuated \u2014 a first. PM Tusk: "
                 "\u201cintentional provocation.\u201d"),
        "verdict": "CONFIRMED", "src": "Reuters \u00b7 EU Today \u00b7 National Security News",
        "glyph": "\u2694",
    },
]

MINIS = [
    ("1", "US ROUT, DAY 7 \u2014 CLOSE",
     "S&P 6,910.39 -3.70% (7th straight loss); Nasdaq -5.28%; Dow -1.93% (-950 pts); VIX 35.89 +26.2%."),
    ("2", "ASIA SELLS OFF",
     "Nikkei ~-5%; SoftBank -16%+; Korea sell-side halt; Shanghai -1.22%, lowest since Jul 2025."),
    ("3", "EU\u2013UK SUMMIT",
     "Brussels: food checks scrapped; youth mobility 100k places/side, to 31, from Jan 2030; tuition deferred 6 mo."),
    ("4", "IRAQ: JURF AL-SAKHAR",
     "Iraqi forces to deploy in Jurf al-Sakhar Fri; Kataib Hezbollah to withdraw. (PM unnamed.)"),
    ("5", "DOROGOBUZH PLANT HIT",
     "Drones hit Dorogobuzh plant overnight; blast + fire. CLAIM: 'reportedly Ukrainian drones' \u2014 unverified."),
    ("6", "EUROPE YOUTH STRIKE",
     "Tens of thousands strike in 25+ nations \u2014 'Money for schools, not war.' 350+ UK schools walk out."),
    ("7", "TAIWAN FLAGS 2,700 ACCOUNTS",
     "Taiwan flags ~2,700 China-linked accounts to Meta ahead of 28 Nov polls; mostly Threads (2,400)."),
    ("8", "JAPAN CPI +2.2%",
     "Core CPI +2.2% y/y in Oct (vs 2.3% f'cast); headline 2.3%. BoJ hike 18 Dec to 1.50% expected."),
    ("9", "CHINA HOLDS RATES",
     "LPR unchanged for an 18th straight month: 1-yr 3.00%, 5-yr 3.50%."),
    ("10", "KOREA CHOLERA, FIRST IN 10 YEARS",
     "KDCA: first cholera case since 2016 \u2014 Changwon patient, no travel; Vibrio cholerae O1 Ogawa."),
    ("11", "CYCLONE XAVIER WEAKENS",
     "Xavier weakening near Cook Islands after peaking Cat 5 Tue (220 km/h) \u2014 strongest Nov cyclone east of dateline."),
    ("12", "GTA 6: $2.36BN",
     "Sensor Tower: $2.36bn sales, 24.58m copies \u2014 biggest launch ever; Metacritic 99. Estimates only."),
]

# One-liners, overall story numbers 17-49 (brief items 13-45 in order).
ALSO = [
    (17, "Pakistan beat Sri Lanka by 8 wkts, 2nd Test \u2014 series 1-0"),
    (18, "NZ 368 (Nicholls 175*, Phillips 118); India reply: Jaiswal 85"),
    (19, "India A beat Nepal, Rising Stars Asia Cup \u2014 Tilak + Kushagra tons"),
    (20, "East Bengal 2-2 SC Delhi, Indian Super League"),
    (21, "Satwik/Chirag into Hong Kong Open badminton semis"),
    (22, "SMAT: Maharashtra, Punjab, UP win (Bhuvneshwar 3-19)"),
    (23, "Bangladesh: paramilitary deployed; 2 killed, 107 held, station torched"),
    (24, "Myanmar REJECTS ICJ Rohingya ruling (ruling was Thu)"),
    (25, "India's MEA answers USCIRF chief's post on Muslims"),
    (26, "Pakistan climate minister confronted on arrival in India"),
    (27, "India's NCB + US DEA shut drug syndicate's Indian base"),
    (28, "Iran marks World Children's Day; tribute to Khamenei's kin"),
    (29, "Ukraine: 40 Russian oil/military targets hit in 50 days"),
    (30, "ATP Finals: Shelton, Zverev into semis in Turin"),
    (31, "Pochettino apologises over drone footage at Man Utd ground"),
    (32, "US sentiment: UMich Nov final 51.5; 1-yr inflation 3.7%"),
    (33, "Gold falls 4.2% Friday, down ~11% in a month"),
    (34, "Brent crude $90.05 (+0.7%)"),
    (35, "US 10-yr Treasury yield 4.91% (-14bp) at close"),
    (36, "Yen near 159 per US dollar"),
    (37, "Anthropic -13% to ~$84.40, back near $83 IPO price"),
    (38, "AMD -7%+ after Hunterbrook short report on China"),
    (39, "White House names Kirsten Davies national cyber director"),
    (40, "Trump presser: Thailand + Philippines trade deals touted"),
    (41, "NYC Mayor Mamdani to shut Rikers Island jail by 2032"),
    (42, "Jennifer Lagner wins Atlantic Beach seat on a coin toss"),
    (43, "California Bar probes ex-press secretary Katie Zacharia"),
    (44, "At least 12 people in Brookline, MA attacked by a suspected owl"),
    (45, "Princeton PhD student detained by ICE \u2014 reported Fri"),
    (46, "SoCal floods recede; LA ocean-water advisory to 23 Nov"),
    (47, "Brazil's B3 exchange closed for Black Consciousness Day"),
    (48, "Estonia closes border with Russia for \u22656 months"),
    (49, "Qeshm Island blast: unexploded munitions disposal, not a strike"),
]

TIMELINE = [
    (0.0, "Kyiv attack begins (23:25 UTC 19 Nov)"),
    (1.0, "China holds rates"),
    (2.0, "Akvan landfall, India"),
    (5.55, "Taiwan flags \u00b7 Poland missile \u00b7 Akvan done"),
    (6.0, "Nikkei closes ~-5%"),
    (9.0, "Akvan downgraded"),
    (9.75, "40 targets hit in 50 days"),
    (14.5, "US markets open"),
    (15.0, "UMich sentiment 51.5"),
    (17.0, "Trump presser \u00b7 Qeshm blast"),
    (21.0, "NYSE close: S&P -3.70%"),
]

# (label, lon, lat)
PINS = [
    ("1", "Gopalpur", 84.9, 19.3),
    ("2", "Kyiv", 30.5, 50.45),
    ("3", "Antalya", 30.7, 36.9),
    ("4", "Nowy Lipowiec", 22.5, 50.3),
    ("5", "Brussels", 4.35, 50.85),
    ("6", "Jurf al-Sakhar", 44.2, 32.9),
    ("7", "Dorogobuzh", 33.3, 54.9),
    ("8", "Taipei", 121.6, 25.0),
    ("9", "Tokyo", 139.7, 35.7),
    ("10", "Beijing", 116.4, 39.9),
    ("11", "Changwon", 128.7, 35.2),
    ("12", "Cook Islands", -160.0, -21.2),
]

# Rough continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 35), (-80, 25),
     (-85, 20), (-90, 15), (-95, 18), (-105, 20), (-115, 28), (-125, 40),
     (-125, 50), (-140, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -45), (-70, -52), (-73, -40),
     (-72, -20), (-80, -5), (-80, 5)],
    [(-10, 36), (-9, 43), (0, 48), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (45, 68),
     (48, 60), (40, 55), (35, 50), (28, 45), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 42), (0, 39), (-2, 37), (-9, 37)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 20), (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (32, -28),
     (25, -34), (18, -32), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 12)],
    [(30, 70), (45, 68), (60, 70), (70, 72), (90, 75), (110, 76), (130, 72),
     (160, 70), (180, 65), (170, 60), (162, 55), (158, 50), (142, 45),
     (135, 40), (130, 35), (127, 33), (122, 30), (120, 25), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 10), (77, 8),
     (72, 20), (66, 25), (60, 25), (55, 26), (50, 30), (48, 30), (43, 35),
     (36, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20),
     (113, -22)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (144, 44),
     (142, 40), (138, 35), (132, 33), (130, 31)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51), (-3, 50)],
    [(95, 5), (105, -5), (115, -8), (125, -9), (135, -8), (140, -8),
     (138, -4), (130, 0), (120, 0), (110, -7), (100, 0), (95, 5)],
]

DATE_CHECK = ("DATE CHECK \u2014 NOT 20 NOV, EXCLUDED: Trump\u2013Xi\u2013Putin Shenzhen "
              "summit (19 Nov) \u00b7 Anthropic IPO debut (19 Nov) \u00b7 ICJ Rohingya "
              "ruling (19 Nov) \u00b7 Gaza Yellow Line op (19 Nov) \u00b7 Houthi missile "
              "on Riyadh PIF Tower (19 Nov) \u00b7 Japan\u2013India 2+2 pact (19 Nov) \u00b7 "
              "BepiColombo Mercury insertion (21 Nov \u2014 not yet).")
SOURCES = ("SOURCES: Reuters, AP, CNN, BBC, Kyiv Independent, WSJ, Barron's, UN News, "
           "MetService NZ, Fiji Met Service, Watchers.news, Hindu BusinessLine, "
           "Bloomberg Law, Inshorts (single-source items marked).")


def section_head(draw, x, y, w, title, right=None):
    draw.rectangle([x, y, x + w, y + 17], fill=NAVY)
    draw.text((x + 8, y + 2), title, font=SANS_B(11), fill=(255, 255, 255))
    if right:
        rf = SANS_B(10)
        draw.text((x + w - rf.getlength(right) - 8, y + 3), right, font=rf,
                  fill=(200, 210, 225))
    return y + 21


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 16  # margin
    CW = W - 2 * M  # 992

    # ---- kicker band ------------------------------------------------------
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((M, 5), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=SANS_B(13), fill=(255, 255, 255))
    right = "49 STORIES \u00b7 7 REGIONS"
    rf = SANS_B(13)
    d.text((W - M - rf.getlength(right), 5), right, font=rf, fill=(255, 209, 102))

    # ---- masthead ---------------------------------------------------------
    mast = "FRIDAY 20 NOVEMBER 2026"
    mf = SERIF_B(45)
    # shrink until it fits the full width
    while mf.getlength(mast) > CW and mf.size > 20:
        mf = SERIF_B(mf.size - 1)
    d.text((M, 30), mast, font=mf, fill=INK)
    sub = "THE WORLD IN ONE PICTURE \u2014 EVERY STORY FROM FRIDAY 20 NOVEMBER 2026"
    d.text((M, 82), sub, font=SANS_B(12), fill=GREY)
    d.line([(M, 99), (W - M, 99)], fill=RED, width=3)

    # ---- UTC timeline strip ----------------------------------------------
    # ---- UTC timeline strip ----------------------------------------------
    y0 = 106
    y0 = section_head(d, M, y0, CW, "FRIDAY 20 NOVEMBER 2026 \u2014 UTC TIMELINE",
                      right="ALL TIMES UTC")
    axis_y = y0 + 24
    d.rectangle([M, y0, W - M, y0 + 48], fill=CARD, outline=LIGHT_LINE)
    d.line([(M + 6, axis_y), (W - M - 6, axis_y)], fill=NAVY, width=2)
    # hour ticks only (no text -- event labels carry the times)
    for hr in range(0, 25, 3):
        x = M + 6 + (W - 2 * M - 12) * hr / 24.0
        d.line([(x, axis_y - 3), (x, axis_y + 3)], fill=NAVY, width=1)
    # event markers; labels placed greedily into 4 rows so none overlap
    lab_f = SANS(9)
    rows_y = [y0 + 3, y0 + 13, axis_y + 5, axis_y + 15]
    placed = {r: [] for r in rows_y}
    for hr, label in TIMELINE:
        x = M + 6 + (W - 2 * M - 12) * hr / 24.0
        d.ellipse([x - 4, axis_y - 4, x + 4, axis_y + 4], fill=RED,
                  outline=(255, 255, 255))
        lw = lab_f.getlength(label)
        lx = min(max(x - lw / 2, M + 2), W - M - 2 - lw)
        for ry in rows_y:
            if all(lx > ex + 6 or lx + lw < sx - 6 for sx, ex in placed[ry]):
                placed[ry].append((lx, lx + lw))
                d.text((lx, ry), label, font=lab_f, fill=NAVY)
                break


    # ---- 4 features, 2x2 --------------------------------------------------
    fy = 178
    fh = 132
    fw = (CW - 8) // 2
    for idx, feat in enumerate(FEATURES):
        fx = M + (idx % 2) * (fw + 8)
        fyy = fy + (idx // 2) * (fh + 6)
        d.rectangle([fx, fyy, fx + fw, fyy + fh], fill=CARD, outline=LIGHT_LINE)
        d.rectangle([fx, fyy, fx + fw, fyy + 5], fill=feat["accent"])
        # number badge + glyph
        d.ellipse([fx + 10, fyy + 14, fx + 34, fyy + 38], fill=feat["accent"])
        nf = SANS_B(13)
        num = feat["num"]
        d.text((fx + 22 - nf.getlength(num) / 2, fyy + 18), num, font=nf,
               fill=(255, 255, 255))
        d.text((fx + 40, fyy + 16), feat["tag"], font=SANS_B(11),
               fill=feat["accent"])
        # verdict chip, right-aligned
        vf = SANS_B(9)
        vw = vf.getlength(feat["verdict"]) + 12
        d.rounded_rectangle([fx + fw - vw - 8, fyy + 13, fx + fw - 8, fyy + 29],
                            radius=6, fill=AMBER_BG, outline=GOLD)
        d.text((fx + fw - vw - 2, fyy + 16), feat["verdict"], font=vf,
               fill=GREEN_TAG if "PENDING" not in feat["verdict"] else (120, 80, 0))
        # headline (2 lines max)
        hf = SANS_B(15)
        hl = wrap_text(feat["head"], hf, fw - 20)[:2]
        hy = fyy + 40
        for j, ln in enumerate(hl):
            d.text((fx + 10, hy + j * 17), ln, font=hf, fill=INK)
        # body
        by = hy + len(hl) * 17 + 3
        body_lines = wrap_text(feat["body"], SANS(10), fw - 20)
        for j, ln in enumerate(body_lines[:4]):
            d.text((fx + 10, by + j * 12), ln, font=SANS(10), fill=(45, 50, 60))
        # source footer
        sf = SANS(9)
        d.text((fx + 10, fyy + fh - 14), feat["src"], font=sf, fill=GREY)

    # ---- 12 minis, 3 columns x 4 rows -------------------------------------
    my = fy + 2 * fh + 6 + 6  # 440
    my = section_head(d, M, my, CW, "THE DAY IN BRIEF \u2014 12 MORE STORIES",
                      right="STORIES 5\u201316")
    col_w = (CW - 16) // 3
    row_h = 37
    for i, (num, head, body) in enumerate(MINIS):
        col = i % 3
        row = i // 3
        x = M + col * (col_w + 8)
        y = my + row * row_h
        if col:
            d.line([(x - 5, y + 2), (x - 5, y + row_h - 4)], fill=LIGHT_LINE)
        # number chip
        d.rounded_rectangle([x, y + 1, x + 18, y + 15], radius=3, fill=NAVY)
        nf = SANS_B(9)
        d.text((x + 9 - nf.getlength(num) / 2, y + 3), num, font=nf,
               fill=(255, 255, 255))
        hf = fit_size(d, head, 11, 8, col_w - 24, "DejaVuSans-Bold.ttf")
        d.text((x + 22, y + 1), head, font=hf, fill=INK)
        bl = wrap_text(body, SANS(10), col_w - 4)[:2]
        for j, ln in enumerate(bl):
            d.text((x + 2, y + 16 + j * 11), ln, font=SANS(10), fill=(45, 50, 60))

    # ---- world map with 12 pins -------------------------------------------
    map_y = my + 4 * row_h + 8
    map_y = section_head(d, M, map_y, CW, "WHERE IT HAPPENED \u2014 12 PLACES ON THE MAP")
    map_top = map_y
    map_h = 104
    d.rectangle([M, map_top, W - M, map_top + map_h], fill=SEA, outline=LIGHT_LINE)

    def project(lon, lat):
        px = M + (lon + 180.0) / 360.0 * CW
        py = map_top + (75.0 - lat) / 130.0 * map_h
        return px, py

    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # pin labels placed to avoid the dense Europe cluster
    label_dx = {"2": (-30, 12), "3": (-12, 12), "4": (-64, -18), "5": (-52, -4),
                "6": (8, 0), "7": (16, -16), "8": (6, 2), "9": (6, -6),
                "10": (-48, -16), "11": (8, -18), "1": (6, 2), "12": (6, 2)}
    # Dorogobuzh's pin would sit on top of Kyiv's -- nudge it with a leader line
    pin_off = {"7": (16, -16)}
    # circles first (a later circle must never cover an earlier label)
    placed_pins = {}
    for num, name, lon, lat in PINS:
        px, py = project(lon, lat)
        ox, oy = pin_off.get(num, (0, 0))
        if (ox, oy) != (0, 0):
            d.line([(px, py), (px + ox, py + oy)], fill=GREY, width=1)
            px, py = px + ox, py + oy
        placed_pins[num] = (px, py)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        pf = SANS_B(9)
        d.text((px - pf.getlength(num) / 2, py - 6), num, font=pf,
               fill=(255, 255, 255))
    # labels second, on top of every circle
    for num, name, lon, lat in PINS:
        px, py = placed_pins[num]
        dx, dy = label_dx.get(num, (6, 2))
        d.text((px + dx, py + dy), name, font=SANS(9), fill=NAVY)

    # ---- ALSO ON 20 NOV, stories 17-49, 3 columns x 11 rows --------------
    ay = map_top + map_h + 10
    ay = section_head(d, M, ay, CW, "ALSO ON 20 NOV", right="STORIES 17\u201349")
    col_w = (CW - 16) // 3
    row_h = 16
    for i, (num, text) in enumerate(ALSO):
        col = i % 3
        row = i // 3
        x = M + col * (col_w + 8)
        y = ay + row * row_h
        nf = SANS_B(10)
        tag = f"{num}."
        d.text((x, y), tag, font=nf, fill=RED)
        tw = col_w - nf.getlength(tag) - 6
        tf = fit_size(d, text, 10, 8, tw)
        d.text((x + nf.getlength(tag) + 4, y), text, font=tf, fill=(40, 45, 55))

    # ---- footer: DATE CHECK + sources --------------------------------------
    fy2 = ay + 11 * row_h + 8
    d.rectangle([M, fy2, W - M, fy2 + 30], fill=AMBER_BG, outline=GOLD)
    dl = wrap_text(DATE_CHECK, SANS(9), CW - 16)
    for j, ln in enumerate(dl[:2]):
        d.text((M + 8, fy2 + 3 + j * 12), ln, font=SANS(9), fill=(90, 60, 0))
    sy = fy2 + 33
    sl = wrap_text(SOURCES, SANS(9), CW)
    for j, ln in enumerate(sl[:2]):
        d.text((M, sy + j * 11), ln, font=SANS(9), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size} bytes)")
