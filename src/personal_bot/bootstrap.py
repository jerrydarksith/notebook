from personal_bot.config import load_application_settings
from personal_bot.db.database import Database
from personal_bot.db.schema import initialize_database_schema


def run_application() -> None:
    application_settings = load_application_settings()
    database = Database(application_settings.database_path)

    try:
        initialize_database_schema(database)
    finally:
        database.close()

    print("Початкову структуру бази даних створено.")

