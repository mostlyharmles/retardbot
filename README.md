# retardbot

![Gumby](https://github.com/mostlyharmles/retardbot/blob/main/img/gumby.png)  
**The most based, unhinged, Gumby-powered chaos bot on Discord.**  
*“You are 69% retarded!” — every server ever*

Prefix-only (`!`) Discord bot that turns your server into a 4chan-adjacent meme hellscape with token gambling, degenerate glazing, and passive retard radar.

---

## ✨ What It Does

- **Passive Retard Radar** — Scans every message for "retard/tard/cringe/based" and instantly roasts the user with a random percentage.
- **Token Economy** — Everyone gets +100 tokens daily (welfare). Gamble them in blackjack. Hit 0 and you get the "Poor" role.
- **Degenerate Commands**:
  - `!glaze` — Cover any image in random cum pics (random position/rotation/opacity).
  - `!faces` — Draws rectangles on every detected face.
  - `!gifitize` — Turns any video into a janky 10fps GIF.
- Full interactive **blackjack** (`!bj` / `!blackjack`).
- Classic stuff: `!gumby`, `!ascii`, `!hello`, etc.
- Admin tools for token management and resets.

---

## 📋 All Commands

| Command              | Aliases              | Description |
|----------------------|----------------------|-----------|
| `!commands`          | -                    | This list |
| `!hello` / `!source` | -                    | Basics |
| `!gumby` / `!ascii`  | -                    | Gumby spam |
| `!gumby` (image)     | -                    | Random meme pic |
| `!glaze`             | -                    | Glaze an image (5s cooldown) |
| `!faces`             | -                    | Face detection |
| `!gifitize`          | -                    | Video → GIF |
| `!check_tokens`      | -                    | Your balance |
| `!next_welfare`      | -                    | Time until payout |
| `!blackjack`         | `!bj !whitejack !wj` | Gamble tokens |
| `!give_tokens` etc.  | -                    | Owner-only admin commands |

**Token Economy**: +100 daily. Lose in blackjack, win big. Poor role auto-applied at 0 tokens.

---

## 🚀 Setup (Arch Edition)

1. `git clone https://github.com/mostlyharmles/retardbot.git && cd retardbot`
2. `uv sync` (or `pip install -r requirements.txt`)
3. Copy `.env.example` → `.env` and fill in your token + IDs
4. `uv run python main.py`

**Pro move**: Make a systemd service so it runs forever (I can give you the exact file if you want).

---

**Tech**: discord.py + Pillow + moviepy + SQLite  
**Warning**: somewhat unhinged. Contains slurs, NSFW glazing folder.

Made with pure retardation by gumby🖤  
