from pydantic import BaseModel as PydanticBase

from todo.utils import to_camel


class CamelModel(PydanticBase):
    class Config:
        orm_mode = True
        extra = 'ignore'
        alias_generator = to_camel
        allow_population_by_field_name = True
