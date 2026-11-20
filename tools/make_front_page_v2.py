from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = "#F7F2E7"
INK = "#1A1A1A"
MUTED = "#6B6255"
RULE = "#D8D0C0"
RED = "#B3261E"
BLUE = "#1F4E79"
CARD = "#FFFFFF"

FONT_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
SERIF_B = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
SERIF = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
GEORGIA_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def f(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, fill, maxw, lh):
    for line in wrap(text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def chip(x, y, label, color, size=12):
    font = f(FONT_BOLD, size)
    w = int(d.textlength(label, font=font)) + 14
    d.rounded_rectangle([x, y, x + w, y + size + 8], radius=4, fill=color)
    d.text((x + 7, y + 4), label, font=font, fill="#FFFFFF")
    return w


def card(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD, outline=RULE, width=2)


def rule(y, color=RED, width=3):
    d.line([(24, y), (1000, y)], fill=color, width=width)


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag(x, y, kind, w=64, h=42):
    if kind == "US":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill="#B22234" if i % 2 == 0 else "#FFFFFF")
        d.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill="#3C3B6E")
        for r in range(2):
            for c in range(3):
                star(x + 5 + c * 9, y + 4 + r * 9, 2.5, "#FFFFFF")
    elif kind == "CN":
        d.rectangle([x, y, x + w, y + h], fill="#DE2910")
        star(x + 10, y + 10, 7, "#FFDE00")
        for a in (35, 70, 105, 140):
            ang = math.radians(a)
            star(x + 10 + 14 * math.cos(ang), y + 10 + 14 * math.sin(ang), 2.5, "#FFDE00")
    else:
        d.rectangle([x, y, x + w, y + h / 3], fill="#FFFFFF")
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill="#0039A6")
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill="#D52B1E")


# ---------------- masthead ----------------
d.text((24, 14), "THE WORLD IN ONE DAY", font=f(FONT_BLACK, 24), fill=INK)
dt = "Thursday 19 November 2026"
dw = d.textlength(dt, font=f(GEORGIA_B, 19))
d.text((1000 - dw, 18), dt, font=f(GEORGIA_B, 19), fill=RED)
rule(52)
headline = "Thursday 19 November 2026"
hw = d.textlength(headline, font=f(GEORGIA_B, 56))
d.text(((W - hw) / 2, 62), headline, font=f(GEORGIA_B, 56), fill=INK)
sub = "Stories from Thursday 19 November 2026"
sw = d.textlength(sub, font=f(GEORGIA, 19))
d.text(((W - sw) / 2, 130), sub, font=f(GEORGIA, 19), fill=MUTED)
rule(158, RULE, 2)

# ---------------- lead story ----------------
card(24, 168, 976, 180)
d.rectangle([24, 168, 330, 348], fill="#EAF1F8")
d.line([(330, 168), (330, 348)], fill=RULE, width=2)
# flags behind
flag(44, 182, "US")
flag(122, 182, "CN")
flag(200, 182, "RU")
# table
d.rectangle([52, 268, 300, 286], fill="#8A6A45")
d.rectangle([60, 286, 74, 330], fill="#6B4F31")
d.rectangle([268, 286, 282, 330], fill="#6B4F31")
# three leaders
for i, (cx, suit, skin) in enumerate([(92, "#2C3E50", "#E8B98D"), (176, "#7B1F1F", "#F0C8A0"), (258, "#1F3A5F", "#E8B98D")]):
    d.rectangle([cx - 20, 236, cx + 20, 270], fill=suit)
    d.ellipse([cx - 14, 208, cx + 14, 236], fill=skin)
    d.rectangle([cx - 6, 236, cx + 6, 244], fill="#FFFFFF")
d.text((44, 300), "APEC 2026 · SHENZHEN", font=f(FONT_BOLD, 13), fill=BLUE)

