from pydantic import BaseModel 
from datetime import datetime


class QueryBase(BaseModel):
    question :str
    latency_ms: int


class QueryCreate(QueryBase):
     pass

class Query(QueryBase):
     id : int
     created_at:datetime
     user_id:int