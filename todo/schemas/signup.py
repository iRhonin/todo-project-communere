from .camel_model import CamelModel
from .tokens import TokensSchema
from .user import UserSchema


class SignupResultSchema(CamelModel):
    user: UserSchema
    tokens: TokensSchema
