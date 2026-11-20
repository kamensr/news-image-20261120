[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kamensr/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kamensr/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# 20 November 2026 — 49 Stories, One Day

Entry for the [make.fun bounty news-image-20261120](https://make.fun/bounty/news-image-20261120): sum up 20 November's world news in one image.

## What it is

A 1024×1024 poster drawn with PIL (flat shapes + real text, no AI photos):

- Kicker + giant date masthead: **FRIDAY 20 NOVEMBER 2026**
- UTC timeline strip of the day's major moments
- 4 illustrated features: Russia's biggest attack on Ukraine this year, Cyclone Akvan in India, COP31 in Antalya ending Friday with no deal, Russian missiles violating Polish airspace
- 12 mini-stories (US market rout close, Asia sell-off, EU–UK summit, and more)
- World map with 12 numbered pins
- "ALSO ON 20 NOV" — 33 one-liners (stories 17–49)
- DATE CHECK box listing stories deliberately excluded (they broke before 20 Nov)
- Sources footer

Every story happened, or was first reported, on 20 November 2026. CLAIM vs CONFIRMED labels are shown where a fact is unverified or an estimate.

## Files

- `generate.py` — builds `entry.png` from the story data (Pillow required)
- `main.py` — stdlib-only entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output/entry.png`)
- `entry.png` — the poster, 1024×1024
- `LICENSE` — MIT

## Build

```bash
pip install pillow
python3 generate.py
python3 main.py
```

## Sources

Reuters, AP, CNN, BBC, Kyiv Independent, WSJ, Barron's, UN News, MetService NZ, Fiji Met Service, Watchers.news, Hindu BusinessLine, Bloomberg Law, Inshorts (single-source items marked).
