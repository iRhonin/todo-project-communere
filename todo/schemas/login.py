from .camel_model import CamelModel
from .tokens import TokensSchema


class LoginSchema(CamelModel):
    username: str
    password: str


class LoginResultSchema(TokensSchema):
    pass
