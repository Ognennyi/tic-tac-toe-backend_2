from dataclasses import dataclass
from uuid import UUID




@dataclass
class Leaderboard:
    user_id: UUID
    win_ratio: float