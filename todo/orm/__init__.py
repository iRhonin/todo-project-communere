from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.schema import MetaData

from .base_model import BaseModel
from .mixins import TimestampMixin

metadata = MetaData()

base: BaseModel = declarative_base(cls=BaseModel, metadata=metadata)

session_factory = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=True,
    twophase=False,
)
session = scoped_session(session_factory)


def create_engine(url, *args, **kwargs):
    return sa_create_engine(url, pool_pre_ping=True, *args, **kwargs)


def setup_schema(session_):
    engine = session_.bind
    metadata.create_all(bind=engine)


def init_model(engine):
    session.remove()
    session.configure(bind=engine)


def safe_commit(session):
    try:
        session.commit()
    except:
        session.rollback()
        raise
