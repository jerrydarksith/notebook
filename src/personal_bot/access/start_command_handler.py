from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from personal_bot.access.service import AccessService
from personal_bot.core.enums import UserStatus
from personal_bot.telegram.menus.main_menu import get_main_menu_message


class StartCommandHandler:
    def __init__(self, access_service: AccessService) -> None:
        self._access_service = access_service

    async def handle(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        del context
        telegram_user = update.effective_user
        message = update.effective_message

        if telegram_user is None or message is None:
            return

        user = self._access_service.find_user_by_telegram_id(telegram_user.id)

        if user is None:
            await message.reply_text(
                "Щоб отримати доступ, подайте заявку та поділіться номером телефону.",
                reply_markup=self._create_phone_number_keyboard(),
            )
            return

        if user.status is UserStatus.ACTIVE:
            await message.reply_text(get_main_menu_message())
            return

        await message.reply_text("Ваш доступ до бота заблоковано.")

    @staticmethod
    def _create_phone_number_keyboard() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            [[KeyboardButton("Поділитися номером телефону", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
