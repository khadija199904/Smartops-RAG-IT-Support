import os
import mlflow
from api.core.config import MLFLOW_TRACKING_URI
import tempfile

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Smartops-RAG-IT-Support")


def log_text_as_artifact(text: str, artifact_name: str, artifact_path: str = None):
    """
    Log du texte long comme artifact MLflow.

    """
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, artifact_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        mlflow.log_artifact(file_path, artifact_path=artifact_path)

def log_rag_params(llm_model, temperature, top_k, embedding_model):
    """Log les paramètres du modèle"""
    mlflow.log_params({
        "llm_model": llm_model,
        "temperature": temperature,
        "top_k": top_k,
        "embedding_model": embedding_model
    })


def log_prompts(system_prompt, user_question):
    """Log les prompts utilisés"""
    
    mlflow.log_param("user_question", user_question)
    log_text_as_artifact(system_prompt, "system_prompt.txt", artifact_path="prompts")



def log_rag_metrics(latency, source_docs):
    """Log les métriques de performance"""
    
    # Calcul des scores de similarité
    scores = [doc.metadata.get("score", 0) for doc in source_docs]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    mlflow.log_metrics({
        "latency_ms": latency,
        "avg_similarity_score": avg_score
    })


def log_rag_outputs(response_text, source_docs):
    """Log la réponse générée et les chunks"""
    
    # Réponse
    log_text_as_artifact(response_text, "generated_response.txt", artifact_path="outputs")
    
    # Chunks avec métadonnées
    chunks_info = []
    for i, doc in enumerate(source_docs):
        chunk_text = f"=== CHUNK {i+1} ===\n"
        chunk_text += f"Score: {doc.metadata.get('score', 'N/A')}\n"
        chunk_text += f"Content:\n{doc.page_content}\n\n"
        chunks_info.append(chunk_text)
   
    if chunks_info:
        log_text_as_artifact("".join(chunks_info), "chunks.txt", artifact_path="outputs")


def track_rag_inference(llm_model, temperature, top_k, embedding_model, 
                        system_prompt, user_question, 
                        response_text, source_docs, latency):
    """
    Fonction complète pour tracker une inférence RAG

    """
    
    # Log paramètres
    log_rag_params(llm_model, temperature, top_k, embedding_model)
    
    # Log prompts
    log_prompts(system_prompt, user_question)
    
    # Log métriques
    log_rag_metrics(latency, source_docs)
    
    # Log outputs
    log_rag_outputs(response_text, source_docs)
    
    # Log du Run ID
    run_id = mlflow.active_run().info.run_id
    print(f" Tracking MLflow - Run ID: {run_id}")
    
    return run_id