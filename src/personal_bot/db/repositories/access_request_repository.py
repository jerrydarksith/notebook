from personal_bot.core.enums import AccessRequestStatus
from personal_bot.db.database import Database


class AccessRequestRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def create_pending(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        last_name: str | None,
        phone_number: str,
        created_at: str,
    ) -> int:
        cursor = self._database.execute(
            """
            INSERT INTO access_requests (
                telegram_id,
                username,
                first_name,
                last_name,
                phone_number,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                telegram_id,
                username,
                first_name,
                last_name,
                phone_number,
                AccessRequestStatus.PENDING.value,
                created_at,
            ),
        )
        return cursor.lastrowid

    def has_pending_for_telegram_id(self, telegram_id: int) -> bool:
        access_request_row = self._database.execute(
            """
            SELECT 1
            FROM access_requests
            WHERE telegram_id = ? AND status = ?
            LIMIT 1
            """,
            (telegram_id, AccessRequestStatus.PENDING.value),
        ).fetchone()
        return access_request_row is not None
