from telegram import Update
from telegram.ext import ContextTypes

from personal_bot.access.service import AccessService
from personal_bot.core.enums import ContactRegistrationResult
from personal_bot.telegram.menus.main_menu import get_main_menu_message


class ContactMessageHandler:
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

        if telegram_user is None or message is None or message.contact is None:
            return

        contact = message.contact

        if not self.is_contact_owned_by_telegram_user(
            contact.user_id,
            telegram_user.id,
        ):
            await message.reply_text(
                "Можна надсилати лише власний номер телефону."
            )
            return

        registration_result = self._access_service.register_contact(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name,
            phone_number=contact.phone_number,
        )

        if registration_result is ContactRegistrationResult.FIRST_SUPER_ADMIN_CREATED:
            await message.reply_text(
                "Вас зареєстровано як Super Admin.\n\n"
                f"{get_main_menu_message()}"
            )
            return

        if registration_result is ContactRegistrationResult.USER_ALREADY_REGISTERED:
            await message.reply_text(get_main_menu_message())
            return

        if registration_result is ContactRegistrationResult.ACCESS_REQUEST_ALREADY_PENDING:
            await message.reply_text(
                "Ваша заявка вже отримана.\n"
                "Вона очікує підтвердження адміністратора."
            )
            return

        await message.reply_text(
            "Вашу заявку отримано.\n"
            "Вона очікує підтвердження адміністратора."
        )

    @staticmethod
    def is_contact_owned_by_telegram_user(
        contact_user_id: int | None,
        telegram_user_id: int,
    ) -> bool:
        return contact_user_id == telegram_user_id
