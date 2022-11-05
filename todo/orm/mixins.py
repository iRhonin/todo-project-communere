from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column, DateTime


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


@sa.event.listens_for(TimestampMixin, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    # When a model with a timestamp is updated; force update the updated
    # timestamp.
    target.updated_at = datetime.utcnow()
