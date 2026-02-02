from sqlalchemy import create_engine 
from api.core.config import DATABASE_URL
from sqlalchemy.orm import declarative_base


engine= create_engine(DATABASE_URL)

Base = declarative_base

