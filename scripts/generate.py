#!/usr/bin/env python3
"""Generate synthetic EPG data: 100 channels, program catalog, 10 viewer agents.
Stdlib only. Output: data/channels.json, data/programs.json, data/agents.json
"""
import json, random, os

random.seed(42)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")

# ---------------------------------------------------------------- channels
# (name, genre, subgenre hint)
CHANNEL_DEFS = [
    # Sports (20)
    ("Gridiron Network", "sports", "football"), ("Hoops TV", "sports", "basketball"),
    ("Pitchside", "sports", "soccer"), ("Grand Slam Tennis", "sports", "tennis"),
    ("Fairway Channel", "sports", "golf"), ("Octane Racing", "sports", "racing"),
    ("Fight Night TV", "sports", "combat"), ("Rinkside", "sports", "hockey"),
    ("Diamond Nine", "sports", "baseball"), ("Olympic Channel Plus", "sports", "olympics"),
    ("Outdoor Pursuit", "sports", "outdoor"), ("Esports Arena", "sports", "esports"),
    ("SportsCenter 24", "sports", "news"), ("The Blitz", "sports", "football"),
    ("Courtside Classics", "sports", "basketball"), ("World Football Daily", "sports", "soccer"),
    ("Marathon TV", "sports", "running"), ("Sail & Surf", "sports", "watersports"),
    ("College GameDay Net", "sports", "college"), ("Pro Wrestling Vault", "sports", "wrestling"),
    # News (12)
    ("Meridian News", "news", "national"), ("Capital Wire", "news", "politics"),
    ("Business First", "news", "business"), ("StormWatch", "news", "weather"),
    ("Global Lens", "news", "international"), ("Morning Briefing", "news", "morning"),
    ("Nightline News", "news", "evening"), ("TechTicker", "news", "tech"),
    ("HealthLine Daily", "news", "health"), ("Rural Radio TV", "news", "regional"),
    ("Financial Edge", "news", "markets"), ("Documentary Now News", "news", "investigative"),
    # Movies (12)
    ("Silver Screen", "movies", "classics"), ("Action Max", "movies", "action"),
    ("Indie Frame", "movies", "indie"), ("Family Flicks", "movies", "family"),
    ("Noir Alley", "movies", "noir"), ("Blockbuster Nights", "movies", "blockbuster"),
    ("World Cinema", "movies", "foreign"), ("RomCom Central", "movies", "romance"),
    ("SciFi Odyssey", "movies", "scifi"), ("Horror After Dark", "movies", "horror"),
    ("Western Frontier", "movies", "western"), ("Animated Worlds", "movies", "animation"),
    # Kids (10)
    ("Sunny Patch", "kids", "preschool"), ("Rocket Kids", "kids", "adventure"),
    ("Toon Lagoon", "kids", "cartoons"), ("Junior Chefs", "kids", "cooking"),
    ("Dino Discovery", "kids", "educational"), ("Pixel Play", "kids", "gaming"),
    ("Storybook Time", "kids", "stories"), ("Animal Pals", "kids", "animals"),
    ("Super Squad", "kids", "superhero"), ("Craft Corner", "kids", "crafts"),
    # Entertainment (12)
    ("Primetime Drama", "entertainment", "drama"), ("Laugh Track", "entertainment", "comedy"),
    ("Reality Realm", "entertainment", "reality"), ("Soap Opera Net", "entertainment", "soap"),
    ("Crime & Justice", "entertainment", "crime"), ("Talk Tonight", "entertainment", "talk"),
    ("Variety Hour", "entertainment", "variety"), ("Game Show Central", "entertainment", "gameshow"),
    ("Talent Quest", "entertainment", "talent"), ("Dating After Dark", "entertainment", "dating"),
    ("Sitcom Classics", "entertainment", "sitcom"), ("Drama Vault", "entertainment", "drama"),
    # Documentary (10)
    ("Terra Wild", "documentary", "nature"), ("Empires of History", "documentary", "history"),
    ("Quantum Leap Docs", "documentary", "science"), ("True Crime Files", "documentary", "truecrime"),
    ("Deep Ocean", "documentary", "nature"), ("Ancient Mysteries", "documentary", "history"),
    ("Space Frontier", "documentary", "space"), ("Human Story", "documentary", "biography"),
    ("Engineering Marvels", "documentary", "engineering"), ("Food Origins", "documentary", "food"),
    # Lifestyle (10)
    ("Sizzle Kitchen", "lifestyle", "food"), ("Wanderlust", "lifestyle", "travel"),
    ("Dream Home", "lifestyle", "home"), ("Fit Life", "lifestyle", "fitness"),
    ("Garden Glory", "lifestyle", "garden"), ("Style Studio", "lifestyle", "fashion"),
    ("Brew Masters", "lifestyle", "drinks"), ("Pet Perfect", "lifestyle", "pets"),
    ("Mindful Living", "lifestyle", "wellness"), ("DIY Workshop", "lifestyle", "diy"),
    # Music (6)
    ("Top 40 Countdown", "music", "pop"), ("Country Roads", "music", "country"),
    ("Hip Hop Nation", "music", "hiphop"), ("Classical Reverie", "music", "classical"),
    ("Rock Anthology", "music", "rock"), ("Jazz After Hours", "music", "jazz"),
    # International (8)
    ("Masala Prime", "international", "hindi"), ("Telenovela Pasion", "international", "spanish"),
    ("K-Drama Wave", "international", "korean"), ("Euro News 24", "international", "european"),
    ("Nollywood Nights", "international", "african"), ("Anime Nexus", "international", "japanese"),
    ("Mandarin Horizon", "international", "chinese"), ("Arabic Star", "international", "arabic"),
]

