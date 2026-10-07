# EPG Farm

Synthetic live linear TV EPG (Electronic Program Guide) for CTV testing.

Generates a realistic 100-channel linear TV lineup with a 7-day program guide,
a Sports Hub with live scores, and 10 viewer agents for personalization testing.

**Separate project from `synth-farm`** (which simulates user behavior events).
This one simulates the *content side*: channels, programs, schedules, scores.

## Quickstart

```bash
python3 scripts/generate.py   # regenerate data/*.json
cd web && python3 -m http.server 8901
# open http://localhost:8901
```

Stdlib only. No build step, no dependencies.

## What's inside

- **100 channels** across 9 genres: sports (20), news (12), movies (12),
  kids (10), entertainment (12), documentary (10), lifestyle (10),
  music (6), international (8)
- **271 realistic programs** — fictional but believable titles, descriptions,
  ratings, and metadata (not lorem ipsum)
- **10 viewer agents** — personas with genre preferences, favorite sports,
  and watch hours (e.g. "Marcus 'Coach' Bell", die-hard sports fan)
- **Seeded schedule engine** — deterministic 7-day guide with dayparting
  (morning news, primetime drama, late night). Same input = same grid.
- **Live TV tab** — EPG grid with now/next, personalized "Top picks" rail
  per agent, program detail modal
- **Sports Hub tab** — live game tiles with simulated live scores
  (Q3 4:32, 2H 67', etc.), upcoming games, sports-only EPG grid

## Data files

- `data/channels.json` — 100 channels (id, name, number, genre, subgenre)
- `data/programs.json` — 271 programs (title, desc, genre, duration, rating)
- `data/agents.json` — 10 viewer personas with taste profiles

## Personalization

Selecting a viewer agent re-ranks the "Top picks" rail by genre affinity
(+ live boost + favorite-sport boost) and reorders Sports Hub tiles so the
agent's favorite sports surface first.

## Live scores

`simScore()` in `web/index.html` generates deterministic, clock-progressing
scores per sport: football (Q1-Q4), basketball (Q1-Q4), soccer (1H/2H + minute),
baseball (innings), hockey (periods). Scores advance with elapsed game time.
