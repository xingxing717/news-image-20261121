#!/usr/bin/env python3
"""Render the 21 November 2026 front page: THE WORLD TODAY.

Pure Pillow drawing, no network, no clock, no randomness. Every story
below happened, or was first reported, on Saturday 21 November 2026,
verified against same-day reporting (Reuters, AP, BBC, Xinhua, USGS,
UPI, Guardian, Yonhap, France 24, and others).

Run:  python3 render.py            -> writes entry.png (1024x1024)
"""
import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = Path(__file__).resolve().parent

PAPER = (247, 242, 232)
CARD = (255, 253, 247)
INK = (20, 20, 20)
BODY = (52, 50, 46)
GREY = (105, 100, 92)
RULE = (60, 55, 48)
HAIR = (214, 208, 196)
RED = (178, 32, 44)
DARKRED = (140, 20, 30)
BLUE = (28, 62, 110)
TEAL = (14, 92, 86)
GOLD = (176, 124, 20)
GREEN = (34, 96, 52)
PURPLE = (84, 52, 110)

SERIF_B = str(BASE / "fonts" / "DejaVuSerif-Bold.ttf")
SANS = str(BASE / "fonts" / "DejaVuSans.ttf")
SANS_B = str(BASE / "fonts" / "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tw(d, text, fnt):
    return d.textlength(text, font=fnt)


# ------------------------------------------------------------------ stories
# Each tuple: (headline, summary, source). All dated 21 November 2026.
LEAD = {
    "kicker": "THE GULF WAR WIDENS  •  MANAMA, BAHRAIN",
    "headline": "IRAN HITS TWO US BASES IN BAHRAIN AS GULF WAR WIDENS",
    "deck": ("The Revolutionary Guards say missiles and drones hit US positions "
             "at al-Riffa and Awali. Bahrain reports a civilian industrial site "
             "ablaze, no injuries, and air defences intercepting more attacks "
             "— the fourth Iranian strike on the kingdom in nine days."),
    "numbers": "2 BASES NAMED  •  1 SITE ABLAZE  •  0 INJURIES  •  4TH STRIKE IN 9 DAYS",
    "source": "REUTERS / XINHUA",
}

SECTIONS = [
    ("MIDDLE EAST & THE GULF", RED, "flame", [
        ("SAUDI INTERCEPTS 3 HOUTHI MISSILES",
         "Three missiles aimed at Riyadh are shot down on a third straight night of alerts.",
         "REUTERS"),
        ("ISRAELI STRIKE KILLS 3 IN GAZA",
         "A food truck is hit in Gaza City; Israel says the dead were Islamic Jihad members.",
         "AL JAZEERA"),
        ("BASRA POWER FIRE KILLS FOUR",
         "A blaze at the Hartha power station injures 35 and strains Iraq's power supply.",
         "REUTERS"),
        ("OIL STEADY AS GULF ATTACKS GO ON",
         "Brent falls 5% on the week to $91 as Gulf flows recover and tanker attacks continue.",
         "OILPRICE"),
        ("GULF ECONOMIES SINK IN WAR",
         "Qatar contracts sharply as the war and the Hormuz disruption drag the region down.",
         "LA NACION"),
    ]),
    ("EUROPE & THE WAR", BLUE, "star", [
        ("MISSILE HITS ZELENSKY'S HOMETOWN",
         "A Russian missile strikes Kryvyi Rih; a 7-year-old boy is among two killed, 60 hurt.",
         "AL JAZEERA"),
        ("DENMARK EXPELS RUSSIAN DIPLOMAT",
         "The defence attache is expelled over an alleged plot to kill rapper Kyivstoner.",
         "BBC"),
        ("COST-OF-LIVING PROTESTS MARCH ON",
         "Thousands march in France and Portugal; 144 are arrested in France on a sixth Saturday.",
         "FRANCE 24"),
        ("POLICE JAILED OVER RACIST BEATING",
         "Three Paris officers get five years each for the 2020 beating of producer Michel Zecler.",
         "BBC"),
        ("VILLEPIN TO RUN FOR PRESIDENT",
         "Former PM Dominique de Villepin announces his candidacy, citing France's 'degradation'.",
         "FRANCE 24"),
    ]),
    ("THE AMERICAS", GREEN, "dome", [
        ("MEXICO CAPTURES CARTEL KINGPIN",
         "FBI most-wanted Fausto Isidro Meza Flores is seized in Sinaloa; 11 die in the violence after.",
         "BBC"),
        ("TRUMP THREATENS DATA-CENTRE TAX",
         "Firms building AI data centres abroad face a 'tremendous tax', the president says.",
         "BBC"),
        ("FBI CRIME DATABASE 'HACKED'",
         "Police records system is reportedly breached, the second major hack in two months.",
         "BBC"),
        ("US CHILD DIES OF MEASLES",
         "Virginia reports its first measles death of 2026 as the US loses elimination status.",
         "GUARDIAN"),
        ("BOLSONARO IN INTENSIVE CARE",
         "Brazil's ex-president is stable in Brasilia with a bowel obstruction; surgery is weighed.",
         "AL JAZEERA"),
    ]),
    ("ASIA-PACIFIC", PURPLE, "globe", [
        ("TRUMP DEFENDS PUTIN FRIENDSHIP",
         "After the Shenzhen summit, Zelensky calls Putin a killer; nuclear-risk talks are agreed.",
         "BBC"),
        ("JAPAN 'LEFT OUT' OF SUMMIT",
         "Trump says Japan felt sidelined by the US-China-Russia talks; Takaichi gets a cool welcome.",
         "JAPAN TIMES"),
        ("SEOUL MOVES TO IMPEACH TOP JUDGE",
         "South Korea's ruling party prepares a motion against the Supreme Court chief justice.",
         "YONHAP"),
        ("NEPAL PM TO VISIT INDIA",
         "Balendra Shah's first foreign trip, 22-23 November, puts trade and links on the agenda.",
         "BBC"),
        ("MAGNITUDE 6.8 QUAKE OFF TIMOR",
         "A deep quake strikes 103 km off Lospalos at 09:42 UTC; no tsunami threat is issued.",
         "YONHAP"),
    ]),
    ("CLIMATE & DISASTERS", TEAL, "cyclone", [
        ("COP31 IN OVERTIME, STILL NO DEAL",
         "Nearly 200 nations deadlocked in Antalya as the draft drops all fossil-fuel wording.",
         "REUTERS"),
        ("MAGNITUDE 6.7 QUAKE SHAKES PERU",
         "A tremor strikes near Carhuamayo at 00:09 UTC, felt in Lima; no damage reported at first.",
         "USGS"),
        ("700,000 DISPLACED IN ETHIOPIA",
         "Conflict displaces hundreds of thousands in the south as troops mass on the Eritrea border.",
         "FRANCE 24"),
        ("US SELLS DEEP-SEA MINING LEASES",
         "First leases off American Samoa are sold days after a judge found wildlife law broken.",
         "EURONEWS"),
        ("KENYA STARTS DRILLING FOR OIL",
         "Onshore crude drilling begins in Turkana, starting the countdown to production.",
         "ALLAFRICA"),
    ]),
    ("MARKETS, TECH & SCIENCE", DARKRED, "chart", [
        ("AI SELL-OFF PUSHES STOCKS DOWN",
         "S&P 500 and Dow enter correction; the Nasdaq erases all its 2026 gains.",
         "UPI"),
        ("NVIDIA CHIEF OUSTED IN SCANDAL",
         "Jensen Huang is out; Trump says he discussed it with Xi as chip rules stay unchanged.",
         "CNBC"),
        ("YOUTUBE NEARS SCHOOLS PAYOUT",
         "A multibillion-dollar settlement over addiction claims nears completion in the US.",
         "STRAITS TIMES"),
        ("CERN SPOTS ULTRA-RARE DECAY",
         "Physicists report first evidence of an extremely rare particle decay at the LHC.",
         "PHYS.ORG"),
        ("MOSQUITOES CUT DENGUE IN BRAZIL",
         "Bacterium-carrying mosquitoes sharply cut dengue and chikungunya in children, a study finds.",
         "STRAITS TIMES"),
    ]),
]

ALSO = [
    ("ALCARAZ REACHES ATP FINAL",
     "Beats Shelton in three sets; faces Zverev on Sunday."),
    ("HARDEN PASSES KOBE WITH 51",
     "26th career 50-point game in a 128-119 Cavs win."),
    ("ENGLAND BEAT ALL BLACKS",
     "A wide-margin win at Twickenham."),
    ("COLTURI WINS FOR ALBANIA",
     "First alpine skiing World Cup win for Albania."),
    ("GTA VI MAKES $3.8 BILLION",
     "Biggest entertainment launch ever, in one day. (BBC)"),
    ("SPITTING IMAGE CREATOR DIES",
     "Peter Fluck, 85, dies at home in Cornwall. (BBC)"),
    ("UN WOMEN EX-CHIEF DIES AT 71",
     "Phumzile Mlambo-Ngcuka, South Africa's first woman deputy president."),
    ("SWIMMER CROSSES THE HORMUZ",
     "Lewis Pugh swims 15 km through the strait in three days."),
]

TICKER = ("IRAN HITS US BASES IN BAHRAIN  •  COP31: NO DEAL AS TALKS RUN INTO OVERTIME  •  "
          "SAUDI INTERCEPTS 3 HOUTHI MISSILES  •  PERU QUAKE 6.7  •  KRYVYI RIH MISSILE KILLS 2")


# ------------------------------------------------------------------ drawing
def draw_glyph(d, kind, cx, cy, color):
    """Small flat white glyph in a section header."""
    if kind == "flame":
        d.polygon([(cx, cy - 10), (cx + 7, cy + 2), (cx + 3, cy + 8),
                   (cx - 3, cy + 8), (cx - 7, cy + 2)], fill=color)
    elif kind == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = 10 if i % 2 == 0 else 4
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill=color)
    elif kind == "dome":
        d.pieslice([cx - 8, cy - 8, cx + 8, cy + 4], 180, 360, fill=color)
        d.rectangle([cx - 9, cy + 4, cx + 9, cy + 9], fill=color)
        d.line([cx - 10, cy + 9, cx + 10, cy + 9], fill=color, width=2)
    elif kind == "globe":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=color, width=2)
        d.ellipse([cx - 4, cy - 9, cx + 4, cy + 9], outline=color, width=1)
        d.line([cx - 9, cy, cx + 9, cy], fill=color, width=1)
    elif kind == "cyclone":
        for r in (9, 6, 3):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=color, width=2)
    elif kind == "chart":
        d.line([(cx - 10, cy + 7), (cx - 3, cy + 1), (cx + 2, cy + 4),
                (cx + 10, cy - 8)], fill=color, width=2)
        d.polygon([(cx + 10, cy - 8), (cx + 4, cy - 8), (cx + 10, cy - 2)],
                  fill=color)