channels = []
for i, (name, genre, sub) in enumerate(CHANNEL_DEFS):
    channels.append({
        "id": f"ch{i+1:03d}",
        "name": name,
        "number": 101 + i,
        "genre": genre,
        "subgenre": sub,
        "language": "es" if sub == "spanish" else "hi" if sub == "hindi" else "en",
    })
assert len(channels) == 100, len(channels)

# ---------------------------------------------------------------- programs
# Realistic fictional program templates per genre: (title, description, mins)
def sports_programs():
    out = []
    leagues = [
        ("Gridiron", "football", [
            ("Chicago Bears", "chi"), ("Dallas Cowboys", "dal"), ("Seattle Seahawks", "sea"),
            ("Miami Dolphins", "mia"), ("Denver Broncos", "den"), ("New England Patriots", "ne")]),
        ("Hoops", "basketball", [
            ("LA Lakers", "lal"), ("Chicago Bulls", "chi"), ("New York Knicks", "nyk"),
            ("Houston Rockets", "hou"), ("Phoenix Suns", "phx"), ("Boston Celtics", "bos")]),
        ("Soccer", "soccer", [
            ("LA Galaxy", "lag"), ("Seattle Sounders", "sea"), ("Portland Timbers", "por"),
            ("Inter Miami", "mia"), ("Austin FC", "aus"), ("NY Red Bulls", "ny")]),
        ("Tennis", "tennis", ["Grand Slam"]), ("Golf", "golf", ["PGA-style"]), ("Racing", "racing", ["Grand Prix"]),
    ]
    # Live games: (title, desc, mins, subgenre)
    for league, subgenre, teams in leagues:
        if len(teams) < 2 or isinstance(teams[0], str): continue
        for _ in range(14):
            a, b = random.sample([t[0] for t in teams], 2)
            out.append((f"{league}: {a} vs {b}",
                        f"Live {league.lower()} action as {a} take on {b}. Expert commentary and analysis.",
                        random.choice([120, 150, 180]), subgenre))
    # Team logo map (ESPN CDN)
    TEAM_LOGOS = {
        "football": {abbr: f"https://a.espncdn.com/i/teamlogos/nfl/500/{abbr}.png" for _, abbr in leagues[0][2]},
        "basketball": {abbr: f"https://a.espncdn.com/i/teamlogos/nba/500/{abbr}.png" for _, abbr in leagues[1][2]},
    }
    # Save team data for frontend
    import os
    os.makedirs("web/data", exist_ok=True)
    team_data = {}
    for league, subgenre, teams in leagues[:3]:
        for name, abbr in teams:
            logo = TEAM_LOGOS.get(subgenre, {}).get(abbr, "")
            team_data[name] = {"abbr": abbr, "sport": subgenre, "logo": logo}
    with open("web/data/teams.json", "w") as f:
        json.dump(team_data, f, indent=1)
    print(f"wrote teams.json: {len(team_data)} teams")
    shows = [
        ("The Blitz: Pregame", "Pregame breakdown with insider predictions and injury reports.", 60),
        ("Postgame Wrap", "Highlights, interviews, and analysis from today's games.", 60),
        ("Inside the Huddle", "Behind-the-scenes access with players and coaches.", 30),
        ("Trade Rumor Mill", "The latest buzz on trades, signings, and roster moves.", 30),
        ("Draft Preview Special", "Scouting reports on the top prospects entering the draft.", 120),
        ("Championship Classics", "Relive the greatest championship games in history.", 120),
        ("SportsCenter 24: Morning Edition", "Overnight scores, highlights, and the day ahead in sports.", 120),
        ("The Coaches Room", "X's and O's breakdown with former head coaches.", 30),
        ("Fantasy Fix", "Start/sit advice and waiver wire targets for your fantasy lineup.", 30),
        ("Olympic Dreams", "Profiles of athletes chasing gold at the upcoming games.", 60),
        ("Marathon: City Run Live", "Live coverage of the annual city marathon from start to finish.", 180),
        ("Surf Championship Tour", "The world's best surfers battle in pumping waves.", 120),
        ("Esports Arena: Grand Final", "The championship final with a $2M prize pool on the line.", 180),
        ("Fight Night: Main Event", "Live undercard and main event from the arena.", 180),
        ("College GameDay Live", "The crew breaks down the biggest college matchups of the week.", 120),
    ]
    out += shows
    return out

