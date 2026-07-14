from personal_bot.core.entities.user import User
from personal_bot.core.enums import UserRole, UserStatus
from personal_bot.db.database import Database


class UserRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def find_by_telegram_id(self, telegram_id: int) -> User | None:
        user_row = self._database.execute(
            """
            SELECT id, telegram_id, role, status
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,),
        ).fetchone()

        if user_row is None:
            return None

        return User(
            id=user_row["id"],
            telegram_id=user_row["telegram_id"],
            role=UserRole(user_row["role"]),
            status=UserStatus(user_row["status"]),
        )

    def has_any_users(self) -> bool:
        user_row = self._database.execute("SELECT 1 FROM users LIMIT 1").fetchone()
        return user_row is not None

    def create(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        phone_number: str,
        role: UserRole,
        status: UserStatus,
        created_at: str,
    ) -> int:
        cursor = self._database.execute(
            """
            INSERT INTO users (
                telegram_id,
                username,
                first_name,
                last_name,
                phone_number,
                role,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                telegram_id,
                username,
                first_name,
                last_name,
                phone_number,
                role.value,
                status.value,
                created_at,
                created_at,
            ),
        )
        return cursor.lastrowid
