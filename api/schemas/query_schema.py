from pydantic import BaseModel 
from datetime import datetime


class QueryBase(BaseModel):
    question :str
    


class QueryRequest(QueryBase):
     pass

class QueryResponce(QueryBase):
     id : int
     latency_ms: int
     created_at:datetime
     user_id:int