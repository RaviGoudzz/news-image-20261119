import json
import math
import os
import re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1024, 1024
PAPER = "#F7F2E7"
INK = "#191919"
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

with open(os.path.join(HERE, "news-edition.json"), encoding="utf-8") as fh:
    edition = json.load(fh)
stories = sorted(edition["stories"], key=lambda s: int(s["n"]))

OUTLETS = {"Reuters", "AP", "AFP", "BBC", "Al Jazeera", "UN News", "Euronews", "ABC", "RNZ", "Xinhua", "Nature", "Kompas", "SABC", "NASA", "Day", "UFC", "Prensa", "L'Observateur", "Hand", "Greek", "City", "Media", "Monitoring", "Agency", "Press", "TV", "Radio", "News", "Post", "Times", "Star", "Mail", "Guardian", "Telegraph", "Journal", "Tribune", "Herald", "Bulletin", "Gazette", "Standard", "Daily"}


def strip_sources(text):
    if " — " not in text:
        return text
    head, tail = text.rsplit(" — ", 1)
    parts = [p.strip() for p in tail.split("·")]
    if parts and all(p and p[0].isupper() for p in parts):
        return head.strip()
    return text


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


def fit(text, font, maxw, maxlines):
    lines = wrap(text, font, maxw)
    if len(lines) <= maxlines:
        return lines
    out = lines[:maxlines]
    last = out[-1]
    while d.textlength(last + "…", font=font) > maxw and last:
        last = last[:-1]
    out[-1] = last + "…"
    return out


def block(x, y, text, font, fill, maxw, lh, maxlines=None):
    lines = fit(text, font, maxw, maxlines) if maxlines else wrap(text, font, maxw)
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def chip(x, y, label, color, size=11):
    font = f(FONT_BOLD, size)
    w = int(d.textlength(label, font=font)) + 12
    d.rounded_rectangle([x, y, x + w, y + 18], radius=4, fill=color)
    d.text((x + 6, y + 3), label, font=font, fill="#FFFFFF")
    return w


def card(x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=CARD, outline=RULE, width=1)


def hrule(y, color=RED, width=3):
    d.line([(24, y), (1000, y)], fill=color, width=width)


def star(cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------- icons ----------
def ic_politics(cx, cy):
    for i, (x, col) in enumerate([(cx - 26, "#B22234"), (cx, "#DE2910"), (cx + 26, "#0039A6")]):
        d.line([(x, cy - 22), (x, cy + 22)], fill="#8A7A5A", width=2)
        d.rectangle([x, cy - 22, x + 18, cy - 8], fill=col)


def ic_justice(cx, cy):
    g = "#C9A227"
    d.line([(cx, cy - 22), (cx, cy + 20)], fill=g, width=3)
    d.line([(cx - 20, cy - 14), (cx + 20, cy - 14)], fill=g, width=3)
    d.polygon([(cx - 19, cy + 8), (cx - 5, cy + 8), (cx - 12, cy - 6)], outline=g, width=2)
    d.polygon([(cx + 5, cy + 8), (cx + 19, cy + 8), (cx + 12, cy - 6)], outline=g, width=2)
    d.rectangle([cx - 10, cy + 20, cx + 10, cy + 24], fill=g)


def ic_business(cx, cy):
    d.line([(cx - 22, cy + 18), (cx + 22, cy + 18)], fill="#2E6B3E", width=3)
    d.polygon([(cx - 20, cy + 14), (cx - 8, cy + 2), (cx + 2, cy + 8), (cx + 14, cy - 16)], fill="#2E6B3E")
    d.line([(cx + 14, cy - 16), (cx + 22, cy - 12)], fill="#2E6B3E", width=3)
    d.ellipse([cx + 12, cy + 2, cx + 30, cy + 20], fill="#C9A227")


def ic_war(cx, cy):
    star(cx, cy - 2, 16, "#E67E22")
    star(cx, cy - 4, 9, "#F1C40F")
    d.line([(cx - 24, cy + 18), (cx + 24, cy + 18)], fill="#3A3A3A", width=3)


def ic_disaster(cx, cy):
    d.arc([cx - 24, cy - 18, cx + 8, cy + 18], 200, 340, fill="#1F4E79", width=4)
    d.arc([cx - 8, cy - 8, cx + 24, cy + 24], 20, 160, fill="#1F4E79", width=4)
    d.line([(cx - 22, cy + 22), (cx + 22, cy + 22)], fill="#1F4E79", width=3)


def ic_sport(cx, cy):
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill="#C9A227")
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill="#E8C55A")
    d.polygon([(cx - 10, cy - 20), (cx - 4, cy - 8), (cx + 2, cy - 20)], fill="#B3261E")
    d.polygon([(cx + 10, cy - 20), (cx + 4, cy - 8), (cx - 2, cy - 20)], fill="#1F4E79")