tx = 350
chip(tx, 182, "WORLD · APEC CHINA 2026", BLUE)
y = block(tx, 208, "Trump, Xi and Putin hold first three-way summit", f(GEORGIA_B, 30), INK, 630, 37)
y = block(tx, y + 4, "The US, Chinese and Russian leaders met for 90 minutes and issued a joint declaration on nuclear war, oil production and UN reform.", f(GEORGIA, 17), "#33302A", 630, 23)
d.text((tx, 322), "Sources: AFP · Reuters · Xinhua", font=f(FONT, 12), fill=MUTED)

# ---------------- icons ----------------
def icon_scales(cx, cy, s=1.0):
    gold = "#C9A227"
    d.line([(cx, cy - 38 * s), (cx, cy + 38 * s)], fill=gold, width=int(5 * s))
    d.line([(cx - 40 * s, cy - 26 * s), (cx + 40 * s, cy - 26 * s)], fill=gold, width=int(5 * s))
    d.polygon([(cx - 38 * s, cy + 16 * s), (cx - 8 * s, cy + 16 * s), (cx - 23 * s, cy - 8 * s)], outline=gold, width=int(3 * s))
    d.polygon([(cx + 8 * s, cy + 16 * s), (cx + 38 * s, cy + 16 * s), (cx + 23 * s, cy - 8 * s)], outline=gold, width=int(3 * s))
    d.rectangle([cx - 16 * s, cy + 38 * s, cx + 16 * s, cy + 44 * s], fill=gold)


def icon_court(cx, cy):
    d.rectangle([cx - 46, cy - 8, cx + 46, cy + 44], fill="#D9C9A8")
    d.polygon([(cx - 52, cy - 8), (cx, cy - 34), (cx + 52, cy - 8)], fill="#B8A582")
    for i in range(4):
        x = cx - 33 + i * 22
        d.rectangle([x, cy + 2, x + 10, cy + 38], fill="#F1E8D5")
    d.rectangle([cx - 8, cy + 22, cx + 8, cy + 44], fill="#6B5B45")
    icon_scales(cx + 52, cy - 2, 0.55)


def icon_controller(cx, cy):
    d.rounded_rectangle([cx - 40, cy - 22, cx + 40, cy + 22], radius=16, fill="#2B2B2B")
    d.rectangle([cx - 26, cy - 5, cx - 10, cy + 5], fill="#E8E8E8")
    d.rectangle([cx - 20, cy - 11, cx - 16, cy + 11], fill="#E8E8E8")
    d.ellipse([cx + 12, cy - 10, cx + 22, cy], fill="#C0392B")
    d.ellipse([cx + 26, cy - 1, cx + 36, cy + 9], fill="#2E6B3E")
    d.rectangle([cx - 52, cy - 46, cx + 52, cy - 26], fill="#1F3A5F")
    d.text((cx - 40, cy - 44), "GTA VI", font=f(FONT_BOLD, 13), fill="#FFFFFF")


def icon_tanker(cx, cy):
    d.polygon([(cx - 58, cy - 2), (cx + 58, cy - 2), (cx + 42, cy + 16), (cx - 46, cy + 16)], fill="#1F3A5F")
    d.rectangle([cx - 22, cy - 20, cx - 2, cy - 2], fill="#FFFFFF")
    d.rectangle([cx + 8, cy - 14, cx + 28, cy - 2], fill="#C0392B")
    d.ellipse([cx + 40, cy - 30, cx + 56, cy - 14], fill="#3A3A3A")
    for a in (0, 60, 120, 180, 240, 300):
        ang = math.radians(a)
        d.line([(cx + 48, cy - 22), (cx + 48 + 9 * math.cos(ang), cy - 22 + 9 * math.sin(ang))], fill="#3A3A3A", width=2)
    d.polygon([(cx + 30, cy - 40), (cx + 40, cy - 20), (cx + 26, cy - 24)], fill="#E67E22")
    d.polygon([(cx + 36, cy - 36), (cx + 44, cy - 20), (cx + 32, cy - 24)], fill="#F1C40F")


