from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field

from .game import GameDTO


class UserDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    games: List[GameDTO] = Field(default_factory=list)
