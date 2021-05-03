import sys
from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import settings as app_settings

working_engine = create_engine(app_settings.DB_CONNECTION)
WorkingSession = sessionmaker(bind=working_engine)

testing_engine = create_engine(app_settings.TESTING_DB_CONNECTION)
TestingSession = sessionmaker(bind=testing_engine)


@contextmanager
def open_db_session(with_commit=False) -> ContextManager[Session]:
    session = WorkingSession()
    if 'pytest' in sys.modules:
        session = TestingSession()
    try:
        yield session
        if with_commit:
            session.commit()
    except:
        session.rollback()
        raise

    session.close()
