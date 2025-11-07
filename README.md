# Insta Saver Telegram Bot (Free)

Bot kaykhddm b Telegram: katssift lih lien dyal Instagram (Reel/Video/Post) u kayrj3 lik lien dyal telechargement aw yssift lik video f Telegram.

## 1) Local run (Free)
```bash
git clone YOUR_REPO_URL insta_saver_bot
cd insta_saver_bot
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# hll BOT_TOKEN f .env b token jdid mn BotFather
export $(grep -v '^#' .env | xargs)  # Windows: set BOT_TOKEN=...
python main.py
```

## 2) Deploy on Render (Free Worker)
1. Dir repo f GitHub w upload had files.
2. Render.com → New → **Worker** → choose repo.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python main.py`
5. Environment → Add `BOT_TOKEN` (mn BotFather `/token`), 7alla `/revoke` bach tbdel lqdim ila tcharaka.
6. Create Worker → mlli ykml, jarrb lbott f Telegram.

## Commands
- `/start`  : instructions + welcome
- `/help`   : kifash tsta3ml

## Notes
- Khddam ghir m3a videos PUBLIC.
- Hada ghyr lta3lim; i7trm 7uquq nashr.
- T9dar tzid TikTok/YouTube b nafs `yt-dlp` bla ta tdbil kbir.
