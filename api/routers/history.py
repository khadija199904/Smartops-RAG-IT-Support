from fastapi import APIRouter ,Depends
from api.dependencies import get_db
from sqlalchemy.orm import Session
from models.queries import Query


router = APIRouter()


@router.get("history")
async def user_history(db: Session = Depends(get_db)):

    interactions = db.query(Query.question, Query.answer).order_by(Query.created_at.desc()).all()
    history = [
        {
            "question": item.question, 
            "answer": item.answer
        } 
        for item in interactions
    ]

    return history




