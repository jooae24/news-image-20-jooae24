# news-image-20261120 — The World in One Page

Entry for the make.fun bounty **news-image-20261120**: "Sum up 20 November's
world news in one image" ($250, top 50). A dense newspaper front page,
1024×1024, summarising Friday 20 November 2026 in **50 sourced stories**.

## What's on the poster

- **Masthead** — "Friday 20 November 2026", 50 stories, 6 continents.
- **The Day in UTC** — six timeline entries, 02:00–19:00 UTC.
- **4 big stories, each with an original programmatic illustration:**
  1. Trump–Xi–Putin three-way summit in Shenzhen (diagram of the three leaders)
  2. ICJ rules Myanmar committed genocide against the Rohingya (courthouse, 9–6)
  3. Cyclone Akvan landfall in Odisha (cyclone spiral + coast)
  4. Houthi missile damages the Saudi PIF tower in Riyadh (tower + missile)
- **Grid 5–16** — numbered stories with region/topic tag, headline, summary
  and a source per story (COP31, Kyiv strikes, Kerch Bridge, Hormuz, Gaza,
  US markets, Anthropic IPO, Kenya Ebola, EU–UK summit, Merz/Yalta,
  Greenland–US deal, Haiti).
- **"Where It Happened" world map** — pins numbered 1–16, dots for stories 17–50.
- **Also on Friday 20 November, 17–50** — one line per story (Bukele, GTA VI
  first-day sales, acai genome, Riemann hypothesis, and 30 more).
- **Date Check footer** — the Shenzhen summit and the ICJ ruling were
  delivered Thursday 19 Nov and lead the page only because Friday was
  dominated by reactions and follow-up; GTA VI and Anthropic's IPO are
  included only for figures first reported on Friday; the follow-up, the
  COP31 final deal and the Ebola countdown outcome are not yet due.
- **Sources line** — AP, Reuters, AFP, CNN, BBC, Al Jazeera, Euronews, IMD,
  PTI, HRW, Variety, Smithsonian Magazine, Ars Technica, TechXplore.
  All drawings are original; no photos.

## Build the poster

```sh
python3 build_poster.py        # renders assets/entry.png (variant A)
python3 build_poster.py b variants/variant-b.png   # alternate layout
python3 build_poster.py c variants/variant-c.png   # alternate layout
```

`build_poster.py` needs Pillow only; fonts are the system DejaVu fonts.
Variant A (classic 4-across front page) was chosen after a self-evaluation
of three variants: B (big stories 2×2) and C (taller big stories, 3-column
grid/list) both pushed the 17–50 list and the Date Check footer off the
1024×1024 page, while A fits all 50 stories, the map, the Date Check and
the sources line inside the frame with no text overflowing its box.

## Run the entry

```sh
python3 main.py        # verifies assets/entry.png is a 1024×1024 PNG
                       # and copies it to /output/entry.png
```

`main.py` uses only the Python standard library, makes no network calls,
and is deterministic: repeated runs copy the same bytes.

## Files

- `main.py` — stdlib-only entry point (copy + verify).
- `build_poster.py` — Pillow renderer for the poster (variants a/b/c).
- `assets/entry.png` — the finished 1024×1024 poster (variant A).
- `variants/` — the two losing layout variants, for reference.
- `LICENSE` — MIT. `README.md` — this file.
