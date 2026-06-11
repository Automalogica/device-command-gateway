import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, SmallInteger, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CommandStatus(str, enum.Enum):
    PENDING    = "PENDING"
    PROCESSING = "PROCESSING"
    DONE       = "DONE"
    ERROR      = "ERROR"
    DLQ        = "DLQ"


class CameraCommand(Base):
    __tablename__ = "camera_commands"

    id            : Mapped[int]            = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    request_id    : Mapped[str]            = mapped_column(String(100), nullable=False, unique=True, index=True)
    camera_id     : Mapped[str]            = mapped_column(String(100), nullable=False)
    command       : Mapped[str]            = mapped_column(String(50),  nullable=False)
    params        : Mapped[str | None]     = mapped_column(Text)
    status        : Mapped[CommandStatus]  = mapped_column(
                                                Enum(CommandStatus, name="command_status"),
                                                nullable=False,
                                                default=CommandStatus.PENDING,
                                            )
    retry_count   : Mapped[int]            = mapped_column(SmallInteger, nullable=False, default=0)
    error_message : Mapped[str | None]     = mapped_column(Text)
    created_at    : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    started_at    : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at   : Mapped[datetime | None] = mapped_column(DateTime(timezone=True))