def news_programs():
    base = [
        ("Meridian Morning", "Top stories, weather, and traffic to start your day.", 120),
        ("The Noon Report", "Midday headlines and developing stories.", 60),
        ("Capital Wire Tonight", "Inside politics with interviews from Capitol Hill.", 60),
        ("Business First AM", "Markets open, earnings, and the day in business.", 60),
        ("Closing Bell Recap", "Wall Street's close and what moved the markets.", 60),
        ("StormWatch Live", "Tracking severe weather across the country.", 30),
        ("Global Lens", "International headlines with correspondents worldwide.", 60),
        ("The Investigators", "In-depth reporting on stories that matter.", 60),
        ("TechTicker Daily", "Silicon Valley news, gadgets, and AI breakthroughs.", 30),
        ("HealthLine", "Medical news and wellness advice from top doctors.", 30),
        ("Nightline News", "The day's top stories and tomorrow's headlines.", 60),
        ("Weekend Roundup", "The week's biggest stories in review.", 120),
    ]
    extra = [
        ("Dawn Patrol", "Early headlines before the markets open.", 60),
        ("The Situation Room Live", "Breaking news as it happens.", 120),
        ("Market Movers", "Stocks making waves and why.", 30),
        ("Weather Now", "Your local forecast, updated hourly.", 30),
        ("The Diplomat", "Foreign policy and global summits explained.", 60),
        ("City Hall", "Local politics and community issues.", 30),
        ("The Science Desk", "Breakthroughs in science and medicine.", 30),
        ("Election Central", "Polls, projections, and campaign trail news.", 120),
        ("The Green Report", "Climate news and sustainability.", 30),
        ("Sports Business Daily", "The money behind the games.", 30),
        ("Overnight Desk", "News from around the world while you slept.", 60),
        ("The Interview", "One-on-one with newsmakers.", 60),
    ]
    return base + extra

