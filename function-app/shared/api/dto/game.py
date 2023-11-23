from pydantic import BaseModel


class GameDTO(BaseModel):
    id: str
    name: str
