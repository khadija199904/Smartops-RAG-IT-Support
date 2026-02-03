from fastapi import APIRouter


app = APIRouter()


@app.get("history")
async def user_history():
    return


