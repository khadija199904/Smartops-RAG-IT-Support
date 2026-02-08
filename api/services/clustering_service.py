import joblib
from pipelineRAG.vectorstore import get_embedding_model
import numpy as np


def clustering_query (query_text: str):
  
  kmeans = joblib.load("ml/models_saved/kmeans_it_support.joblib")
  embed_model = get_embedding_model()
  q_vector = embed_model.embed_documents(query_text)
  q_X = np.array(q_vector)
  cluster_label = kmeans.predict(q_X)[0].item()


  return cluster_label











if __name__ == "__main__":
    test_questions = [
        "Comment identifier la cause racine d’un problème informatique",
        "Quelle est la différence entre first-line, second-line et third-line support ?",      
        "Quelles sont les trois questions fondamentales de l’IT support ?",     
        "Pourquoi ne faut-il jamais faire d’hypothèses lors d’un diagnostic IT",      
        "Pouvez-vous m'installer le logiciel Photoshop ?",        
        "L'imprimante fait un bruit bizarre et ne sort rien",      
        "Comment configurer mon VPN pour le télétravail ?",       
        "J'ai renversé du café sur mon clavier",                  
    ]

    print("\n--- Analyse des Sujets ---")
    for q in test_questions:
        cluster_id = clustering_query(q)
        print(f"Cluster {cluster_id} | Question: {q}")