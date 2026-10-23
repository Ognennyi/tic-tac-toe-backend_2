import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker



env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

db_password = os.getenv("DB_PASSWORD")

if db_password is None:
    raise RuntimeError("Не задан DB_PASSWORD")


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password=db_password,
    host="localhost",
    port=5432,
    database="tic_tac_toe"
)



engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass




