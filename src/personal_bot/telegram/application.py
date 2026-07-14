from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from personal_bot.access.contact_message_handler import ContactMessageHandler
from personal_bot.access.service import AccessService
from personal_bot.access.start_command_handler import StartCommandHandler


def create_telegram_application(
    telegram_bot_token: str,
    access_service: AccessService,
) -> Application:
    telegram_application = ApplicationBuilder().token(telegram_bot_token).build()
    start_command_handler = StartCommandHandler(access_service)
    contact_message_handler = ContactMessageHandler(access_service)
    telegram_application.add_handler(
        CommandHandler("start", start_command_handler.handle)
    )
    telegram_application.add_handler(
        MessageHandler(filters.CONTACT, contact_message_handler.handle)
    )

    return telegram_application
