#!/usr/bin/env python3
"""Render the Friday 20 November 2026 front page (1024x1024).

Original programmatic drawings only: no photos, no copied images.
Run:  python3 build_poster.py [a|b|c] [output-path]
Default variant is A; default output is assets/entry.png.
"""
import sys, textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 248, 232)
INK = (18, 18, 18)
RED = (178, 34, 28)
BLUE = (24, 64, 128)
TEAL = (14, 110, 110)
GOLD = (176, 132, 20)
GREY = (90, 88, 80)
LIGHT = (238, 230, 205)
RULE = (60, 55, 45)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(p, s, b=False):
    return ImageFont.truetype(p, s)

def wrap(draw, text, font, width):
    out = []
    for para in text.split("\n"):
        words = para.split()
        line, lines = "", []
        for w in words:
            t = (line + " " + w).strip()
            if draw.textlength(t, font=font) <= width:
                line = t
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        out.extend(lines if lines else [""])
    return out

def para(draw, x, y, text, font, fill, width, lh):
    lines = wrap(draw, text, font, width)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def para_limit(draw, x, y, text, font, fill, width, lh, max_lines):
    """Render at most max_lines lines, truncating with an ellipsis."""
    lines = wrap(draw, text, font, width)[:max_lines]
    if len(wrap(draw, text, font, width)) > max_lines and lines:
        last = lines[-1]
        while last and draw.textlength(last + "...", font=font) > width:
            last = last[:-1].rstrip()
        lines[-1] = last + "..."
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def hline(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)

BIG = [
    ("1", "ASIA · SUMMIT", "Trump, Xi and Putin hold first three-way summit",
     "Leaders of the US, China and Russia met in Shenzhen on Thursday and signed a four-point joint declaration after about 70 minutes of talks. No breakthrough on Ukraine, Iran or nuclear arms; Germany's Merz warned Europe would not accept a settlement negotiated without it.",
     "Reuters, AP", "summit"),
    ("2", "JUSTICE · MYANMAR", "ICJ rules Myanmar committed genocide against the Rohingya",
     "In a 9-6 vote the World Court found Myanmar's military committed mass killings and widespread sexual violence in 2016-17 clearance operations; about 10,000 killed, 700,000+ fled. A first: the ICJ has held a state responsible for genocide. Myanmar called the ruling \"unfair\" on Friday.",
     "ICJ, CNN, Reuters, HRW", "court"),
    ("3", "ASIA · WEATHER", "Cyclone Akvan makes landfall in Odisha",
     "Cyclonic Storm Akvan crossed the north Andhra Pradesh and south Odisha coasts near Gopalpur 07:30-08:30 IST, winds 70-80 km/h gusting to 90. More than 300,000 people were evacuated to shelters; no deaths or major damage in the first assessment; it weakened to a deep depression by afternoon.",
     "IMD, PTI", "cyclone"),
    ("4", "MIDDLE EAST · CONFLICT", "Houthi missile damages Saudi wealth fund tower in Riyadh",
     "Houthi missiles hit Riyadh's financial district, damaging the Public Investment Fund tower and other buildings. Saudi Arabia intercepted another Houthi missile and five drones on Friday.",
     "Reuters, AP", "tower"),
]

