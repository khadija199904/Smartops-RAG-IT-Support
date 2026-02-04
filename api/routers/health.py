import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db 
from langchain_groq import ChatGroq

router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    health_report = {
        "timestamp": time.time(),
        "status": "healthy",
        "components": {}
    }

    #  Test Base de données (Queries)
    try:
        db.execute(text("SELECT 1"))
        health_report["components"]["database"] = "up"
    except Exception:
        health_report["components"]["database"] = "down"
        health_report["status"] = "unhealthy"

    # Test Vector Store (ChromaDB)
    try:
        from pipelineRAG.vectorstore import load_vector_db
        db_vector = load_vector_db()
        if db_vector:
            health_report["components"]["vector_db"] = "up"
    except Exception:
        health_report["components"]["vector_db"] = "down"
        health_report["status"] = "degraded"

    return health_report