import os, re, time
from collections import defaultdict
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

# Prefer environment variable for security
BOT_TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

# Regex to catch Instagram links
INSTAGRAM_REGEX = re.compile(r"(https?://(?:www\.)?instagram\.com/[^\s]+)")

# Simple anti-spam memory
last = defaultdict(float)

def extract_url(text: str) -> str | None:
    if not text:
        return None
    m = INSTAGRAM_REGEX.search(text)
    return m.group(1) if m else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا! صيفط لي أي لينك ديال Instagram (Reel/Video/Post) ونعطيك التحميل 🎥\n"
        "✅ خاص الفيديو يكون عمومي (Public).\n"
        "📎 مثال: https://www.instagram.com/reel/XXXXXXXX/"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📎 صيفط الرابط ديال Instagram، وأنا نرجع ليك الفيديو. خاص المنشور يكون Public.")

def extract_download_url(ig_url: str) -> str | None:
    # Use yt-dlp to fetch a direct media URL without downloading the file
    ydl_opts = {
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        "format": "mp4[height<=720]/mp4/best",
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(ig_url, download=False)
        # Handle playlists/carousels
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        # Prefer direct URL if present
        if info.get("url"):
            return info["url"]
        # Fallback to iterating formats
        for f in reversed(info.get("formats", [])):
            if f.get("url") and f.get("ext") in ("mp4", "mov"):
                return f["url"]
    return None

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user_id = msg.from_user.id
    now = time.time()

    # Rate limit (5 seconds between requests per user)
    if now - last[user_id] < 5:
        await msg.reply_text("⏳ واحد الشوية باش مانكونوش سبام.")
        return
    last[user_id] = now

    url = extract_url(msg.text or "")
    if not url:
        await msg.reply_text("📎 صيفط لينك صحيح ديال Instagram.")
        return

    await msg.reply_text("⏳ كنوجد ليك الفيديو…")
    try:
        dl_url = extract_download_url(url)
        if dl_url:
            await msg.reply_video(dl_url, caption="✅ تفضّل الفيديو.\n@YourBotName")
        else:
            await msg.reply_text("❌ ماقدرتش نستخرج الفيديو. تأكد أنه Public وجرب لينك آخر.")
    except Exception as e:
        await msg.reply_text("❌ وقع خطأ فالاستخراج. جرّب من جديد أو فيديو آخر (Public).")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "PUT_YOUR_TOKEN_HERE":
        raise SystemExit("❌ Set BOT_TOKEN environment variable before running.")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
