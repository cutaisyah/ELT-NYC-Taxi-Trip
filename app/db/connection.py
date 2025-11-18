from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import DB_URL

def get_db_connection():
    engine = create_engine(DB_URL, echo=True)
    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True
    )
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()