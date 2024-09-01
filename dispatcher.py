from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from commands import check_link, start, button_handler

# Your bot token here
TOKEN = '7481510974:AAG0pPCCCpBIU3zVy7EZoTNapuBDauUWEug'

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_link))
    application.add_handler(CallbackQueryHandler(button_handler))



    application.run_polling()

if __name__ == '__main__':
    main()