GRID = [
    ("5", "CLIMATE · COP31", "COP31 draft drops call to phase out fossil fuels",
     "Negotiators in Antalya, Turkey removed any reference to ending fossil fuel use from a slimmed-down draft deal. Activists chanted \"shame\" as talks faltered.", "Reuters, AFP"),
    ("6", "EUROPE · UKRAINE WAR", "Russia launches major overnight missile and drone attack on Kyiv",
     "Explosions heard early Friday; missile debris struck a building in Obolonskyi district. Austrian and Dutch embassies damaged, staff unharmed; metro stations became overnight shelters.", "Reuters, Euronews"),
    ("7", "EUROPE · UKRAINE WAR", "Kerch Bridge rail traffic resumes after strikes",
     "Rail traffic across the Kerch Bridge resumed on Friday after earlier strikes disrupted the crossing.", "Reuters"),
    ("8", "MIDDLE EAST · IRAN", "Iran war enters ninth month as Hormuz tanker attacks intensify",
     "A tanker caught fire in the Strait of Hormuz after hitting a mine. Iran readied a tanker convoy at Kharg Island to test the US oil blockade.", "Reuters, AP"),
    ("9", "MIDDLE EAST · GAZA", "Israeli forces cross Yellow Line in central Gaza",
     "Israeli troops crossed the ceasefire boundary, the first such incursion since the truce. Israeli drone attacks killed seven Palestinians in central Gaza.", "Al Jazeera, Reuters"),
    ("10", "ECONOMY · MARKETS", "US stocks fall for a sixth straight day",
     "S&P 500 lost 2.02%, Dow fell 1,101 points (-2.19%) below 50,000, Nasdaq -2.25%. Japan's Nikkei down 4.8%.", "Reuters"),
    ("11", "TECH · MARKETS", "Anthropic falls 9.5% a day after record IPO",
     "Shares slid to about $88 after closing at $97.17 on Thursday's Nasdaq debut. Underwriters exercised their option in full, lifting the total raised to about $93.5bn, the largest IPO on record.", "Reuters, TechXplore"),
    ("12", "AFRICA · HEALTH", "Kenya discharges its last Ebola patient",
     "Kenya discharged its last Ebola patient, 37 days after its first case, starting a 42-day countdown to an Ebola-free declaration.", "AP, Reuters"),
    ("13", "EUROPE · DIPLOMACY", "EU and UK hold second summit in Brussels",
     "European Council President Costa and Commission President von der Leyen met British PM Andy Burnham to deepen the renewed strategic partnership.", "Euronews"),
    ("14", "EUROPE · DIPLOMACY", "Germany rejects a new Yalta over Europe's future",
     "Chancellor Friedrich Merz warned Europeans would not accept a great-power settlement on Europe negotiated without them, after the Shenzhen summit.", "Reuters"),
    ("15", "EUROPE · SECURITY", "Denmark approves Greenland-US security agreement",
     "Denmark's parliament approved a trilateral security agreement with Greenland and the United States.", "Euronews"),
    ("16", "AMERICAS · SECURITY", "34 suspected gang members killed in Haiti",
     "Haitian police said 34 suspected gang members were killed; two Salvadoran soldiers died handling explosives in Haiti.", "AP, Al Jazeera"),
]

ALSO = [
    (17, "Bukele registers for a third term in El Salvador."),
    (18, "Dozens missing after a migrant boat capsizes off Senegal."),
    (19, "Drone strike kills 10 at a gold mine in Sudan's South Kordofan."),
    (20, "US and Venezuela sign a military cooperation deal."),
    (21, "US Senate passes a major bipartisan energy-permitting bill, 62-33."),
    (22, "White House fires cyber director Sean Cairncross after a week of tech outages."),
    (23, "Estonia to shut its border with Russia over a GRU-linked sabotage attack."),
    (24, "HMS Vengeance sets a record with a 217-day underwater patrol."),
    (25, "US auctions first-ever deep-sea mining leases despite a court ruling."),
    (26, "NYC mayor unveils a plan to close the notorious Rikers Island jail by 2032."),
    (27, "Italy: workers and students stage a nationwide strike over living costs."),
    (28, "Morocco commits 366 million euros to build a national defence industry by 2035."),
    (29, "GTA VI sells 24.5 million units worth $2.36bn on its first day, Sensor Tower says."),
    (30, "GTA VI draws 7.88 million concurrent viewers across YouTube, Twitch and Kick within three hours."),
    (31, "Brazilian scientists sequence the acai berry genome: 3.1 billion base pairs, 41,700 genes."),
    (32, "Forced fumbles hit 1.8 per game, up 33% year on year, on a Peanut Punch renaissance."),
    (33, "14 charged over Southern California train heists netting $22m of Nike sneakers, tools and electronics."),
    (34, "US Army postpones Friday's detonation of unstable explosives in Middletown, Iowa to Monday 23 Nov."),
    (35, "Fiona the hippo dies at Cincinnati Zoo after swallowing a visitor's hat."),
    (36, "BBC reports Anthropic may have solved the Riemann hypothesis, a major maths problem."),
    (37, "Lauren Price beats Kotaskova to become undisputed world welterweight champion."),
    (38, "Nepal PM Balendra Shah to meet India's PM Modi on his first trip abroad."),
    (39, "Trump threatens a ban on US firms building AI data centres overseas."),
    (40, "US lawmakers push for tougher AI chip rules amid the China export crackdown."),
    (41, "NASA's new Moon plan is taking shape, but big questions remain."),
    (42, "A Roman cup and hundreds of treasures unearthed in a 2,000-year-old tomb reveal an ancient Asian empire's trade network."),
    (43, "Sudan's war leaves disabled children missing out on education."),
    (44, "Iraq deploys federal forces near a Kataib Hezbollah stronghold at Jurf al-Sakhar."),
    (45, "Bangladesh tense after an opposition-called shutdown and political violence."),
    (46, "Pakistan says its forces killed 22 militants near the Afghan frontier."),
    (47, "India relaxes vessel-age restrictions to expand its national fleet."),
    (48, "Tallinn Black Nights Fest: 'On Top of the Cliff' scores the Grand Prix."),
    (49, "CMA Awards see a 55% ratings bump with Taylor Swift's return to the show."),
    (50, "The Internet Archive's workers are unionizing."),
]

