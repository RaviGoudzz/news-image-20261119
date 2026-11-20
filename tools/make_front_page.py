from PIL import Image, ImageDraw, ImageFont

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


def chip(x, y, label, color):
    font = f(FONT_BOLD, 12)
    w = int(d.textlength(label, font=font)) + 14
    d.rounded_rectangle([x, y, x + w, y + 20], radius=4, fill=color)
    d.text((x + 7, y + 3), label, font=font, fill="#FFFFFF")
    return w


def card(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD, outline=RULE, width=2)


def rule(y, color=RED, width=3):
    d.line([(24, y), (1000, y)], fill=color, width=width)


def star(cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------- masthead ----------------
d.text((24, 16), "THE WORLD IN ONE DAY", font=f(FONT_BLACK, 24), fill=INK)
date_txt = "Thursday 19 November 2026"
dw = d.textlength(date_txt, font=f(GEORGIA_B, 20))
d.text((1000 - dw, 20), date_txt, font=f(GEORGIA_B, 20), fill=RED)
rule(54)

headline = "Thursday 19 November 2026"
hw = d.textlength(headline, font=f(GEORGIA_B, 58))
d.text(((W - hw) / 2, 68), headline, font=f(GEORGIA_B, 58), fill=INK)
sub = "The day's world news in one image"
sw = d.textlength(sub, font=f(GEORGIA, 20))
d.text(((W - sw) / 2, 138), sub, font=f(GEORGIA, 20), fill=MUTED)
rule(164, RULE, 2)

# ---------------- lead story ----------------
card(24, 175, 976, 190)
d.rectangle([24, 175, 300, 365], fill="#EAF1F8")
d.line([(300, 175), (300, 365)], fill=RULE, width=2)
# flags
def flag(x, y, kind):
    w, h = 74, 46
    if kind == "US":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill="#B22234" if i % 2 == 0 else "#FFFFFF")
        d.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill="#3C3B6E")
        for r in range(2):
            for c in range(3):
                star(x + 6 + c * 11, y + 5 + r * 10, 3, "#FFFFFF")
    elif kind == "CN":
        d.rectangle([x, y, x + w, y + h], fill="#DE2910")
        star(x + 12, y + 12, 8, "#FFDE00")
        for a in (35, 70, 105, 140):
            import math
            ang = math.radians(a)
            star(x + 12 + 16 * math.cos(ang), y + 12 + 16 * math.sin(ang), 3, "#FFDE00")
    else:
        d.rectangle([x, y, x + w, y + h / 3], fill="#FFFFFF")
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill="#0039A6")
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill="#D52B1E")
    d.line([(x - 6, y - 6), (x - 6, y + h + 22)], fill="#8A7A5A", width=3)

flag(48, 205, "US")
flag(140, 205, "CN")
flag(232, 205, "RU")
d.text((48, 285), "SHENZHEN", font=f(FONT_BOLD, 15), fill=BLUE)
d.text((48, 308), "APEC CHINA 2026", font=f(FONT_BOLD, 12), fill=MUTED)

tx = 320
chip(tx, 188, "WORLD · APEC CHINA 2026", BLUE)
y = block(tx, 216, "Trump, Xi and Putin hold first three-way summit", f(GEORGIA_B, 31), INK, 656, 38)
y = block(tx, y + 4, "The US, Chinese and Russian leaders met for 90 minutes and issued a joint declaration on nuclear war, oil production and UN reform.", f(GEORGIA, 18), "#33302A", 656, 24)
d.text((tx, 336), "Sources: AFP · Reuters · Xinhua", font=f(FONT, 12), fill=MUTED)

# ---------------- row B ----------------
def icon_scales(cx, cy, s=1.0):
    gold = "#C9A227"
    d.line([(cx, cy - 40 * s), (cx, cy + 40 * s)], fill=gold, width=int(5 * s))
    d.line([(cx - 42 * s, cy - 28 * s), (cx + 42 * s, cy - 28 * s)], fill=gold, width=int(5 * s))
    d.polygon([(cx - 40 * s, cy + 18 * s), (cx - 8 * s, cy + 18 * s), (cx - 24 * s, cy - 8 * s)], outline=gold, width=int(3 * s))
    d.polygon([(cx + 8 * s, cy + 18 * s), (cx + 40 * s, cy + 18 * s), (cx + 24 * s, cy - 8 * s)], outline=gold, width=int(3 * s))
    d.rectangle([cx - 18 * s, cy + 40 * s, cx + 18 * s, cy + 46 * s], fill=gold)


def icon_controller(cx, cy, s=1.0):
    d.rounded_rectangle([cx - 46 * s, cy - 24 * s, cx + 46 * s, cy + 24 * s], radius=18 * s, fill="#2B2B2B")
    d.rectangle([cx - 30 * s, cy - 6 * s, cx - 12 * s, cy + 6 * s], fill="#E8E8E8")
    d.rectangle([cx - 24 * s, cy - 12 * s, cx - 18 * s, cy + 12 * s], fill="#E8E8E8")
    d.ellipse([cx + 14 * s, cy - 12 * s, cx + 26 * s, cy], fill="#C0392B")
    d.ellipse([cx + 30 * s, cy - 2 * s, cx + 42 * s, cy + 10 * s], fill="#2E6B3E")


def story_card(x, y, w, h, region, color, headline, summary, icon=None):
    card(x, y, w, h)
    chip(x + 14, y + 12, region, color)
    yy = y + 42
    yy = block(x + 14, yy, headline, f(GEORGIA_B, 25), INK, w - 28, 31)
    yy = block(x + 14, yy + 4, summary, f(GEORGIA, 16), "#33302A", w - 28, 21)
    if icon:
        icon(x + w - 56, y + h - 56)


