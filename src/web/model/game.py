from dataclasses import dataclass
from uuid import UUID
from web.model.board import WebBoard

@dataclass
class WebGame:
    id: UUID
    board: WebBoard