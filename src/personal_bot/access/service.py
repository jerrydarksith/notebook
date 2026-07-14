from datetime import datetime, timezone

from personal_bot.core.entities.user import User
from personal_bot.core.enums import ContactRegistrationResult, UserRole, UserStatus
from personal_bot.db.database import Database
from personal_bot.db.repositories.access_request_repository import AccessRequestRepository
from personal_bot.db.repositories.settings_repository import SettingsRepository
from personal_bot.db.repositories.user_repository import UserRepository


class AccessService:
    def __init__(
        self,
        database: Database,
        user_repository: UserRepository,
        settings_repository: SettingsRepository,
        access_request_repository: AccessRequestRepository,
    ) -> None:
        self._database = database
        self._user_repository = user_repository
        self._settings_repository = settings_repository
        self._access_request_repository = access_request_repository

    def find_user_by_telegram_id(self, telegram_id: int) -> User | None:
        return self._user_repository.find_by_telegram_id(telegram_id)

    def register_contact(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        phone_number: str,
    ) -> ContactRegistrationResult:
        created_at = datetime.now(timezone.utc).isoformat()

        with self._database.transaction():
            existing_user = self._user_repository.find_by_telegram_id(telegram_id)

            if existing_user is not None:
                return ContactRegistrationResult.USER_ALREADY_REGISTERED

            if not self._user_repository.has_any_users():
                user_id = self._user_repository.create(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    role=UserRole.SUPER_ADMIN,
                    status=UserStatus.ACTIVE,
                    created_at=created_at,
                )
                self._settings_repository.create_default(user_id, created_at)
                return ContactRegistrationResult.FIRST_SUPER_ADMIN_CREATED

            if self._access_request_repository.has_pending_for_telegram_id(telegram_id):
                return ContactRegistrationResult.ACCESS_REQUEST_ALREADY_PENDING

            self._access_request_repository.create_pending(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                created_at=created_at,
            )
            return ContactRegistrationResult.ACCESS_REQUEST_CREATED
