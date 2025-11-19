from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


DATABASE_URL = (
    "mssql+pyodbc://DESKTOP-JOGOILA\\SQLEXPRESS01/ActiveUsers"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    future=True,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
