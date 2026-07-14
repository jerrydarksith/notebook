from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class ApplicationSettings:
    database_path: Path


def load_application_settings() -> ApplicationSettings:
    load_dotenv()
    database_path_value = os.getenv("DATABASE_PATH", "data/personal_bot.sqlite3")

    return ApplicationSettings(database_path=Path(database_path_value))

