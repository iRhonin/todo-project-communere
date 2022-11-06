from typing import List
from typing import Optional

from pydantic import constr

from .camel_model import CamelModel
from .timestamp import TimestampSchema
from .user import UserSchema


class TaskDto(CamelModel):
    name: constr(strip_whitespace=True, max_length=32)
    project_id: int


class TaskSchema(TaskDto, TimestampSchema):
    id: int
    developers: List[UserSchema]


class AssignTaskDto(CamelModel):
    developer_id: int


class ListProjectTasksQuery(CamelModel):
    developer_id: Optional[int]
