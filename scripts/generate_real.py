#!/usr/bin/env python3
"""Real EPG generator - 100% actual networks, shows, movies, teams."""
import json, random, sys
sys.path.insert(0, 'data')
from real_channels import CHANNELS as REAL_CHANNELS
from real_shows import DOCUMENTARY, LIFESTYLE, MUSIC_SHOWS, INTERNATIONAL_SHOWS, NEWS_EXTRA, KIDS_EXTRA, SPORTS_STUDIO_EXTRA

random.seed(42)

# Load real channels
channels = []
for name, number, genre, subgenre in REAL_CHANNELS:
    channels.append({
        "id": f"ch{number}",
        "name": name,
        "number": number,
        "genre": genre,
        "subgenre": subgenre,
    })

# Load TMDB catalog
tmdb = json.load(open('data/catalog_tmdb.json'))
movies = [m for m in tmdb if m['type'] == 'movie' and m['poster']]
tv_shows = [t for t in tmdb if t['type'] == 'tv' and t['poster']]
print(f"TMDB: {len(movies)} movies, {len(tv_shows)} TV shows with posters")

# Real sports teams
NFL = [("Chicago Bears","chi"),("Dallas Cowboys","dal"),("Seattle Seahawks","sea"),
       ("Miami Dolphins","mia"),("Denver Broncos","den"),("New England Patriots","ne")]
NBA = [("LA Lakers","lal"),("Chicago Bulls","chi"),("New York Knicks","nyk"),
       ("Houston Rockets","hou"),("Phoenix Suns","phx"),("Boston Celtics","bos")]
MLS = [("LA Galaxy","lag"),("Seattle Sounders","sea"),("Portland Timbers","por"),
       ("Inter Miami","mia"),("Austin FC","aus"),("NY Red Bulls","ny")]

TEAM_LOGOS = {}
for name, abbr in NFL:
    # Use local downloaded logo (ESPN blocks hotlinking)
    TEAM_LOGOS[name] = f"img/logos/foo_{abbr}.png"
for name, abbr in NBA:
    TEAM_LOGOS[name] = f"img/logos/bas_{abbr}.png"
# MLS logos via ESPN soccer (use generic)
for name, abbr in MLS:
    TEAM_LOGOS[name] = ""  # No reliable ESPN MLS pattern; use generic soccer image

# Save teams
with open('web/data/teams.json', 'w') as f:
    json.dump({name: {"logo": logo, "sport": "football" if name in [n for n,_ in NFL] else "basketball" if name in [n for n,_ in NBA] else "soccer"}
                      for name, logo in TEAM_LOGOS.items()}, f, indent=1)

# Build programs
programs = []
pid = 1

def add_prog(title, desc, genre, subgenre, mins, poster="", rating="TV-PG", year=2024, live=False):
    global pid
    programs.append({
        "id": f"p{pid:05d}", "title": title, "desc": desc, "genre": genre,
        "subgenre": subgenre, "duration_min": mins, "poster": poster,
        "rating": rating, "year": year, "live": live,
    })
    pid += 1

# Distribute TMDB content across movie and entertainment channels
movie_channels = [c for c in channels if c['genre'] == 'movies']
ent_channels = [c for c in channels if c['genre'] == 'entertainment']

# Movies: assign real movies to movie channels
for i, m in enumerate(movies):
    ch = movie_channels[i % len(movie_channels)]
    poster_url = f"https://image.tmdb.org/t/p/w500{m['poster']}" if m['poster'] else ""
    add_prog(m['title'], m['overview'][:200], 'movies', ch['subgenre'],
             random.choice([90, 105, 120, 135]), poster_url,
             random.choice(["PG-13", "R", "PG"]), m['year'] or 2024)

# TV shows: assign to entertainment channels
for i, t in enumerate(tv_shows):
    ch = ent_channels[i % len(ent_channels)]
    poster_url = f"https://image.tmdb.org/t/p/w500{t['poster']}" if t['poster'] else ""
    add_prog(t['title'], t['overview'][:200], 'entertainment', ch['subgenre'],
             random.choice([30, 60]), poster_url, "TV-14", t['year'] or 2024)

# Sports: real matchups
for _ in range(20):
    for league, teams, sport in [("NFL", NFL, "football"), ("NBA", NBA, "basketball"), ("MLS", MLS, "soccer")]:
        a, b = random.sample([t[0] for t in teams], 2)
        add_prog(f"{league}: {a} vs {b}",
                 f"Live {sport} action as {a} take on {b}.",
                 'sports', sport, random.choice([120, 150, 180]), "", "TV-PG", 2026, True)

