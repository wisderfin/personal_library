from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy import create_engine
from settings import settings
from app.models import Base, User


class Connect():
    def __init__(self):
        engine = create_engine(f'postgresql://{settings.USER}:{settings.PASSWORD}@{settings.HOST}:{settings.PORT}/{settings.DB}')
        Base.metadata.bind = engine
        self.DBSession = sessionmaker(bind=engine)

    @contextmanager
    def session(self):
        with self.DBSession() as session:
            yield session

    def create_user(self, user):
        with self.session() as session:
            session.add(user)
            session.commit()

    def search_user(self, user):
        with self.session() as session:
            return session.query(User).filter_by(login=user.login).first()

    def check_login(self, username):
        with self.session() as session:
            return session.query(User).filter_by(login=username).first()