TIMELINE = [
    ("02:00 UTC", "Akvan landfall, Gopalpur, India."),
    ("06:00 UTC", "Overnight strike on Kyiv; two embassies hit."),
    ("09:30 UTC", "Myanmar calls ICJ ruling \"unfair\"."),
    ("14:30 UTC", "Anthropic slides ~10% after record IPO."),
    ("17:00 UTC", "COP31 draft drops fossil-fuel phase-out."),
    ("19:00 UTC", "Houthi damage to Riyadh PIF tower."),
]

# Rough lon/lat -> map x/y for pins 1-16 (lon -170..190, lat -55..75)
PINS = {1: (116, 22), 2: (92, 20), 3: (85, 19), 4: (47, 25), 5: (30, 37),
        6: (30, 50), 7: (36, 45), 8: (56, 26), 9: (34, 31), 10: (-77, 40),
        11: (-122, 37), 12: (37, 0), 13: (4, 51), 14: (10, 51), 15: (-42, 72),
        16: (-72, 19)}
DOTS = [( -100, 13), (-62, -10), (30, 15), (-70, 10), (-95, 38), (-100, 35),
        (10, 59), (-2, 54), (-120, 35), (-74, 41), (12, 42), (-7, 34),
        (-122, 37), (-100, 20), (100, 5), (78, 21), (67, 30), (90, 24),
        (77, 28), (139, 35), (35, -1), (32, 15), (44, 33), (47, 32),
        (100, 13), (103, 1), (-43, -23), (151, -33), (18, 59), (-0, 51)]

