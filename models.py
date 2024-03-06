import atexit
from abc import ABC
import datetime

from sqlalchemy import create_engine, String, DateTime, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

POSTEGRES_PASSWORD = ''
POSTEGRES_USER = ''
POSTEGRES_DB = ''
POSTEGRES_HOST = ''
POSTEGRES_PORT = ''

BD_post = f'postgresql://{POSTEGRES_USER}:{POSTEGRES_PASSWORD}@{POSTEGRES_HOST}:{POSTEGRES_PORT}/{POSTEGRES_DB}'
engine = create_engine(BD_post, echo=True)

Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    tittle: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    create_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    author: Mapped[str]

    @property
    def create_dict(self):
        return {
            'id': self.id,
            'tittle': self.tittle,
            'description': self.description,
            'author': self.author,
            'create_at': self.create_at.isoformat()
        }


# Base.metadata.create_all(bind=engine)