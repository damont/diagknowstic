from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
import re

SQLALCHEMY_DATABASE_URL = "sqlite:///./alert_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _cc2jl(string):
    REGEX = r'(.(?:[^a-z_]+(?=[A-Z_]|$)|[^A-Z_]+))'
    def _jl_match(match):
        group = match.group()
        prefix = bool(match.start() and not group.startswith('_'))
        return '_' * prefix + group.lower()

    return re.subn(REGEX, _jl_match, string)[0]


class SABase(object):
    
    @declared_attr
    def __tablename__(cls):
        return _cc2jl(cls.__name__)

    @classmethod
    def get_or_create(cls, session, **kwargs):
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    post_time = Column(DateTime, server_default=func.now())
    

Base = declarative_base(cls=SABase)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()