# Sports studio shows (real names)
sports_shows = [
    ("SportsCenter", "ESPN's flagship sports news and highlights show.", 60),
    ("NFL Live", "Daily NFL news, analysis and interviews.", 60),
    ("NBA Today", "Daily NBA coverage with news and analysis.", 60),
    ("Pardon the Interruption", "Tony Kornheiser and Michael Wilbon debate the day's sports.", 30),
    ("Around the Horn", "Sports journalists debate the biggest stories.", 30),
    ("First Take", "Stephen A. Smith and guests debate sports topics.", 120),
    ("The Pat McAfee Show", "Sports talk with Pat McAfee and crew.", 180),
    ("College GameDay", "Live from campus with college football preview.", 180),
]
for title, desc, mins in sports_shows:
    add_prog(title, desc, 'sports', 'studio', mins, "", "TV-PG", 2026, "Live" in desc)

# News: real show names
news_shows = [
    ("Anderson Cooper 360", "In-depth reporting on the day's top stories.", 60),
    ("Morning Joe", "Morning news and political discussion.", 180),
    ("Fox & Friends", "Morning news, interviews and entertainment.", 180),
    ("The Rachel Maddow Show", "Political commentary and analysis.", 60),
    ("Cuomo", "News analysis with Chris Cuomo.", 60),
    ("BBC World News", "Global news coverage from London.", 30),
    ("Marketplace", "Business and economic news.", 30),
    ("Nightly News", "Evening national newscast.", 30),
]
for title, desc, mins in news_shows:
    add_prog(title, desc, 'news', 'general', mins, "", "TV-PG", 2026, True)

# Kids: real popular shows (from TMDB or well-known)
kids_shows = [
    ("SpongeBob SquarePants", "Adventures of SpongeBob in Bikini Bottom.", 30),
    ("PAW Patrol", "Rescue pups save Adventure Bay.", 30),
    ("Bluey", "Australian cattle dog family adventures.", 30),
    ("Peppa Pig", "Peppa and family have fun adventures.", 30),
    ("Teen Titans Go!", "Teen superheroes in comedic adventures.", 30),
    ("The Amazing World of Gumball", "Gumball and Darwin's misadventures.", 30),
]
for title, desc, mins in kids_shows + KIDS_EXTRA:
    add_prog(title, desc, 'kids', 'animation', mins, "", "TV-Y7", 2024)

# Documentary: real acclaimed docs
for title, desc, mins in DOCUMENTARY:
    add_prog(title, desc, 'documentary', 'nature', mins, "", "TV-PG", 2020)

# Lifestyle: real shows
for title, desc, mins in LIFESTYLE:
    sub = 'food' if any(x in title.lower() for x in ['chopped','diners','barefoot','top chef']) else 'home' if any(x in title.lower() for x in ['fixer','property','house']) else 'reality'
    add_prog(title, desc, 'lifestyle', sub, mins, "", "TV-PG", 2022)

# Music: real shows
for title, desc, mins in MUSIC_SHOWS:
    add_prog(title, desc, 'music', 'pop', mins, "", "TV-PG", 2023)

# International: real global hits
for title, desc, mins in INTERNATIONAL_SHOWS:
    add_prog(title, desc, 'international', 'drama', mins, "", "TV-MA", 2021)

# News extra
for title, desc, mins in NEWS_EXTRA:
    add_prog(title, desc, 'news', 'general', mins, "", "TV-PG", 2026, True)

# Sports studio extra
for title, desc, mins in SPORTS_STUDIO_EXTRA:
    add_prog(title, desc, 'sports', 'studio', mins, "", "TV-PG", 2026, True)

# Save
with open('data/channels.json', 'w') as f:
    json.dump(channels, f, indent=1)
with open('data/programs.json', 'w') as f:
    json.dump(programs, f, indent=1)
# Copy to web
import shutil, os
os.makedirs('web/data', exist_ok=True)
shutil.copy('data/channels.json', 'web/data/channels.json')
shutil.copy('data/programs.json', 'web/data/programs.json')

print(f"wrote channels.json: {len(channels)} real networks")
print(f"wrote programs.json: {len(programs)} programs ({len([p for p in programs if p['poster']])} with posters)")
