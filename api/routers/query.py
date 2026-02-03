from fastapi import APIRouter

app = APIRouter()

@app.post('/query')
async def ask_query():

  return
