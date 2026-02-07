from fastapi import APIRouter ,Depends ,HTTPException
from api.dependencies import get_db
from sqlalchemy.orm import Session
from api.models.queries import Query
from api.models.users import USER
from api.dependencies import get_current_user

router = APIRouter()


@router.get("/history")
async def user_history(db: Session = Depends(get_db),current_user: USER = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
    
    try:
        
        interactions = (
            db.query(Query.question, Query.answer)
            .filter(Query.user_id == current_user.id)
            .order_by(Query.created_at.desc())
            .all()
        )

        
        if not interactions:
            return {"message": "Aucune interaction trouvée pour cet utilisateur."}

       
        history = [
            {
                "question": item.question,
                "answer": item.answer
            }
            for item in interactions
        ]

        return history

    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")




