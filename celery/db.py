import yaml
from sqlalchemy import Column, Integer, String, create_engine, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

with open("db.yaml", 'r', encoding="utf-8") as f:
    data = yaml.safe_load(f)

DATABASE_URL = data['url']

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class LoginValid(Base):
    __tablename__ = "login_valid"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_pass = Column(String(300), unique=True, index=True)
    jet_used = Column(Boolean, default=False)
    check_date = Column(DateTime)
