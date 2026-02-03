from fastapi import APIRouter


app = APIRouter()


@app.get("health")
async def serive_health():

    return