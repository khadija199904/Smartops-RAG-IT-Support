
from pipelineRAG.ingestion import ingestion_preparation
from pipelineRAG.vectorstore import create_and_store_embeddings




chunks = ingestion_preparation()
vecteur = create_and_store_embeddings(chunks)
