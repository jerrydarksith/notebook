from personal_bot.config import load_application_settings
from personal_bot.access.service import AccessService
from personal_bot.db.database import Database
from personal_bot.db.repositories.access_request_repository import AccessRequestRepository
from personal_bot.db.repositories.settings_repository import SettingsRepository
from personal_bot.db.repositories.user_repository import UserRepository
from personal_bot.db.schema import initialize_database_schema
from personal_bot.telegram.application import create_telegram_application


def run_application() -> None:
    application_settings = load_application_settings()
    database = Database(application_settings.database_path)

    try:
        initialize_database_schema(database)
        user_repository = UserRepository(database)
        settings_repository = SettingsRepository(database)
        access_request_repository = AccessRequestRepository(database)
        access_service = AccessService(
            database,
            user_repository,
            settings_repository,
            access_request_repository,
        )
        telegram_application = create_telegram_application(
            application_settings.telegram_bot_token,
            access_service,
        )
        telegram_application.run_polling()
    finally:
        database.close()
