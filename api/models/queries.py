from sqlalchemy import Column, Integer,ForeignKey , DateTime,func ,Text
from api.database import Base
from sqlalchemy.orm import relationship

class Query(Base):
  __tablename__ = "queries"

  id = Column(Integer,primary_key=True)
  user_id = Column(Integer,ForeignKey('users.id'))
  question = Column(Text,nullable=False)
  answer = Column(Text)
  cluster = Column(Integer)
  latency_ms = Column(Integer)
  created_at = Column(DateTime, server_default=func.now())
  
  owner = relationship("USER",back_populates="queries")