def movie_programs():
    films = [
        ("The Last Horizon", "A retired pilot takes one final flight across the Atlantic.", 125, "2019"),
        ("Midnight in Marrakech", "A jewel thief's last heist goes sideways in Morocco.", 110, "2021"),
        ("The Cartographer's Daughter", "A young mapmaker uncovers a centuries-old conspiracy.", 135, "2018"),
        ("Neon Requiem", "A detective hunts a rogue android in 2087 Neo-Tokyo.", 120, "2022"),
        ("The Beekeeper's War", "Two rival honey farms feud in rural Provence.", 95, "2020"),
        ("Starlight Expressway", "Truckers race across the desert with mysterious cargo.", 105, "2017"),
        ("The Glass Observatory", "Astronomers discover a signal from deep space.", 130, "2023"),
        ("Second Chances Diner", "A struggling chef inherits a roadside diner.", 100, "2019"),
        ("The Forgery", "An art forger is blackmailed into one last job.", 115, "2021"),
        ("Tides of Fortune", "Fishermen battle a storm and each other off the Maine coast.", 125, "2016"),
        ("The Quantum Thief", "A hacker steals memories in a digital heist.", 118, "2024"),
        ("Harvest Moon Rising", "A city lawyer returns to save the family farm.", 102, "2020"),
        ("The Silent Auction", "Bidders compete for a painting with a dark secret.", 108, "2022"),
        ("Ironwood", "A blacksmith forges a legendary sword in medieval Wales.", 140, "2018"),
        ("The Lighthouse Keeper's Son", "A boy rows to a haunted lighthouse every night.", 96, "2023"),
        ("Crimson Meridian", "A spy thriller across three continents.", 122, "2021"),
        ("The Winter Countess", "A noblewoman hides refugees in WWII Vienna.", 138, "2019"),
        ("Paper Moon Rising", "Jazz musicians chase a dream in 1950s New Orleans.", 112, "2022"),
        ("The Long Commute", "A comedy about the world's worst train ride.", 98, "2023"),
        ("Echoes of Tomorrow", "Time travelers fix a broken timeline.", 128, "2024"),
        ("The Salt Road", "A caravan crosses the desert with precious cargo.", 132, "2017"),
        ("Murder at the Regatta", "A detective investigates at a sailing race.", 104, "2020"),
        ("The Backup Singer", "She finally gets her shot at stardom.", 106, "2021"),
        ("Glacier Run", "Rescuers race a blizzard in the Alps.", 116, "2019"),
        ("The Diplomat's Wife", "Espionage and romance in Cold War Berlin.", 124, "2018"),
        ("Jukebox Heroes", "A tribute band becomes the real thing.", 110, "2022"),
        ("The Orchard", "Three sisters reunite at the family orchard.", 100, "2023"),
        ("Deep Cover Blues", "An undercover cop infiltrates a jazz club.", 114, "2020"),
        ("The Last Drive-In", "Teens save their town's drive-in theater.", 96, "2021"),
        ("Starfall", "A comet brings strangers together in a small town.", 108, "2024"),
    ]
    return [(t, d, m) for t, d, m, _y in films]

def kids_programs():
    return [
        ("Sunny Patch Pals", "Pip and friends learn sharing on Sunny Patch Farm.", 30),
        ("Rocket Rangers", "Kid astronauts explore the solar system.", 30),
        ("Dino Discovery", "Paleontologist Penny digs up dinosaur adventures.", 30),
        ("Toon Lagoon", "Wacky cartoons from the lagoon crew.", 60),
        ("Junior Chefs: Bake Off", "Kid chefs compete in sweet challenges.", 60),
        ("Super Squad", "Teen heroes protect Metro City.", 30),
        ("Animal Pals Rescue", "Vets save animals around the world.", 30),
        ("Storybook Time", "Classic tales come alive with animation.", 30),
        ("Pixel Play Live", "Kid gamers take on epic challenges.", 60),
        ("Craft Corner", "DIY crafts and art projects for kids.", 30),
        ("The Wonder Workshop", "Inventors build amazing gadgets.", 30),
        ("Pirate Pups", "Puppy pirates sail the seven seas.", 30),
        ("Math Quest", "Heroes solve puzzles to save numbers.", 30),
        ("The Giggle Gang", "Silly sketches and songs for kids.", 30),
        ("Space Pioneers Jr.", "Young cadets train for Mars.", 30),
        ("Fairy Tale Theater", "Enchanted stories on stage.", 60),
        ("Robot Friends", "A boy and his robot best friend.", 30),
        ("The Nature Nuts", "Kids explore forests and rivers.", 30),
        ("Baking Buddies", "Easy recipes kids can make.", 30),
        ("Dragon Academy", "Young riders train baby dragons.", 30),
    ]