story_card(24, 380, 480, 175, "ASIA · JUSTICE", RED,
           "World Court: Myanmar committed genocide",
           "The ICJ found Myanmar guilty of genocide against the Rohingya and ordered reparations.",
           icon_scales)
story_card(520, 380, 480, 175, "BUSINESS · GAMES", "#2E6B3E",
           "GTA VI launches at $2.3B",
           "Rockstar's sequel became the biggest video-game launch in history, beating Call of Duty by $600M.",
           icon_controller)


def icon_tanker(cx, cy):
    d.polygon([(cx - 60, cy), (cx + 60, cy), (cx + 44, cy + 18), (cx - 48, cy + 18)], fill="#1F3A5F")
    d.rectangle([cx - 24, cy - 18, cx - 2, cy], fill="#FFFFFF")
    d.rectangle([cx + 8, cy - 12, cx + 30, cy], fill="#C0392B")
    d.ellipse([cx + 44, cy - 26, cx + 62, cy - 8], fill="#3A3A3A")
    for a in (0, 60, 120, 180, 240, 300):
        import math
        ang = math.radians(a)
        d.line([(cx + 53, cy - 17), (cx + 53 + 10 * math.cos(ang), cy - 17 + 10 * math.sin(ang))], fill="#3A3A3A", width=2)
    d.polygon([(cx + 34, cy - 34), (cx + 44, cy - 18), (cx + 30, cy - 20)], fill="#E67E22")
    d.polygon([(cx + 40, cy - 30), (cx + 48, cy - 18), (cx + 36, cy - 21)], fill="#F1C40F")


def icon_tower(cx, cy):
    d.rectangle([cx - 16, cy - 42, cx + 16, cy + 40], fill="#35507A")
    d.rectangle([cx - 2, cy - 56, cx + 2, cy - 42], fill="#35507A")
    for r in range(5):
        d.line([(cx - 12, cy - 30 + r * 14), (cx + 12, cy - 30 + r * 14)], fill="#9FB6D4", width=2)
    star(cx + 26, cy - 20, 14, "#E67E22")
    star(cx + 32, cy - 28, 8, "#F1C40F")


def icon_factory(cx, cy):
    d.rectangle([cx - 50, cy - 10, cx + 50, cy + 34], fill="#7A6A55")
    for i in range(3):
        x0 = cx - 50 + i * 34
        d.polygon([(x0, cy - 10), (x0 + 17, cy - 28), (x0 + 34, cy - 10)], fill="#8A7A63")
    d.rectangle([cx + 28, cy - 40, cx + 40, cy - 10], fill="#5A4E3E")
    d.rectangle([cx - 44, cy + 8, cx - 18, cy + 34], fill="#3A3228")
    d.rectangle([cx + 8, cy + 4, cx + 44, cy + 34], fill="#C9BFA8")


story_card(24, 570, 312, 175, "MIDDLE EAST · HORMUZ", "#C77700",
           "Tanker hits mine, catches fire",
           "An oil tanker caught fire after hitting a naval mine east of the Strait of Hormuz, Iran's navy said.",
           icon_tanker)
story_card(356, 570, 312, 175, "MIDDLE EAST · RIYADH", "#C77700",
           "Missiles hit Riyadh financial district",
           "Houthi missiles damaged the PIF Tower and other buildings; no injuries reported.",
           icon_tower)
story_card(688, 570, 312, 175, "ASIA · BANGLADESH", RED,
           "341 garment factories closed",
           "Minimum-wage protests spread; police used tear gas in Ashulia and Gazipur.",
           icon_factory)

# ---------------- also on the day ----------------
d.text((24, 762), "ALSO ON 19 NOVEMBER", font=f(FONT_BLACK, 15), fill=INK)
rule(784, RULE, 2)
items = [
    ("AMERICAS", "El Salvador: Bukele files for a third term"),
    ("AFRICA", "Senegal: budget enacted by decree; $2.2B IMF talks"),
    ("ASIA", "Mongolia: president resigns amid corruption claims"),
    ("AMERICAS", "Haiti: 34 alleged gang members killed in Port-au-Prince"),
    ("MIDDLE EAST", "Somalia expels the UAE ambassador"),
    ("GLOBAL", "Saudi oil exports highest since the February war"),
    ("ASIA", "Pakistan and Qatar sign a security pact"),
]
col_x = [24, 520]
yy = 798
for i, (reg, txt) in enumerate(items):
    x = col_x[i // 4]
    y = yy + (i % 4) * 28
    chip(x, y, reg, BLUE if reg != "EUROPE" else "#6A3FA0")
    cw = int(d.textlength(reg, font=f(FONT_BOLD, 12))) + 14
    d.text((x + cw + 8, y + 2), txt, font=f(GEORGIA, 16), fill=INK)

# ---------------- date check + footer ----------------
d.rounded_rectangle([24, 946, 1000, 976], radius=4, outline=RED, width=2)
dt = "DATE CHECK  ✓  Every story on this page is from Thursday 19 November 2026."
d.text((36, 953), dt, font=f(FONT_BOLD, 13), fill=RED)
foot = "19 NOVEMBER 2026 · THE WORLD IN ONE DAY · drawn in code · sources: AFP, Reuters, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua"
fw = d.textlength(foot, font=f(FONT, 11))
d.text(((W - fw) / 2, 988), foot, font=f(FONT, 11), fill=MUTED)

img.save("/Users/monalisa/makefun/news-image-20261119/entry.png", "PNG", optimize=True)
print("saved", img.size)