def draw_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 248), outline=BLUE)
    d.polygon([(x + 8, y + h - 6), (x + w // 2, y + 8), (x + w - 8, y + h - 6)], outline=BLUE)
    for cx, col, lab in [(x + w * 0.22, RED, "US"), (x + w * 0.5, RED, "CN"),
                         (x + w * 0.78, BLUE, "RU")]:
        d.ellipse([cx - 20, y + h - 52, cx + 20, y + h - 12], fill=col)
        d.text((cx - 8, y + h - 40), lab, font=F(SANSB, 10), fill=(255, 255, 255))
    d.text((x + 6, y + 3), "SHENZHEN · 3-WAY SUMMIT", font=F(SANSB, 9), fill=BLUE)

def draw_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210), outline=GOLD)
    d.polygon([(x + 10, y + 34), (x + w // 2, y + 6), (x + w - 10, y + 34)], fill=GOLD)
    for cx in (x + w * 0.25, x + w * 0.5, x + w * 0.75):
        d.rectangle([cx - 4, y + 36, cx + 4, y + h - 10], fill=INK)
    d.rectangle([x + 8, y + h - 10, x + w - 8, y + h - 4], fill=INK)
    d.text((x + 6, y + h - 26), "9-6", font=F(SERIFB, 13), fill=RED)
    d.text((x + w - 52, y + 3), "THE HAGUE", font=F(SANSB, 9), fill=INK)

def draw_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 234, 240), outline=TEAL)
    cx, cy = x + w * 0.48, y + h // 2 + 8
    for r, col in [(24, TEAL), (18, (40, 140, 140)), (12, (90, 170, 170)), (6, (255, 255, 255))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    d.line([(x + w * 0.62, y + 6), (x + w * 0.66, y + h - 6)], fill=(120, 90, 40), width=3)
    d.text((x + w * 0.68, y + 6), "ODISHA", font=F(SANSB, 9), fill=INK)
    d.text((x + w * 0.68, y + 20), "70-80 km/h", font=F(SANS, 9), fill=INK)
    d.text((x + 6, y + 3), "AKVAN · 07:30 IST", font=F(SANSB, 9), fill=TEAL)

def draw_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 210), outline=INK)
    bx = x + w * 0.42
    d.rectangle([bx, y + 14, bx + 46, y + h - 6], fill=(70, 70, 78))
    for yy in range(y + 20, y + h - 10, 9):
        d.line([(bx + 4, yy), (bx + 42, yy)], fill=(200, 200, 200), width=1)
    d.polygon([(bx + 46, y + 14), (bx + 62, y + 26), (bx + 46, y + 30)], fill=RED)
    d.line([(bx + 62, y + 26), (bx + 78, y + 8)], fill=RED, width=2)
    d.ellipse([bx + 72, y + 2, bx + 84, y + 14], fill=(255, 200, 40))
    d.text((x + 6, y + 3), "RIYADH · PIF TOWER", font=F(SANSB, 9), fill=RED)
    d.text((x + w - 78, y + h - 16), "5 drones down", font=F(SANS, 8), fill=INK)

ILLUS = {"summit": draw_summit, "court": draw_court,
         "cyclone": draw_cyclone, "tower": draw_tower}

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 242), outline=BLUE)
    d.text((x + 6, y + 3), "WHERE IT HAPPENED — pins 1-16 numbered; dots = stories 17-50",
           font=F(SANSB, 10), fill=BLUE)
    mx0, my0, mw, mh = x + 8, y + 20, w - 16, h - 26
    # schematic continents (simple polygons, original drawing)
    def px(lon): return mx0 + (lon + 170) / 360 * mw
    def py(lat): return my0 + (75 - lat) / 130 * mh
    conts = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 70), (-80, 62), (-60, 55),
         (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-95, 20), (-105, 22),
         (-115, 30), (-125, 40), (-140, 58), (-165, 60)],
        [(-80, 10), (-60, 8), (-50, 0), (-40, -8), (-35, -20), (-45, -30),
         (-60, -35), (-70, -20), (-75, -5), (-80, 5)],
        [(-10, 36), (0, 38), (10, 44), (20, 45), (30, 42), (35, 36),
         (28, 40), (15, 55), (5, 58), (-5, 50), (-10, 44)],
        [(35, 30), (45, 30), (55, 25), (60, 15), (50, 12), (42, 15), (38, 22)],
        [(60, 70), (90, 72), (120, 72), (150, 70), (170, 66), (160, 60),
         (140, 55), (120, 50), (100, 55), (80, 60), (65, 68)],
        [(65, 35), (75, 30), (85, 20), (95, 15), (100, 8), (105, 20),
         (110, 25), (120, 30), (125, 40), (115, 35), (100, 35), (85, 35), (75, 35)],
        [(113, -22), (130, -12), (142, -11), (150, -25), (153, -32),
         (140, -38), (130, -32), (115, -32)],
    ]
    for c in conts:
        d.polygon([(px(lo), py(la)) for lo, la in c], fill=(196, 214, 176),
                  outline=(90, 120, 70))
    for lon, lat in DOTS:
        d.ellipse([px(lon) - 2, py(lat) - 2, px(lon) + 2, py(lat) + 2], fill=GREY)
    for n, (lon, lat) in sorted(PINS.items()):
        cx, cy = px(lon), py(lat)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255))
        d.text((cx - 3 if n < 10 else cx - 6, cy - 6), str(n),
               font=F(SANSB, 9), fill=(255, 255, 255))