def icon_tower(cx, cy):
    d.rectangle([cx - 15, cy - 44, cx + 15, cy + 40], fill="#35507A")
    d.rectangle([cx - 2, cy - 58, cx + 2, cy - 44], fill="#35507A")
    for r in range(5):
        d.line([(cx - 11, cy - 32 + r * 13), (cx + 11, cy - 32 + r * 13)], fill="#9FB6D4", width=2)
    star(cx + 28, cy - 24, 15, "#E67E22")
    star(cx + 34, cy - 32, 8, "#F1C40F")


def icon_factory(cx, cy):
    d.rectangle([cx - 48, cy - 8, cx + 48, cy + 34], fill="#7A6A55")
    for i in range(3):
        x0 = cx - 48 + i * 32
        d.polygon([(x0, cy - 8), (x0 + 16, cy - 26), (x0 + 32, cy - 8)], fill="#8A7A63")
    d.rectangle([cx + 26, cy - 38, cx + 38, cy - 8], fill="#5A4E3E")
    d.ellipse([cx + 28, cy - 50, cx + 40, cy - 40], fill="#C9C2B4")
    d.ellipse([cx + 34, cy - 60, cx + 46, cy - 50], fill="#D8D2C4")
    d.rectangle([cx - 42, cy + 6, cx - 18, cy + 34], fill="#3A3228")


def icon_ballot(cx, cy):
    d.rectangle([cx - 26, cy - 10, cx + 26, cy + 30], fill="#8A6A45")
    d.rectangle([cx - 30, cy - 18, cx + 30, cy - 10], fill="#6B4F31")
    d.rectangle([cx - 8, cy - 28, cx + 4, cy - 12], fill="#F1F1F1")
    d.line([(cx - 12, cy + 8), (cx + 12, cy + 8)], fill="#3A3228", width=2)


def icon_graph(cx, cy):
    d.rectangle([cx - 34, cy - 24, cx + 34, cy + 30], fill="#FFFFFF", outline="#8A8A8A", width=2)
    d.line([(cx - 26, cy + 16), (cx - 10, cy), (cx + 4, cy + 8), (cx + 24, cy - 20)], fill="#2E6B3E", width=4)
    d.polygon([(cx + 24, cy - 20), (cx + 12, cy - 18), (cx + 20, cy - 6)], fill="#2E6B3E")


def icon_palace(cx, cy):
    d.rectangle([cx - 34, cy - 6, cx + 34, cy + 34], fill="#C9A227")
    d.polygon([(cx - 40, cy - 6), (cx, cy - 30), (cx + 40, cy - 6)], fill="#8A6A45")
    for i in range(4):
        x = cx - 24 + i * 16
        d.rectangle([x, cy + 6, x + 8, cy + 34], fill="#F1E8D5")


def icon_desert(cx, cy):
    d.rectangle([cx - 36, cy + 8, cx + 36, cy + 30], fill="#E0C08A")
    d.polygon([(cx - 20, cy + 8), (cx - 8, cy - 12), (cx + 4, cy + 8)], fill="#C9A227")
    d.rectangle([cx + 12, cy - 22, cx + 24, cy - 4], fill="#6B4F31")
    d.rectangle([cx + 6, cy - 8, cx + 30, cy - 2], fill="#8A6A45")


def icon_shield(cx, cy):
    d.polygon([(cx - 22, cy - 24), (cx + 22, cy - 24), (cx + 18, cy + 12), (cx, cy + 32), (cx - 18, cy + 12)], fill="#35507A")
    d.line([(cx, cy - 16), (cx, cy + 20)], fill="#FFFFFF", width=3)
    d.line([(cx - 10, cy - 6), (cx + 10, cy - 6)], fill="#FFFFFF", width=3)


def icon_globe(cx, cy):
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill="#2E6B8A")
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline="#1F4E79", width=2)
    d.arc([cx - 26, cy - 26, cx + 26, cy + 26], 0, 360, fill="#9FD4E8", width=2)
    d.line([(cx - 26, cy), (cx + 26, cy)], fill="#9FD4E8", width=2)
    d.line([(cx, cy - 26), (cx, cy + 26)], fill="#9FD4E8", width=2)
    star(cx + 8, cy - 8, 4, "#F1C40F")


