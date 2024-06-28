from pydoc import Doc
from pydantic import BaseModel
from beanie import Document


# Define a Pydantic model
class Users(Document):
    user_id: int
    user_name: str | None
    first_name: str | None
    last_name: str | None
    time_offset: int


class Word(Document):
    send_word: str
    right_word: str


class UserWord(Document):
    user_id: int
    success: bool | None
    time: float | None
    word: Word


class UserTests(Document):
    user_id: int
    stage: int  # -1 when test already past, else position of the word to write
    words: list[UserWord]
    time_start: float
    time_end: float | None


class UserSending(Document):
    user_id: int
    time: float
    # data: {str: str} TODO:
