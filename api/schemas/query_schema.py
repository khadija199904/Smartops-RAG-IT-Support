from pydantic import BaseModel 
from datetime import datetime


class QueryBase(BaseModel):
    question :str
    


class QueryRequest(QueryBase):
     pass

class QueryData(BaseModel):
    user_id: int
    question: str
    answer: str
    cluster: int      
    latency_ms: float


class QueryResponce(QueryBase):
     id : int
     latency_ms: int
     created_at:datetime
     user_id:int