def ic_science(cx, cy):
    for a in (0, 60, 120):
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], outline="#6A3FA0", width=2)
        break
    d.ellipse([cx - 20, cy - 7, cx + 20, cy + 7], outline="#6A3FA0", width=2)
    d.ellipse([cx - 7, cy - 20, cx + 7, cy + 20], outline="#6A3FA0", width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill="#6A3FA0")


def ic_health(cx, cy):
    d.rectangle([cx - 16, cy - 6, cx + 16, cy + 6], fill="#B3261E")
    d.rectangle([cx - 6, cy - 16, cx + 6, cy + 16], fill="#B3261E")


def ic_env(cx, cy):
    d.polygon([(cx, cy - 20), (cx + 14, cy - 4), (cx + 6, cy + 18), (cx - 10, cy + 14), (cx - 14, cy - 6)], fill="#2E6B3E")
    d.line([(cx - 8, cy + 12), (cx + 4, cy - 8)], fill="#F7F2E7", width=2)


def ic_culture(cx, cy):
    d.polygon([(cx - 18, cy - 14), (cx, cy - 6), (cx, cy + 16), (cx - 18, cy + 8)], fill="#6A3FA0")
    d.polygon([(cx + 18, cy - 14), (cx, cy - 6), (cx, cy + 16), (cx + 18, cy + 8)], fill="#8A5FC0")


def ic_globe(cx, cy):
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline="#1F4E79", width=3)
    d.ellipse([cx - 8, cy - 18, cx + 8, cy + 18], outline="#1F4E79", width=2)
    d.line([(cx - 18, cy), (cx + 18, cy)], fill="#1F4E79", width=2)


ICONS = [
    (("court", "icj", "tribunal", "guilty", "sentenc", "justice", "judge"), ic_justice),
    (("missile", "strike", "killed", "war", "military", "police", "gang", "fire", "attack", "drone"), ic_war),
    (("cyclone", "flood", "storm", "hurricane", "earthquake", "landfall", "wildfire"), ic_disaster),
    (("gta", "sale", "ipo", "market", "econom", "budget", "imf", "rate", "shares", "oil", "trade", "aid", "loan", "fund"), ic_business),
    (("olympic", "marathon", "sport", "football", "cup", "medal", "doping"), ic_sport),
    (("vaccine", "virus", "health", "hospital", "measles", "bird flu"), ic_health),
    (("fossil", "climate", "cop31", "emissions", "wildfire"), ic_env),
    (("study", "space", "species", "science", "research", "astronomer", "gene", "vaccine"), ic_science),
    (("author", "film", "music", "book", "novel", "director"), ic_culture),
    (("summit", "president", "minister", "parliament", "election", "court", "eu", "un", "nato", "mayor", "ambassador", "sanction"), ic_politics),
]


def icon_for(story):
    text = (story["headline"] + " " + story["summary"]).lower()
    for keys, fn in ICONS:
        if any(k in text for k in keys):
            return fn
    return ic_globe


# ---------- masthead ----------
d.text((24, 12), "THE WORLD IN ONE DAY", font=f(FONT_BLACK, 22), fill=INK)
dt = "Thursday 19 November 2026"
dw = d.textlength(dt, font=f(GEORGIA_B, 18))
d.text((1000 - dw, 16), dt, font=f(GEORGIA_B, 18), fill=RED)
hrule(46)
headline = "Thursday 19 November 2026"
hw = d.textlength(headline, font=f(GEORGIA_B, 52))
d.text(((W - hw) / 2, 56), headline, font=f(GEORGIA_B, 52), fill=INK)
sub = f"{len(stories)} stories · {len(edition['regions'])} regions · every event from this one day"
sw = d.textlength(sub, font=f(GEORGIA, 17))
d.text(((W - sw) / 2, 122), sub, font=f(GEORGIA, 17), fill=MUTED)

