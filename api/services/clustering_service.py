import joblib
from pipelineRAG.vectorstore import get_embedding_model
import numpy as np


def clustering_query (query_text: str):
  
  kmeans = joblib.load("ml/models_saved/kmeans_it_support.joblib")
  embed_model = get_embedding_model()
  q_vector = embed_model.embed_documents(query_text)
  q_X = np.array(q_vector)
  cluster_label = kmeans.predict(q_X)[0].item()

#   cluster_label = kmeans.predict(q_vector)[0]

  return cluster_label



if __name__ == "__main__":
    test_questions = [
        "Le wifi ne fonctionne pas dans la salle de réunion",      # Sujet : Réseau
        "Je n'arrive pas à réinitialiser mon mot de passe",       # Sujet : Sécurité/Accès
        "Mon écran reste noir quand j'allume l'ordinateur",       # Sujet : Matériel
        "Pouvez-vous m'installer le logiciel Photoshop ?",        # Sujet : Logiciel
        "L'imprimante fait un bruit bizarre et ne sort rien",      # Sujet : Périphérique
        "Comment configurer mon VPN pour le télétravail ?",       # Sujet : Réseau (devrait être Cluster 0)
        "J'ai renversé du café sur mon clavier",                  # Sujet : Matériel
    ]

    print("\n--- Analyse des Sujets ---")
    for q in test_questions:
        cluster_id = clustering_query(q)
        print(f"Cluster {cluster_id} | Question: {q}")