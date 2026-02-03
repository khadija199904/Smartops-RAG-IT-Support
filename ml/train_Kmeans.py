from sklearn.cluster import KMeans
from pipelineRAG.vectorstore import get_embedding_model
import numpy as np
import joblib

MODEL_SAVE_PATH = "ml/models_saved"

def train_kmeans ():
    print("--- Phase 1 : Entraînement sur données IT ---")
    
    with open("./data/it_support_questions.txt", "r", encoding="utf-8") as file_it:
        questions = [line.strip() for line in file_it if line.strip()]

   
    model_embedding = get_embedding_model()

    questions_embeddings = model_embedding.embed_documents(questions)

    X = np.array(questions_embeddings)

    # Entraîner KMeans
    kmeans = KMeans(n_clusters=10, random_state=42)
    
    clusters = kmeans.fit(X)

    cluster_ids = kmeans.labels_ 
    print(f"Questions clustérisées en {len(set(cluster_ids))} groupes")
    

    joblib.dump(kmeans, MODEL_SAVE_PATH)
    print(f"Modèle sauvegardé dans {MODEL_SAVE_PATH}")
    return kmeans
    
if __name__ == "__main__":
    
    train_kmeans()