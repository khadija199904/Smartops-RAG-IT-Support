import mlflow
import mlflow.langchain
import time
from pipelineRAG.retrieval import build_rag_chain, MODEL_NAME, TEMPERATURE, TOP_K, system_prompt
from api.core.config import EMBEDDING_MODEL_NAME

mlflow.set_tracking_uri("http://localhost:5000") 
mlflow.set_experiment("Smartops-RAG-IT-Support")

_rag_chain = None

def get_chain():
    global _rag_chain
    if _rag_chain is None:
        print("Initialisation de la chaîne RAG...")
        _rag_chain = build_rag_chain()
    return _rag_chain




def query_rag_service(question_text):
    
    chain = get_chain()
    with mlflow.start_run():
        #  Log des Paramètres
        mlflow.log_params({
            "model_name": MODEL_NAME,
            "temperature": TEMPERATURE,
            "top_k": TOP_K,
            "embedding_model": EMBEDDING_MODEL_NAME,
            "system_prompt": system_prompt
        })

        # Latence
        start_time = time.time()
        
        # Exécution de la chaîne
        result = chain.invoke({"query": question_text})
        
        latency = time.time() - start_time

        #Métriques
        mlflow.log_metric("latency", latency)
        
        #  Log des Inputs/Outputs (Traces)
        mlflow.log_param("question", question_text)
        mlflow.log_text(result["result"], "response.txt")
        
        # Log des sources (chunks utilisés)
        sources = [doc.page_content for doc in result.get("source_documents", [])]
        mlflow.log_text("\n---\n".join(sources), "context_chunks.txt")

      
        mlflow.langchain.log_model(
            lc_model=chain,
            artifact_path="rag_pipeline",
            registered_model_name="Smartops-RAG-Model"
        )

        print(f"Réponse générée en {latency:.2f}s")
        return result

    return result


if __name__ == "__main__":
  query = 'Comment configurer mon VPN pour le télétravail ?'
  query_rag_service(query)
