from datetime import datetime

from .camel_model import CamelModel


class TimestampSchema(CamelModel):
    created_at: datetime
    updated_at: datetime