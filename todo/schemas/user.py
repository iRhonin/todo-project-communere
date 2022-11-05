from .camel_model import CamelModel
from .timestamp import TimestampSchema


class UserDto(CamelModel):
    username: str
    password: str


class UserSchema(UserDto, TimestampSchema):
    username: str
    id: int
    type: str

    class Config:
        fields = {'password': {'exclude': True}}