def draw_gulf_scene(d, x, y, w, h):
    """Flat vector scene: night over the Gulf — missiles, interceptors,
    a naval base skyline, fire on the water."""
    # night sky
    d.rectangle([x, y, x + w, y + h], fill=(18, 30, 52))
    for sx, sy, sr in [(30, 18, 2), (90, 10, 1), (150, 26, 2), (210, 12, 1),
                       (270, 22, 2), (330, 14, 1), (60, 40, 1), (180, 44, 1),
                       (250, 38, 2), (350, 44, 1)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(220, 225, 235))
    # moon
    d.ellipse([x + w - 56, y + 10, x + w - 26, y + 40], fill=(238, 228, 190))
    d.ellipse([x + w - 50, y + 16, x + w - 42, y + 24], fill=(214, 202, 160))
    # distant skyline with radar domes
    for bx, bw, bh in [(10, 30, 34), (46, 22, 48), (74, 36, 28), (250, 26, 40),
                       (282, 20, 30), (308, 34, 44)]:
        d.rectangle([x + bx, y + 96 - bh, x + bx + bw, y + 96],
                    fill=(38, 52, 74))
    for dx, dy in [(57, 40), (295, 48)]:
        d.rectangle([x + dx - 1, y + dy, x + dx + 1, y + 96], fill=(38, 52, 74))
        d.pieslice([x + dx - 9, y + dy - 9, x + dx + 9, y + dy + 9],
                   180, 360, fill=(38, 52, 74))
    # lit windows
    for wx, wy in [(16, 74), (30, 82), (52, 60), (80, 78), (256, 66),
                   (288, 74), (314, 62), (330, 78)]:
        d.rectangle([x + wx, y + wy, x + wx + 4, y + wy + 5],
                    fill=(240, 200, 90))
    # sea
    d.rectangle([x, y + 96, x + w, y + h], fill=(34, 68, 100))
    for wy in (112, 136, 162, 184):
        d.line([(x + 8, y + wy), (x + 60, y + wy), (x + 90, y + wy + 3),
                (x + 150, y + wy)], fill=(70, 110, 140), width=2)
        d.line([(x + 210, y + wy + 2), (x + 280, y + wy),
                (x + 330, y + wy + 3), (x + w - 8, y + wy)],
               fill=(70, 110, 140), width=2)
    # missile trails arcing down from the sky
    for (x1, y1, x2, y2) in [(40, 8, 120, 92), (200, 4, 260, 88),
                             (320, 10, 300, 96)]:
        d.line([(x + x1, y + y1), (x + x2, y + y2)], fill=(250, 180, 80),
               width=3)
        d.line([(x + x1, y + y1), (x + x2, y + y2)], fill=(255, 220, 130),
               width=1)
    # interceptor arcs rising to meet them
    for (x1, y1, x2, y2) in [(100, 96, 150, 52), (280, 96, 240, 58)]:
        d.arc([x + min(x1, x2) - 10, y + min(y1, y2) - 6,
               x + max(x1, x2) + 10, y + max(y1, y2) + 6],
              200, 340, fill=(160, 210, 240), width=2)
    # bursts where missiles are hit
    for ex, ey, r in [(120, 92, 24), (258, 88, 26)]:
        pts = []
        for i in range(12):
            ang = i * math.pi / 6
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((x + ex + rr * math.cos(ang),
                        y + ey + rr * math.sin(ang)))
        d.polygon(pts, fill=(232, 120, 30))
        d.ellipse([x + ex - 9, y + ey - 9, x + ex + 9, y + ey + 9],
                  fill=(250, 210, 60))
    # fire glow on the water under the base
    d.ellipse([x + 40, y + 150, x + 130, y + 186], fill=(200, 90, 30))
    d.ellipse([x + 58, y + 158, x + 112, y + 180], fill=(240, 160, 60))
    # smoke puffs
    for sx, sy, sr in [(150, 70, 11), (168, 60, 8), (286, 66, 12),
                       (304, 56, 8)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(110, 112, 118))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def draw_story(d, x, y, width, headline, summary, source, max_bottom):
    """One story block; returns y after the block."""
    hf = font(SANS_B, 12)
    sf = font(SANS, 10)
    srcf = font(SANS_B, 8)
    for ln in wrap(d, headline, hf, width)[:2]:
        d.text((x, y), ln, font=hf, fill=INK)
        y += 15
    slines = wrap(d, summary, sf, width - 62)[:2]
    for i, ln in enumerate(slines):
        d.text((x, y), ln, font=sf, fill=BODY)
        if i == len(slines) - 1:
            sx = x + tw(d, ln, sf) + 5
            d.text((sx, y + 1), "· " + source, font=srcf, fill=GREY)
        y += 13
    if y > max_bottom:
        print(f"OVERFLOW in story: {headline[:40]}", file=sys.stderr)
    return y + 1


