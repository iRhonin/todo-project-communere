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


class Project(base, TimestampMixin):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(32), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship(
        'ProductManager', foreign_keys=[owner_id], back_populates='owned_projects'
    )

    team_members = relationship(
        'Developer',
        secondary='team_members',
        back_populates='projects',
    )

    tasks = relationship(
        'Task',
        back_populates='project',
    )