def entertainment_programs():
    return [
        ("Harbor Lights", "A coastal town's secrets surface after a storm.", 60),
        ("The Night Shift", "ER doctors navigate chaos and romance.", 60),
        ("Laugh Riot", "Stand-up's biggest names take the stage.", 60),
        ("The Mansion", "Twelve strangers compete for $1M in a mansion.", 90),
        ("Cold Case Unit", "Detectives reopen a 20-year-old disappearance.", 60),
        ("Talk Tonight with Mara Voss", "Celebrity interviews and comedy sketches.", 60),
        ("Spin the Wheel", "Contestants spin for cash and prizes.", 60),
        ("The Proposal", "Real proposals, real tears, real joy.", 60),
        ("Sitcom Rewind: The 90s", "Classic 90s sitcom marathon.", 120),
        ("The Talent Stage: Finale", "The winner takes $500K and a record deal.", 120),
        ("Soap: Endless Summer", "Love triangles on the California coast.", 60),
        ("Variety Spectacular", "Music, magic, and comedy in one show.", 90),
        ("The Penthouse", "Wealth, betrayal, and skyscraper drama.", 60),
        ("Comedy Cellar Live", "Uncensored stand-up from NYC.", 60),
        ("The Escape Room", "Celebrities race the clock in themed rooms.", 60),
        ("Island of Temptation", "Couples test their love on a tropical island.", 90),
        ("The Rookie Lawyer", "A 40-year-old starts over at a law firm.", 60),
        ("Late Night with Danny Cole", "Monologue, guests, and house band.", 60),
        ("The Cooking Duel", "Chefs battle in timed challenges.", 60),
        ("Mystery Manor", "A reality whodunit in a haunted mansion.", 90),
        ("The Apartment Hunt", "House hunters in the big city.", 30),
        ("Stand-Up Spotlight", "Rising comics, one mic.", 30),
        ("The Family Business", "A deli dynasty fights to survive.", 60),
        ("Quiz Kings", "Trivia titans face off for $250K.", 60),
    ]

def documentary_programs():
    return [
        ("Planet Wild: Savannah", "Lions, elephants, and the circle of life.", 60),
        ("Empires: Rome", "The rise and fall of the Roman Empire.", 60),
        ("The Quantum World", "Physicists probe the nature of reality.", 60),
        ("Cold Case: The Vanishing", "A true crime investigation.", 60),
        ("Deep Blue: Abyss", "Submersibles explore the ocean's depths.", 60),
        ("Secrets of the Pyramids", "New scans reveal hidden chambers.", 60),
        ("Mission to Mars", "Engineers build the first Mars habitat.", 60),
        ("The Inventor's Story", "Biography of a world-changing inventor.", 90),
        ("Bridges of the World", "Engineering marvels spanning rivers.", 60),
        ("The Spice Trail", "How spices shaped world history.", 60),
        ("Planet Wild: Arctic", "Polar bears in a melting world.", 60),
        ("Empires: The Ottomans", "Six centuries of sultans.", 60),
        ("The AI Revolution", "How machines learned to think.", 60),
        ("Heist: The Museum Job", "The greatest art theft ever.", 90),
        ("Volcano Worlds", "Eruptions captured in stunning detail.", 60),
        ("The Silk Road", "Merchants and empires of the ancient trade route.", 60),
        ("Inside the Mind", "Neuroscientists map consciousness.", 60),
        ("The Lost Fleet", "Divers find a WWII armada.", 60),
        ("Skyscraper: One Year", "Building a tower in 12 months.", 60),
        ("The Chocolate Story", "From bean to bar.", 60),
    ]

