import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pipelineRAG.vectorstore import get_embedding_model

MODEL_PATH = "ml/models_saved/kmeans_it_support.joblib"

def train_kmeans():
    print("--- Phase 1 : Entraînement sur données IT ---")
    
    # 1. Chargement des données
    file_path = "./data/it_support_questions.txt"
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return None

    with open(file_path, "r", encoding="utf-8") as file_it:
        questions = [line.strip() for line in file_it if line.strip()]

    # 2. Génération des embeddings
     # print(f"Génération des embeddings pour {len(questions)} questions...")
    model_embedding = get_embedding_model()
    questions_embeddings = model_embedding.embed_documents(questions)
    X = np.array(questions_embeddings)

    # 3. Entraînement KMeans
   
    # print("Calcul des clusters...")
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X)

    # cluster_ids = kmeans.labels_ 
    # print(f"Succès : {len(set(cluster_ids))} groupes identifiés.")
    
    # 4. Sauvegarde du modèle
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(kmeans, MODEL_PATH)
    print(f"Modèle entraîné et sauvegardé .")
    return kmeans

    
    



if __name__ == "__main__":
    train_kmeans()