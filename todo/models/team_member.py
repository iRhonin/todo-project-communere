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


class TeamMember(base, TimestampMixin):
    __tablename__ = 'team_members'

    developer_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True,
        nullable=False,
    )

    project_id = Column(
        Integer,
        ForeignKey('projects.id'),
        primary_key=True,
        nullable=False,
    )