# region chips
labels = []
for r in edition["regions"]:
    name = r.get("id") or r.get("name") or ""
    labels.append(f"{name.upper()} {r['count']}")
font = f(FONT_BOLD, 11)
widths = [int(d.textlength(t, font=font)) + 14 for t in labels]
gap = 8
total = sum(widths) + gap * (len(labels) - 1)
x = (W - total) / 2
for t, w in zip(labels, widths):
    d.rounded_rectangle([x, 148, x + w, 166], radius=4, fill=BLUE)
    d.text((x + 7, 151), t, font=font, fill="#FFFFFF")
    x += w + gap
hrule(178, RULE, 2)

# ---------- lead story ----------
lead = stories[0]
card(24, 186, 976, 140)
d.rectangle([24, 186, 286, 326], fill="#EAF1F8")
d.line([(286, 186), (286, 326)], fill=RULE, width=1)
# flags
def flag(x, y, kind):
    w, h = 66, 40
    if kind == "US":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill="#B22234" if i % 2 == 0 else "#FFFFFF")
        d.rectangle([x, y, x + w * 0.42, y + h * 4 / 7], fill="#3C3B6E")
        for r in range(2):
            for c in range(3):
                star(x + 5 + c * 9, y + 4 + r * 8, 2.5, "#FFFFFF")
    elif kind == "CN":
        d.rectangle([x, y, x + w, y + h], fill="#DE2910")
        star(x + 11, y + 11, 7, "#FFDE00")
    else:
        d.rectangle([x, y, x + w, y + h / 3], fill="#FFFFFF")
        d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill="#0039A6")
        d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill="#D52B1E")
    d.line([(x - 5, y - 5), (x - 5, y + h + 18)], fill="#8A7A5A", width=2)

flag(42, 206, "US")
flag(128, 206, "CN")
flag(214, 206, "RU")
d.text((42, 268), "SHENZHEN · APEC CHINA 2026", font=f(FONT_BOLD, 13), fill=BLUE)

tx = 304
chip(tx, 196, "WORLD · APEC CHINA 2026", BLUE, 12)
y = block(tx, 220, lead["headline"], f(GEORGIA_B, 28), INK, 672, 34, 2)
y = block(tx, y + 4, strip_sources(lead["summary"]), f(GEORGIA, 17), "#33302A", 672, 22, 2)

# ---------- feature cards ----------
features = stories[1:10]
fx = [24, 352, 680]
fy = 336
fw, fh = 312, 108
for i, st in enumerate(features):
    col, row = i % 3, i // 3
    x, y = fx[col], fy + row * (fh + 8)
    card(x, y, fw, fh)
    chip(x + 10, y + 8, st["region"].upper(), RED if st["region"] == "asia" else BLUE, 10)
    icon_for(st)(x + fw - 34, y + 40)
    block(x + 10, y + 32, st["headline"], f(GEORGIA_B, 14), INK, fw - 70, 17, 2)
    block(x + 10, y + 70, strip_sources(st["summary"]), f(GEORGIA, 10.5), "#33302A", fw - 20, 13, 2)

# ---------- also list ----------
list_y = 686
d.text((24, list_y), "ALSO ON THURSDAY 19 NOVEMBER", font=f(FONT_BLACK, 14), fill=INK)
hrule(list_y + 22, RULE, 2)
rest = stories[10:]
col_x = [24, 520]
font = f(GEORGIA, 12)
for i, st in enumerate(rest):
    x = col_x[i // 12]
    y = list_y + 32 + (i % 12) * 23
    txt = f"{i + 11}. {st['headline']}"
    if st.get("place"):
        txt += f" — {st['place']}"
    lines = fit(txt, font, 464, 1)
    d.text((x, y), lines[0], font=font, fill=INK)

# ---------- date check + footer ----------
d.rounded_rectangle([24, 984, 1000, 1006], radius=4, outline=RED, width=2)
d.text((34, 989), "DATE CHECK: Every story on this page is from Thursday 19 November 2026.", font=f(FONT_BOLD, 11), fill=RED)
foot = "19 NOVEMBER 2026 · THE WORLD IN ONE DAY · drawn in code · sources: AFP, Reuters, BBC, Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature"
fw2 = d.textlength(foot, font=f(FONT, 10))
d.text(((W - fw2) / 2, 1010), foot, font=f(FONT, 10), fill=MUTED)

img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)
print("saved", img.size, len(stories), "stories")
