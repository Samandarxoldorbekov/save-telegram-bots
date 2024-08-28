from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands import check_link, start

# Your bot token here
TOKEN = '7452238296:AAFnS1SfDT4P-27sZFa2Xoeua3eI3X5NwRQ'

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))

    application.run_polling()

if __name__ == '__main__':
    main()
