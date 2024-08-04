from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine


URL = "sqlite:///./task_two/e_comm_db.db"
engine = create_engine(url=URL, connect_args={"check_same_thread": False})
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def db_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
