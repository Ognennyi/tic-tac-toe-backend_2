
from uuid import UUID

from datasource.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import DateTime

from datetime import datetime

class Game(Base):
    __tablename__ = "games"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    board: Mapped[list[list[int]]] = mapped_column(JSONB, nullable=False)

    player_1_id: Mapped[UUID] = mapped_column()
    player_2_id: Mapped[UUID | None] = mapped_column()
    game_status: Mapped[str] = mapped_column()
    current_turn_id: Mapped[UUID | None] = mapped_column() #Тот кто должен сходить
    winner_id: Mapped[UUID | None] = mapped_column()
    player_1_symbol: Mapped[int] = mapped_column()
    player_2_symbol: Mapped[int] = mapped_column()
    is_computer_game: Mapped[bool] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)