def lifestyle_programs():
    return [
        ("Sizzle: 30-Minute Meals", "Fast, delicious weeknight cooking.", 30),
        ("Wanderlust: Kyoto", "Temples, tea houses, and neon streets.", 60),
        ("Dream Home Makeover", "A dated ranch becomes a modern showpiece.", 60),
        ("Fit Life: HIIT Blast", "High-intensity workout with trainer Jess.", 30),
        ("Garden Glory", "Transform your backyard into paradise.", 30),
        ("Style Studio", "Fashion trends and wardrobe rescues.", 30),
        ("Brew Masters", "Inside America's best craft breweries.", 30),
        ("Pet Perfect", "Training tips for happy dogs.", 30),
        ("Mindful Mornings", "Meditation and wellness to start the day.", 30),
        ("DIY Workshop", "Build a farmhouse table from scratch.", 60),
        ("Sizzle: Street Food World", "Tacos, dumplings, and night markets.", 60),
        ("Wanderlust: Patagonia", "Glaciers and peaks at the end of the world.", 60),
        ("Tiny House Hunters", "Living large in 400 square feet.", 30),
        ("Yoga Flow", "Morning vinyasa for all levels.", 30),
        ("The Cocktail Lab", "Craft cocktails with master mixologists.", 30),
        ("Rescue My Garden", "Landscapers save dying yards.", 60),
        ("Thrift Flip", "Turning thrift finds into treasures.", 30),
        ("The Pasta Project", "Handmade pasta from three regions of Italy.", 60),
        ("Adventure Eats: Peru", "Ceviche to cuy in Lima and Cusco.", 60),
        ("Strength & Stretch", "Full-body strength training.", 30),
    ]

def music_programs():
    return [
        ("Top 40 Countdown", "This week's biggest hits.", 120),
        ("Country Roads Live", "Live from the Grand Ole stage.", 90),
        ("Hip Hop Nation", "The hottest tracks and videos.", 60),
        ("Classical Reverie", "Beethoven's Ninth with the Philharmonic.", 90),
        ("Rock Anthology", "Four decades of rock legends.", 60),
        ("Jazz After Hours", "Smooth late-night jazz sessions.", 60),
        ("Pop Vault: 2000s", "The hits that defined a decade.", 60),
        ("Unplugged Sessions", "Stripped-down acoustic performances.", 60),
        ("EDM Universe", "Festival sets from the main stage.", 120),
        ("Soul Train Rewind", "Classic soul and R&B performances.", 60),
        ("Indie Spotlight", "Breaking artists to watch.", 30),
        ("Metal Mayhem", "The heaviest riffs on TV.", 60),
    ]

def international_programs():
    return [
        ("Masala Prime: Drama Hour", "Family saga from Mumbai.", 60),
        ("Pasion de Amor", "Telenovela of love and betrayal.", 60),
        ("K-Drama: Seoul Hearts", "Romance in the K-pop world.", 70),
        ("Euro News Tonight", "European headlines in English.", 30),
        ("Nollywood Nights", "Lagos drama and comedy.", 90),
        ("Anime Nexus", "New episodes from Japan.", 30),
        ("Mandarin Horizon", "Drama from Shanghai.", 60),
        ("Arabic Star Variety", "Music and talk from Dubai.", 90),
        ("Masala Prime: Comedy Nights", "Stand-up from Mumbai's best.", 60),
        ("Corazon Valiente", "A fearless journalist fights corruption.", 60),
        ("K-Drama: The Heirs", "Chaebol family power struggles.", 70),
        ("Euro Football Weekly", "Champions League highlights.", 60),
        ("Lagos Market Days", "Comedy from Nigeria's markets.", 60),
        ("Samurai Chronicles", "Anime epic of feudal Japan.", 30),
        ("The Bund", "Crime drama in 1930s Shanghai.", 60),
        ("Desert Rose", "Drama from the Gulf.", 60),
    ]

GENRE_BUILDERS = {
    "sports": sports_programs, "news": news_programs, "movies": movie_programs,
    "kids": kids_programs, "entertainment": entertainment_programs,
    "documentary": documentary_programs, "lifestyle": lifestyle_programs,
    "music": music_programs, "international": international_programs,
}

