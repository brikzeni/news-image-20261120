# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/brikzeni/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/brikzeni/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One newspaper-style image summing up world news of Friday 20 November 2026:
the first Trump–Xi–Putin summit in Shenzhen, the ICJ ruling that Myanmar
committed genocide against the Rohingya, Russia's overnight barrage on Kyiv's
bridges (and Polish airspace), the Houthi strike on Riyadh's PIF Tower, the
AI sell-off around Anthropic's record IPO, and COP31 dropping fossil fuels.
Every fact was verified against at least two credible news sources (see
RESEARCH.md in the campaign workspace for the source list).

## The six stories

1. **Shenzhen summit** — Trump, Xi and Putin meet face to face; four-point
   "peace declaration", no deal on Ukraine or Iran.
2. **The Hague** — ICJ: Myanmar committed genocide against the Rohingya in
   2017, the first state ever held responsible.
3. **Kyiv** — 400+ drones and 110 missiles overnight; 8 killed, three Dnipro
   bridges hit; Russian objects violate Polish airspace.
4. **Riyadh** — Houthi missile damages 7–8 floors of the PIF Tower, HQ of
   the Saudi wealth fund; no injuries.
5. **Markets** — Anthropic's record IPO closes +17% at $97.17, but the
   Nikkei falls 4.8% and the S&P 500 logs a fifth straight loss.
6. **COP31, Antalya** — draft deal drops every mention of ending fossil-fuel
   use and admits 1.5 °C will be overshot.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to the
output directory. `draw.py` is the program that drew the image with Pillow
and DejaVu fonts — re-run it with `python3 draw.py` to regenerate `entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
