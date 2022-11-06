from argon2 import PasswordHasher
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.orm import synonym

from todo.orm import TimestampMixin
from todo.orm import base
from todo.roles import Roles


class User(base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Unicode(32), nullable=False)
    _password = Column(Unicode, nullable=False)
    type = Column(Unicode(32), nullable=False)

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""

        ph = PasswordHasher()
        self._password = ph.hash(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym(
        '_password',
        descriptor=property(_get_password, _set_password),
        info=dict(protected=True),
    )

    def validate_password(self, password):
        ph = PasswordHasher()
        return ph.verify(self.password, password)

    __mapper_args__ = {
        'polymorphic_on': type,
    }


class Developer(User):
    projects = relationship(
        'Project',
        secondary='team_members',
        back_populates='team_members',
    )

    tasks = relationship(
        'Task',
        secondary='tasks_developers',
        back_populates='developers',
    )

    __mapper_args__ = {
        'polymorphic_identity': Roles.DEVELOPER,
    }


class ProductManager(Developer):
    owned_projects = relationship('Project', back_populates='owner')

    __mapper_args__ = {
        'polymorphic_identity': Roles.PRODUCT_MANAGER,
    }
