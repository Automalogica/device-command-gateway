import logging
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from sqlalchemy.dialects.postgresql import insert
 
from src.services.database.models import CameraCommand, CommandStatus

logger = logging.getLogger(__name__)


class CommandCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session


    async def insert_command(
        self,
        request_id: str,
        camera_id: str,
        command: str,
        params: str | None = None,
    ) -> None:
        """Persists new command with status PENDING"""
        self._session.add(
            CameraCommand(
                request_id=request_id,
                camera_id=camera_id,
                command=command,
                params=params,
                status=CommandStatus.PENDING,
                created_at=datetime.now(timezone.utc),
            )
        )
        await self._session.commit()
        logger.debug("INSERT | request_id=%s status=PENDING", request_id)

    async def update_status(
        self,
        request_id: str,
        status: CommandStatus,
        error_message: str | None = None,
    ) -> None:
        """Update status of command and timestamps"""
        now = datetime.now(timezone.utc)

        values: dict = {"status": status}

        if status == CommandStatus.PROCESSING:
            values["started_at"] = now
        elif status in (CommandStatus.DONE, CommandStatus.ERROR, CommandStatus.DLQ):
            values["finished_at"] = now

        if error_message is not None:
            values["error_message"] = error_message

        await self._session.execute(
            update(CameraCommand)
            .where(CameraCommand.request_id == request_id)
            .values(**values)
        )
        await self._session.commit()
        logger.debug("UPDATE | request_id=%s status=%s", request_id, status)

    async def increment_retry(self, request_id: str) -> int:
        """Increment retry_count and returns updated value"""
        result = await self._session.execute(
            select(CameraCommand)
            .where(CameraCommand.request_id == request_id)
            .with_for_update()
        )
        cmd = result.scalar_one()
        cmd.retry_count += 1
        await self._session.commit()
        logger.debug("RETRY | request_id=%s retry_count=%s", request_id, cmd.retry_count)
        return cmd.retry_count


    async def poll_pending(self) -> CameraCommand | None:
        """
        Search next command PENDING using SELECT FOR UPDATES SKIP LOCKED.
        Ensures that two workers never process the same command simultaneously.

        The transaction must remain open until processing is complete — 
        the commit or rollback must be done by the caller via update_status.
        """
        result = await self._session.execute(
            select(CameraCommand)
            .where(CameraCommand.status == CommandStatus.PENDING)
            .order_by(CameraCommand.created_at)
            .limit(1)
            .with_for_update(skip_locked=True)
        )
        return result.scalar_one_or_none()
    