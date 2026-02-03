from fastapi import FastAPI
from api.routers import auth , query,history,health
from api.database import Base,engine


app  = FastAPI(title = "Smart Assistant IT RAG")

Base.metadata.create_all(bind=engine)

# Routes
app.include_router(auth.router)
app.include_router(query.router)
app.include_router(history.router)
app.include_router(health.router)

