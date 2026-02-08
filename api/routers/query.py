from fastapi import APIRouter ,Depends , HTTPException, status
from sqlalchemy.orm import Session
from api.schemas.query_schema import QueryRequest ,QueryData
from api.services.rag_service import query_rag_service
from api.services.clustering_service import clustering_query
from api.dependencies import get_db ,get_current_user
from api.models.queries import Query
from api.models.users import USER
import logging


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post('/query')
async def ask_query(request : QueryRequest,db : Session = Depends(get_db),current_user: USER = Depends(get_current_user)):
    try:
        userid = current_user.id
        question = request.question

        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La question ne peut pas être vide"
            )

        # --- Appel RAG ---
        try:
            full_response, latency_ms = query_rag_service(question)
            response_text = full_response.get("result", "")
        except Exception as e:
            logger.error(f"Erreur RAG: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erreur lors de la génération de la réponse"
            )

        # --- Clustering ---
        try:
            cluster_id = clustering_query(question)
        except Exception as e:
            logger.error(f"Erreur clustering: {e}")
            cluster_id = None  # on continue même si clustering échoue

        # --- Préparation des données ---
        query_data = QueryData(
            user_id=userid,
            question=question,
            answer=response_text,
            cluster=cluster_id,
            latency_ms=latency_ms
        ).dict()

        query_entry = Query(**query_data)
      
        db.add(query_entry)
        db.commit()
        db.refresh(query_entry)
    
    
   
        return { "clustre": cluster_id,
            "reponse": response_text,
           }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur interne du serveur"
        )