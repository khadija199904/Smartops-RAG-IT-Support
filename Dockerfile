FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./data/chroma_db ./pipelineRAG ./ml/models_saved/ /app/
CMD ["sh","-c","sleep 5 && uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"]


