from pydantic import constr

from .camel_model import CamelModel
from .timestamp import TimestampSchema
from .user import UserSchema


class TeamMemberDto(CamelModel):
    developer_id: int
    project_id: int


class TeamMemberSchema(TeamMemberDto, TimestampSchema):
    pass
