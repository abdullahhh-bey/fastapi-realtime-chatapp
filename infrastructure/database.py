from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#simpler, no password needed
DATABASE_URL = "mssql+pyodbc://DESKTOP-JOGOILA\\SQLEXPRESS01/mydatabase?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(
    DATABASE_URL,
    echo=True, #it shows sql queries in the console
)

#it will make local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Dependency injection function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()