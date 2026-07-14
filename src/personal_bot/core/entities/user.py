from dataclasses import dataclass

from personal_bot.core.enums import UserRole, UserStatus


@dataclass(frozen=True)
class User:
    id: int
    telegram_id: int
    role: UserRole
    status: UserStatus
