# AI Agentic Farm for Live Linear

A multi-agent testing environment for AI-driven personalization of live linear TV (CTV EPG).

## Vision

Build and test AI agents that don't just recommend content — they act as viewers. They browse the guide, pick shows, react to live sports, and give feedback. We measure how well personalization algorithms serve them.

## Current State

The `web/` directory contains a working synthetic CTV EPG prototype:

- **Live TV tab**: 100-channel linear EPG grid with personalized Top Picks rail
- **Sports Hub tab**: App-centric view (ESPN, NFL, NBA, MLB, NHL, PGA Tour) with live scores
- **3 viewer personalities**: Sports (Marcus Bell), News (Sarah Chen), Movies (James Whitfield)
- **Real content**: 100 real networks, TMDB posters, real team logos, real franchises
- **Simulated schedules**: Seeded schedule engine (acknowledged synthetic — not real EPG data)

## Project Structure

```
web/          Static CTV EPG demo (open index.html via local server)
data/         Channel, program, agent, and team data (JSON + generators)
scripts/      Data generation scripts
```

## Running Locally

```bash
cd web
python3 -m http.server 8000
# Open http://localhost:8000
```

## Roadmap

- [ ] Agent action framework (browse, select, rate, feedback loop)
- [ ] Personalization algorithm benchmarking
- [ ] Real EPG data source integration
- [ ] Multi-agent interaction simulation

## Attribution

- Movie/TV data via TMDB
- Team logos via ESPN
- Schedules are simulated for demo purposes
