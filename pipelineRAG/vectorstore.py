from langchain_huggingface import HuggingFaceEmbeddings , HuggingFaceEndpointEmbeddings
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

from langchain_community.vectorstores import Chroma
from api.core.config import  EMBEDDING_MODEL_NAME ,VECTOR_DB_DIR ,PDF_PATH ,HF_TOKEN

import os
import shutil


def get_embedding_model():
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN est manquant dans les variables d'environnement.")
    print(f"Chargement du modèle d'embeddings : {EMBEDDING_MODEL_NAME,}...")
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


def create_and_store_embeddings(chunks):
    """Génère les vecteurs et les stocke dans ChromaDB avec persistance."""
      
    # suprimr ancienne chroma db
    if os.path.exists(VECTOR_DB_DIR):
       shutil.rmtree(VECTOR_DB_DIR)
       print("Ancienne base vectorielle supprimée.")
    try:
       # vectorization
       embeddings = get_embedding_model()
       print(f"Stockage dans ChromaDB à l'emplacement : {VECTOR_DB_DIR}...")
       # Création et persistance automatique dans le dossier spécifié
       vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=VECTOR_DB_DIR
        )
       
       print(" Base de données vectorielle créée et persistée avec succès.")
       
       return vector_db
    except Exception as e:
        print(f"Erreur lors de la création de la Vector DB : {e}")
        return None 
    
    




def load_vector_db():
    """Charge la base de données vectorielle existante."""
    if os.path.exists(VECTOR_DB_DIR):
        embeddings = get_embedding_model()
        return Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
    else:
        print("La base de données n'existe pas encore.")
        return None
    














if __name__ == "__main__":
    # # Test Simple
    # model = get_embedding_model()
    # texte = "Keep pushing forward, Khadija. Your workflow is spot on!"
    # vecteur = model.embed_query(texte)
    # print(len(vecteur))
    # print(f"Premier élément : {vecteur[0]}")
    from pipelineRAG.ingestion import ingestion_preparation
    #test fonctionnement complet
    chunks = ingestion_preparation(file_path=PDF_PATH)
    vecteur = create_and_store_embeddings(chunks)
