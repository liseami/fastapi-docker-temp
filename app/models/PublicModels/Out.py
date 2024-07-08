
from sqlmodel import SQLModel


class RespMod(SQLModel):
    message: str = ""
    code: int = 200
    data: dict | str | None | list = {}


class ErrorMod(Exception):
    def __init__(self, message: str):
        self.message = message
