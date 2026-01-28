from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from api.core.config import MODEL_NAME ,VECTOR_DB_DIR ,PDF_PATH
from pipelineRAG.load_split import ingestion_preparation


def get_embedding_model():
    print(f"Chargement du modèle d'embeddings : {MODEL_NAME}...")
    return HuggingFaceEmbeddings(model_name=MODEL_NAME)



def create_and_store_embeddings(chunks):
    """Génère les vecteurs et les stocke dans ChromaDB avec persistance."""
      
    embeddings = get_embedding_model()
    # Création et persistance automatique dans le dossier spécifié
    vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=VECTOR_DB_DIR
        )
        
    

   

    return vector_db
if __name__ == "__main__":
    # print(MODEL_NAME)
    # model = get_embedding_model ()
    # texte = "Keep pushing forward, Khadija. Your workflow is spot on!"
    # vecteur = model.embed_query(texte)
    # print(vecteur)
    chunks = ingestion_preparation(file_path=PDF_PATH)
    vecteur = create_and_store_embeddings(chunks)
