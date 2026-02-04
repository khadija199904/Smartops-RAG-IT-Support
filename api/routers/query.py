from fastapi import APIRouter
from api.schemas.query_schema import QueryRequest
from api.services.rag_service import query_rag_service
from api.services.clustering_service import clustring_query

router = APIRouter()

@router.post('/query')
async def ask_query(question : QueryRequest):

  reponse = query_rag_service(question)
  cluster_id = clustring_query(question)
  print (cluster_id)
  return reponse 
