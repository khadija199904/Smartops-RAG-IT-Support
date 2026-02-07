import mlflow
import time
from pipelineRAG.retrieval import build_rag_chain, MODEL_NAME, TEMPERATURE, TOP_K, system_prompt
from api.core.config import EMBEDDING_MODEL_NAME ,MLFLOW_TRACKING_URI
from api.utils.mlflow_track import track_rag_inference





_rag_chain = None

def get_chain():
    global _rag_chain
    if _rag_chain is None:
        print("Initialisation de la chaîne RAG...")
        _rag_chain = build_rag_chain()
    return _rag_chain




def query_rag_service(question_text):
    
    chain = get_chain()

    with mlflow.start_run(run_name="rag_inference"):
        
        # Exécution de la requête
        start_time = time.time()
        result = chain.invoke({"query":  question_text})
        latency = time.time() - start_time
        latency_ms = round((latency * 1000),2)
        # Extraction des données
        response_text = result["result"]
        source_docs = result.get("source_documents", [])
        
        # Tracking MLflow (fonction du script)
        run_id = track_rag_inference(
            llm_model=MODEL_NAME,
            temperature=TEMPERATURE,
            top_k=TOP_K,
            embedding_model=EMBEDDING_MODEL_NAME,
            system_prompt=system_prompt,
            user_question=question_text,
            response_text=response_text,
            source_docs=source_docs,
            latency=latency
        )
        
        
        return result,latency_ms

    


if __name__ == "__main__":
  query = 'Quelle est la procédure pour un problème de connexion réseau ?'
  query_rag_service(query)
