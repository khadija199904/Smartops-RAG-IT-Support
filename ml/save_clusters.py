
import joblib
import numpy as np
from sqlalchemy.orm import Session
from api.models.queries import Query  # Ton modèle SQLAlchemy
from pipelineRAG.vectorstore import get_embedding_model

def process_query_clustering(db: Session):
    """
    Fonction pour classer les questions en attente et enregistrer leur cluster en DB.
    """
    # 1. Extraction : Récupérer les questions qui n'ont pas encore de cluster
    queries_to_process = db.query(Query).filter(Query.cluster.is_(None)).all()
    
    if not queries_to_process:
        return 0

    # 2. Préparation des données
    ids = [q.id for q in queries_to_process]
    texts = [q.question for q in queries_to_process]

    # 3. Chargement du modèle KMeans et de l'embedder
    # Assure-toi que le chemin vers le .joblib est correct
    kmeans = joblib.load("ml/models_saved/kmeans_it_support.joblib")
    embed_model = get_embedding_model()

    # 4. Génération des embeddings et Prédiction
    embeddings = embed_model.embed_documents(texts)
    labels = kmeans.predict(np.array(embeddings))

    # 5. Stockage : Mise à jour de la table queries
    for q_id, label in zip(ids, labels):
        db.query(Query).filter(Query.id == q_id).update({"cluster": int(label)})
    
    # 6. Validation
    db.commit()
    
    return len(ids)

