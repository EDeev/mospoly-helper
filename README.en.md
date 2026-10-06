# MosPolyHelper

[Русский](README.md) · **English**

[![CI](https://github.com/EDeev/mospoly-helper/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/mospoly-helper/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/EDeev/mospoly-helper)](https://github.com/EDeev/mospoly-helper/releases)

A Telegram bot that sends a video route to a classroom in Moscow Polytechnic University buildings: pick a
campus, type the room number and get a video note with the way from the campus gate or from the building
entrance.

**Status:** team coursework (project practice, Moscow Polytech, group 241-327, 2025), completed · bot
[@MosPoly_Helperbot](https://t.me/MosPoly_Helperbot)

**Stack:** Python 3.10 · aiogram 3 · MoviePy 2 · FFmpeg · Docker

## Features

- Five campuses: Bolshaya Semyonovskaya, Pavla Korchagina, Pryanishnikova, Mikhalkovskaya, Avtozavodskaya
- A route from the campus gate or the building entrance: the clip is assembled from "building → floor →
  room" fragments, sped up 2× and encoded for Telegram (H.264, 1500k)
- Finished clips are cached and repeat requests are instant; `combine.py` pre-builds the cache
- Room number validation with hints when the format or campus doesn't match

Videos were filmed for the Pryanishnikova buildings (76 rooms) and partly for Avtozavodskaya; for other
campuses the bot replies that the route isn't available yet and suggests writing by email.

## Running

```bash
git clone https://github.com/EDeev/mospoly-helper.git && cd mospoly-helper
cp .env.example .env      # BOT_TOKEN from @BotFather
docker compose up -d
```

**Prebuilt image** (videos inside, the route cache is built on the fly):

```bash
docker run -d -e BOT_TOKEN=token -v mospoly-cache:/app/src/data/cache -v mospoly-users:/app/src/data/users ghcr.io/edeev/mospoly-helper
```

(same as `git.deev.su/edeev/mospoly-helper`).

Without Docker: Python 3.10+, FFmpeg, `pip install -r requirements.txt`, then
`cd src/code && BOT_TOKEN=… python bot.py`. More in [QUICKSTART.md](QUICKSTART.md) and [DOCKER.md](DOCKER.md) (in Russian).

> [!NOTE]
> The repository holds about 220 video clips (sources and cache), so it is over 500 MB.

## License

Coursework (project practice, Moscow Polytechnic University, 2025). The code is open for study; there is
no separate license.

## Authors

- **Egor Deev** — [GitHub](https://github.com/EDeev)
- **Petr Saprykin** — [GitHub](https://github.com/PetrSaprykin)
- **Ruslan Starkov** — [GitHub](https://github.com/RayStar-k)

---

<div align="center">
  <sub>⭐ If you find this project useful, give it a star on GitHub!</sub>
  <p><sub>Made with ❤️ by Moscow Polytech students, group 241-327</sub></p>
</div>
