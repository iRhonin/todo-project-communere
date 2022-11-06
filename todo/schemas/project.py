from pydantic import constr

from .camel_model import CamelModel
from .timestamp import TimestampSchema
from .user import UserSchema


class ProjectDto(CamelModel):
    name: constr(strip_whitespace=True, max_length=32)


class ProjectSchema(ProjectDto, TimestampSchema):
    id: int
    owner: UserSchema