def build(variant="a"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 22
    # ---- masthead ----
    d.rectangle([0, 0, W, 86], fill=INK)
    d.text((M, 6), "THE WORLD IN ONE PAGE", font=F(SERIFB, 30), fill=(255, 255, 255))
    d.text((M, 44), "Friday 20 November 2026", font=F(SERIFB, 22), fill=(255, 214, 90))
    d.text((W - M - 330, 12), "50 STORIES · 6 CONTINENTS", font=F(SANSB, 15), fill=(255, 255, 255))
    d.text((W - M - 330, 36), "FRIDAY EDITION · ALL TIMES UTC", font=F(SANS, 12), fill=(200, 200, 200))
    d.text((W - M - 330, 56), "Every story happened or was first", font=F(SANS, 10), fill=(200, 200, 200))
    d.text((W - M - 330, 70), "reported on Friday 20 Nov 2026*", font=F(SANS, 10), fill=(200, 200, 200))
    # ---- timeline ----
    y = 92
    d.text((M, y), "THE DAY IN UTC", font=F(SANSB, 11), fill=RED)
    hline(d, M, W - M, y + 16, 1, RED)
    ty = y + 20
    if variant == "b":
        tw = (W - 2 * M) // 3
    else:
        tw = (W - 2 * M) // 6
    cols = 3 if variant == "b" else 6
    for i, (t, txt) in enumerate(TIMELINE):
        cx = M + (i % cols) * tw
        cy = ty + (i // cols) * 34
        d.text((cx, cy), t, font=F(SANSB, 10), fill=RED)
        para_limit(d, cx, cy + 11, txt, F(SANS, 9), INK, tw - 8, 10, 2)
    big_y = ty + (68 if variant == "b" else 36)
    hline(d, M, W - M, big_y - 4, 2)
    # ---- big stories ----
    if variant == "b":
        bh, ih = 152, 62
        bw = (W - 2 * M - 10) // 2
        for i, (n, tag, head, summ, src, kind) in enumerate(BIG):
            bx = M + (i % 2) * (bw + 10)
            by = big_y + (i // 2) * (bh + 8)
            d.rectangle([bx, by, bx + bw, by + bh], outline=RULE, width=1)
            d.text((bx + 6, by + 3), n + "  " + tag, font=F(SANSB, 10), fill=RED)
            ILLUS[kind](d, bx + 6, by + 20, bw - 12, ih)
            yy = para_limit(d, bx + 6, by + 20 + ih + 4, head, F(SERIFB, 12), INK, bw - 12, 14, 2)
            yy = para_limit(d, bx + 6, yy + 1, summ, F(SANS, 9), INK, bw - 12, 11, 3)
            d.text((bx + 6, by + bh - 12), "Source: " + src, font=F(SANS, 8), fill=GREY)
        grid_y = big_y + 2 * bh + 24
    else:
        bh = 192 if variant == "c" else 166
        ih = 78 if variant == "c" else 62
        bw = (W - 2 * M - 30) // 4
        for i, (n, tag, head, summ, src, kind) in enumerate(BIG):
            bx = M + i * (bw + 10)
            by = big_y
            d.rectangle([bx, by, bx + bw, by + bh], outline=RULE, width=1)
            d.text((bx + 5, by + 3), n, font=F(SERIFB, 14), fill=RED)
            d.text((bx + 22, by + 5), tag, font=F(SANSB, 8), fill=RED)
            ILLUS[kind](d, bx + 5, by + 22, bw - 10, ih)
            yy = para_limit(d, bx + 5, by + 22 + ih + 4, head, F(SERIFB, 11), INK, bw - 10, 13, 2)
            yy = para_limit(d, bx + 5, yy + 1, summ, F(SANS, 9), INK, bw - 10, 11, 4)
            d.text((bx + 5, by + bh - 12), "Source: " + src, font=F(SANS, 7), fill=GREY)
        grid_y = big_y + bh + 12
    # ---- grid 5-16 ----
    d.text((M, grid_y), "THE DAY'S NEWS  ·  5-16", font=F(SANSB, 11), fill=RED)
    hline(d, M, W - M, grid_y + 15, 1, RED)
    gy = grid_y + 19
    if variant == "b":
        gcols, grows, gh = 3, 4, 70
    elif variant == "c":
        gcols, grows, gh = 3, 4, 72
    else:
        gcols, grows, gh = 4, 3, 80
    gw = (W - 2 * M - (gcols - 1) * 8) // gcols
    for i, (n, tag, head, summ, src) in enumerate(GRID):
        gx = M + (i % gcols) * (gw + 8)
        gr = gy + (i // gcols) * (gh + 4)
        d.rectangle([gx, gr, gx + gw, gr + gh], outline=(180, 170, 140), width=1)
        d.text((gx + 4, gr + 2), n + "  " + tag, font=F(SANSB, 8), fill=RED)
        yy = para_limit(d, gx + 4, gr + 14, head, F(SANSB, 10), INK, gw - 8, 12, 2)
        yy = para_limit(d, gx + 4, yy, summ, F(SANS, 9), INK, gw - 8, 11, 2)
        d.text((gx + 4, gr + gh - 11), "Source: " + src, font=F(SANS, 7), fill=GREY)
    map_y = gy + grows * (gh + 4) + 6
    # ---- map ----
    map_h = 148 if variant == "b" else 104
    draw_map(d, M, map_y, W - 2 * M, map_h)
    list_y = map_y + map_h + 8
    # ---- also list 17-50 ----
    d.text((M, list_y), "ALSO ON FRIDAY 20 NOVEMBER  ·  17-50",
           font=F(SANSB, 11), fill=RED)
    hline(d, M, W - M, list_y + 15, 1, RED)
    ly = list_y + 19
    lcols = 3 if variant == "c" else 4
    per = (len(ALSO) + lcols - 1) // lcols
    lw = (W - 2 * M - (lcols - 1) * 10) // lcols
    list_bottom = ly
    for c in range(lcols):
        lx = M + c * (lw + 10)
        yy = ly
        for n, txt in ALSO[c * per:(c + 1) * per]:
            lines = wrap(d, f"{n}. {txt}", F(SANS, 9), lw)
            for ln in lines:
                d.text((lx, yy), ln, font=F(SANS, 9), fill=INK)
                yy += 10
        list_bottom = max(list_bottom, yy)
    foot_y = list_bottom + 6
    # ---- footer ----
    hline(d, M, W - M, foot_y, 2)
    fy = foot_y + 5
    d.text((M, fy), "DATE CHECK", font=F(SANSB, 10), fill=RED)
    dc = ("* The Shenzhen summit and the ICJ genocide ruling were DELIVERED Thursday 19 Nov — they lead "
          "this page because Friday 20 Nov was dominated by reactions and follow-up (Myanmar's "
          "rejection, Merz's Yalta warning). GTA VI launched Thursday 19 Nov — included "
          "only for its first-day sales figures, reported Friday. Anthropic's IPO debut was Thursday — included "
          "only for Friday's 9.5% fall and the $93.5bn final tally. NOT YET: the Xi-Trump-Putin follow-up, the "
          "COP31 final deal and the 42-day Ebola countdown outcome are all due after Friday.")
    fy = para(d, M + 78, fy, dc, F(SANS, 8), INK, W - 2 * M - 78, 10)
    fy += 2
    d.text((M, fy), "Sources: AP, Reuters, AFP, CNN, BBC, Al Jazeera, Euronews, IMD, PTI, HRW, Variety, "
                    "Smithsonian Magazine, Ars Technica, TechXplore. Original drawings.",
           font=F(SANS, 8), fill=GREY)
    return img

if __name__ == "__main__":
    var = sys.argv[1] if len(sys.argv) > 1 else "a"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/entry.png"
    img = build(var)
    img.save(out, optimize=True)
    print(out, img.size)