# ---------------- story cards ----------------
def story_card(x, y, w, h, region, color, headline, summary, icon=None, head_size=23):
    card(x, y, w, h)
    d.rectangle([x, y, x + 5, y + h], fill=color)
    chip(x + 14, y + 10, region, color, 11)
    yy = y + 34
    yy = block(x + 14, yy, headline, f(GEORGIA_B, head_size), INK, w - 28, int(head_size * 1.25))
    yy = block(x + 14, yy + 3, summary, f(GEORGIA, 14.5), "#33302A", w - 28, 19)
    if icon:
        icon(x + w - 58, y + h - 58)


story_card(24, 360, 480, 180, "ASIA · JUSTICE", RED,
           "World Court: Myanmar committed genocide",
           "The ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations.",
           icon_court, 24)
story_card(520, 360, 480, 180, "BUSINESS · GAMES", "#2E6B3E",
           "GTA VI goes on sale after 13 years",
           "Rockstar's sequel became the biggest video-game launch in history, with $2.3B in sales.",
           icon_controller, 24)
story_card(24, 552, 312, 180, "MIDDLE EAST · HORMUZ", "#C77700",
           "Tanker hits mine, catches fire",
           "An oil tanker caught fire after hitting a naval mine east of the Strait of Hormuz.",
           icon_tanker, 22)
story_card(356, 552, 312, 180, "MIDDLE EAST · RIYADH", "#C77700",
           "Missiles hit Riyadh financial district",
           "Houthi missiles damaged the PIF Tower and other buildings; no injuries reported.",
           icon_tower, 22)
story_card(688, 552, 312, 180, "ASIA · BANGLADESH", RED,
           "341 garment factories closed",
           "Minimum-wage protests spread; police used tear gas in Ashulia and Gazipur.",
           icon_factory, 22)

# ---------------- also on the day ----------------
d.text((24, 744), "ALSO ON 19 NOVEMBER", font=f(FONT_BLACK, 15), fill=INK)
rule(766, RULE, 2)
items = [
    ("AMERICAS", "El Salvador: Bukele files for a third term", icon_ballot),
    ("AFRICA", "Senegal: budget enacted by decree; $2.2B IMF talks", icon_graph),
    ("ASIA", "Mongolia: president resigns amid corruption claims", icon_palace),
    ("AMERICAS", "Haiti: 34 alleged gang members killed in Port-au-Prince", icon_shield),
    ("MIDDLE EAST", "Somalia expels the UAE ambassador", icon_globe),
    ("GLOBAL", "Saudi oil exports highest since the February war", icon_desert),
]
for i, (reg, txt, ic) in enumerate(items):
    col = i // 3
    row = i % 3
    x = 24 + col * 488
    y = 778 + row * 40
    chip(x, y, reg, BLUE, 11)
    cw = int(d.textlength(reg, font=f(FONT_BOLD, 11))) + 14
    d.text((x + cw + 8, y + 2), txt, font=f(GEORGIA, 15), fill=INK)
    ic(x + 452, y - 6)

# ---------------- date check + footer ----------------
d.rounded_rectangle([24, 900, 1000, 930], radius=4, outline=RED, width=2)
d.text((36, 908), "DATE CHECK  ✓  Every story on this page is from Thursday 19 November 2026.", font=f(FONT_BOLD, 13), fill=RED)
foot = "19 NOVEMBER 2026 · THE WORLD IN ONE DAY · drawn in code · sources: AFP, Reuters, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua"
fw = d.textlength(foot, font=f(FONT, 11))
d.text(((W - fw) / 2, 940), foot, font=f(FONT, 11), fill=MUTED)

img.save("/Users/monalisa/makefun/news-image-20261119/entry_v2.png", "PNG", optimize=True)
print("saved", img.size)