# ------------------------------------------------------------------ by the numbers
# Four figures drawn from stories already on this page: the Ethiopia
# displacement, the Timor-Leste quake, the GTA VI launch and Harden's
# 51-point night. The strip sits in the empty band beneath the lead
# story, above the section grid.
NUMBERS = [
    ("700,000", "DISPLACED IN ETHIOPIA", RED),
    ("M6.8", "QUAKE OFF TIMOR", PURPLE),
    ("$3.8BN", "GTA VI LAUNCH DAY", DARKRED),
    ("51 PTS", "HARDEN PASSES KOBE", GREEN),
]


def draw_numbers_strip(d, x, y, w):
    """'BY THE NUMBERS' strip: red header label plus four small stat
    boxes, each with a big figure over a small caption."""
    hf = font(SANS_B, 10)
    nf = font(SANS_B, 12)
    lf = font(SANS, 8)
    d.rectangle([x, y + 8, x + 8, y + 16], fill=RED)
    d.text((x + 12, y + 7), "BY THE NUMBERS", font=hf, fill=RED)
    hx = x + 12 + tw(d, "BY THE NUMBERS", hf) + 12
    gap = 6
    bw = (x + w - hx - gap * 3) // 4
    bh = 24
    for i, (num, label, color) in enumerate(NUMBERS):
        bx = hx + i * (bw + gap)
        d.rectangle([bx, y, bx + bw, y + bh], fill=CARD, outline=RULE,
                    width=1)
        d.rectangle([bx, y, bx + 3, y + bh], fill=color)
        d.text((bx + 9, y + 3), num, font=nf, fill=INK)
        d.text((bx + 9, y + 15), label, font=lf, fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((W // 2, 16), "ONE DAY  •  ONE PAGE  •  THE WHOLE WORLD",
           font=font(SANS_B, 11), fill=GREY, anchor="ma")
    d.text((W // 2, 34), "THE WORLD TODAY", font=font(SERIF_B, 56),
           fill=INK, anchor="ma")
    d.line([16, 100, 1008, 100], fill=RULE, width=2)
    d.line([16, 104, 1008, 104], fill=RULE, width=1)
    d.text((16, 110), "SATURDAY 21 NOVEMBER 2026", font=font(SANS_B, 16),
           fill=RED)
    d.text((1008, 110), "39 STORIES  •  7 REGIONS", font=font(SANS_B, 13),
           fill=INK, anchor="ra")

    # ---- ticker
    d.rectangle([16, 134, 1008, 160], fill=DARKRED)
    tf = font(SANS_B, 12)
    while tw(d, TICKER, tf) > 976 and tf.size > 9:
        tf = font(SANS_B, tf.size - 1)
    d.text((W // 2, 140), TICKER, font=tf, fill=(255, 255, 255), anchor="ma")

    # ---- lead story
    lx, ly, lw = 16, 170, 592
    d.text((lx, ly), LEAD["kicker"], font=font(SANS_B, 11), fill=RED)
    y = ly + 20
    for ln in wrap(d, LEAD["headline"], font(SERIF_B, 29), lw):
        d.text((lx, y), ln, font=font(SERIF_B, 29), fill=INK)
        y += 34
    y += 4
    for ln in wrap(d, LEAD["deck"], font(SANS, 13), lw):
        d.text((lx, y), ln, font=font(SANS, 13), fill=BODY)
        y += 17
    y += 6
    d.text((lx, y), LEAD["numbers"], font=font(SANS_B, 12), fill=BLUE)
    y += 20
    d.text((lx, y), "SOURCE: " + LEAD["source"], font=font(SANS_B, 9),
           fill=GREY)
    draw_gulf_scene(d, 624, 170, 384, 196)

    draw_numbers_strip(d, 16, 349, 592)

    # ---- section grid: 3 cols x 2 rows
    gx, gy = 16, 374
    pw, ph, gap = 325, 272, 8
    for idx, (title, color, glyph, stories) in enumerate(SECTIONS):
        col, row = idx % 3, idx // 3
        px = gx + col * (pw + gap)
        py = gy + row * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=CARD, outline=RULE,
                    width=1)
        d.rectangle([px, py, px + pw, py + 28], fill=color)
        draw_glyph(d, glyph, px + 16, py + 14, (255, 255, 255))
        d.text((px + 30, py + 7), title, font=font(SANS_B, 13),
               fill=(255, 255, 255))
        y = py + 36
        for i, (h, s, src) in enumerate(stories):
            y = draw_story(d, px + 10, y, pw - 20, h, s, src, py + ph - 6)
            if i < len(stories) - 1:
                d.line([px + 10, y + 1, px + pw - 10, y + 1], fill=HAIR,
                       width=1)
                y += 2

    # ---- also today band
    ay = 934
    d.rectangle([16, ay, 1008, ay + 66], fill=CARD, outline=RULE, width=1)
    d.rectangle([16, ay, 1008, ay + 20], fill=INK)
    d.text((26, ay + 4), "ALSO TODAY", font=font(SANS_B, 11),
           fill=(255, 255, 255))
    d.text((1008 - 10, ay + 4), "SPORT  •  CULTURE  •  SCIENCE",
           font=font(SANS_B, 10), fill=(200, 200, 200), anchor="ra")
    colw = 992 / 4
    for i, (h, s) in enumerate(ALSO):
        col, row = i % 4, i // 4
        ax = 26 + col * colw
        ayy = ay + 22 + row * 20
        hf = font(SANS_B, 9)
        sf = font(SANS, 9)
        avail = colw - 14
        h2 = h
        while tw(d, h2, hf) > avail and len(h2) > 4:
            h2 = h2[:-2]
        if h2 != h:
            h2 = h2.rstrip() + "…"
        d.text((ax, ayy), h2, font=hf, fill=INK)
        s2 = s
        while tw(d, s2, sf) > avail and len(s2) > 4:
            s2 = s2[:-2]
        if s2 != s:
            s2 = s2.rstrip() + "…"
        d.text((ax, ayy + 10), s2, font=sf, fill=BODY)

    # ---- footer
    d.line([16, 1006, 1008, 1006], fill=RULE, width=1)
    d.text((W // 2, 1011),
           "SOURCES: REUTERS  •  AP  •  BBC  •  XINHUA  •  USGS  •  UPI  •  GUARDIAN  •  YONHAP  •  FRANCE 24  —  ALL STORIES HAPPENED OR WERE FIRST REPORTED ON SATURDAY 21 NOVEMBER 2026",
           font=font(SANS, 9), fill=GREY, anchor="ma")
    return img


def main():
    out = Path(os.environ.get("RENDER_OUT",
                              str(BASE / "entry.png")))
    img = render()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
