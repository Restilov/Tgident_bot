import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN", "")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.WARNING
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Identity Bot!\n\n"
        "Send me any message and I'll show you your full Telegram identity details.\n\n"
        "Commands:\n"
        "/start — Show this message\n"
        "/info  — Show your identity details"
    )


async def show_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user      = update.effective_user
    chat      = update.effective_chat
    msg       = update.effective_message
    username  = f"@{user.username}" if user.username else "—"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "—"
    lang      = user.language_code or "—"
    is_bot    = "Yes" if user.is_bot else "No"
    is_premium= "Yes" if getattr(user, "is_premium", False) else "No"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    reply = (
        "─────────────────────────\n"
        "     IDENTITY REPORT     \n"
        "─────────────────────────\n"
        "\n"
        "👤  USER\n"
        f"    Full name    : {full_name}\n"
        f"    Username     : {username}\n"
        f"    User ID      : {user.id}\n"
        f"    Language     : {lang}\n"
        f"    Bot account  : {is_bot}\n"
        f"    Premium      : {is_premium}\n"
        "\n"
        "💬  CHAT\n"
        f"    Chat ID      : {chat.id}\n"
        f"    Chat type    : {chat.type}\n"
        f"    Chat title   : {getattr(chat, 'title', None) or '—'}\n"
        "\n"
        "📨  MESSAGE\n"
        f"    Message ID   : {msg.message_id}\n"
        f"    Date         : {timestamp}\n"
        "\n"
        "─────────────────────────"
    )

    await update.message.reply_text(reply)


def main():
    if not TOKEN:
        print("Error: TOKEN environment variable is not set.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", show_info))
    app.add_handler(MessageHandler(filters.ALL, show_info))

    print("Identity Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