programs = []
pid = 1
for ch in channels:
    builder = GENRE_BUILDERS[ch["genre"]]
    for item in builder():
        # sports games carry their own subgenre (4-tuple); others use channel's
        if len(item) == 4:
            title, desc, mins, sub = item
        else:
            title, desc, mins = item
            sub = ch["subgenre"]
        programs.append({
            "id": f"p{pid:05d}",
            "title": title.strip(),
            "desc": desc,
            "genre": ch["genre"],
            "subgenre": sub,
            "duration_min": mins,
            "rating": random.choice(["TV-G", "TV-PG", "TV-14", "TV-MA"]) if ch["genre"] in ("movies", "entertainment") else "TV-PG",
            "year": random.randint(2015, 2026),
            "live": "Live" in title or "live" in desc.lower(),
        })
        pid += 1

# Dedupe identical titles (same builder reused across channels of same genre)
seen = set()
unique = []
for p in programs:
    if p["title"] not in seen:
        seen.add(p["title"])
        unique.append(p)
programs = unique
# Re-id
for i, p in enumerate(programs):
    p["id"] = f"p{i+1:05d}"

print(f"channels: {len(channels)}, programs: {len(programs)}")

# ---------------------------------------------------------------- agents
AGENTS = [
    {"id": "a01", "name": "Marcus 'Coach' Bell", "tagline": "Lives for game day",
     "genres": {"sports": 0.95, "news": 0.4, "movies": 0.3, "entertainment": 0.3},
     "fav_sports": ["football", "basketball", "baseball"],
     "watch_hours": [17, 18, 19, 20, 21, 22]},
    {"id": "a02", "name": "Sarah Chen", "tagline": "News before coffee",
     "genres": {"news": 0.95, "documentary": 0.6, "entertainment": 0.3},
     "fav_sports": [],
     "watch_hours": [6, 7, 8, 12, 18, 22]},
    {"id": "a03", "name": "Priya Nair", "tagline": "Mom of two, queen of the remote",
     "genres": {"kids": 0.95, "movies": 0.6, "lifestyle": 0.5},
     "fav_sports": [],
     "watch_hours": [7, 8, 16, 17, 19, 20]},
    {"id": "a04", "name": "James Whitfield", "tagline": "Film snob, proudly",
     "genres": {"movies": 0.95, "documentary": 0.6, "entertainment": 0.4},
     "fav_sports": [],
     "watch_hours": [20, 21, 22, 23]},
    {"id": "a05", "name": "Ashley Rivera", "tagline": "Reality TV is my sport",
     "genres": {"entertainment": 0.95, "music": 0.5, "lifestyle": 0.4},
     "fav_sports": [],
     "watch_hours": [19, 20, 21, 22]},
    {"id": "a06", "name": "David Okafor", "tagline": "Documentaries or nothing",
     "genres": {"documentary": 0.95, "news": 0.5, "movies": 0.4},
     "fav_sports": ["olympics"],
     "watch_hours": [20, 21, 22]},
    {"id": "a07", "name": "Maria Santos", "tagline": "Always hungry for content",
     "genres": {"lifestyle": 0.95, "entertainment": 0.5, "international": 0.4},
     "fav_sports": ["soccer"],
     "watch_hours": [11, 12, 18, 19, 20]},
    {"id": "a08", "name": "Raj Patel", "tagline": "Desi at heart, global in taste",
     "genres": {"international": 0.95, "sports": 0.6, "movies": 0.5},
     "fav_sports": ["soccer", "tennis"],
     "watch_hours": [19, 20, 21, 22]},
    {"id": "a09", "name": "Chris Novak", "tagline": "Night owl comedy nerd",
     "genres": {"entertainment": 0.9, "music": 0.5, "sports": 0.3},
     "fav_sports": ["esports"],
     "watch_hours": [21, 22, 23, 0, 1]},
    {"id": "a10", "name": "Emma Larsen", "tagline": "Up at 5, zen by 9",
     "genres": {"lifestyle": 0.9, "documentary": 0.5, "news": 0.4},
     "fav_sports": ["running", "tennis"],
     "watch_hours": [5, 6, 7, 18, 19]},
]

# ---------------------------------------------------------------- write
os.makedirs(DATA, exist_ok=True)
for name, obj in [("channels.json", channels), ("programs.json", programs), ("agents.json", AGENTS)]:
    with open(os.path.join(DATA, name), "w") as f:
        json.dump(obj, f, indent=1)
    print(f"wrote {name}: {len(obj)} records")
