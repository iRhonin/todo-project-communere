from argon2 import PasswordHasher
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.orm import synonym

from todo.orm import TimestampMixin
from todo.orm import base
from todo.roles import Roles


class Task(base, TimestampMixin):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship('Project', foreign_keys=[project_id], back_populates='tasks')

    developers = relationship(
        'Developer',
        secondary='tasks_developers',
        back_populates='tasks',
    )


class TaskDeveloper(base, TimestampMixin):
    __tablename__ = 'tasks_developers'

    developer_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True,
        nullable=False,
    )

    task_id = Column(
        Integer,
        ForeignKey('tasks.id'),
        primary_key=True,
        nullable=False,
    )
