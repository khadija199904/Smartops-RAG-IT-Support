from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma
import chromadb
# from langchain_community.vectorstores import Chroma
from api.core.config import  EMBEDDING_MODEL_NAME ,HF_TOKEN,CHROMA_HOST ,CHROMA_PORT ,COLLECTION_NAME



def get_embedding_model():
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN est manquant dans les variables d'environnement.")
    print(f"Chargement du modèle d'embeddings : {EMBEDDING_MODEL_NAME}...")
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


def create_and_store_embeddings(chunks):
    """Génère les vecteurs et les stocke dans ChromaDB avec persistance."""
      
    
    try:
       # vectorization
       embeddings = get_embedding_model()
       print(f"Connexion au serveur ChromaDB sur {CHROMA_HOST}:{CHROMA_PORT}...")
        
       
       persistent_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

       # delete a collection if exist

    #    try:
    #         persistent_client.delete_collection(name=COLLECTION_NAME)
    #         print(f"Ancienne collection '{COLLECTION_NAME}' supprimée.")
    #    except Exception:
    #         pass
       
       vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            client=persistent_client, 
            collection_name=COLLECTION_NAME
        )
       
       print(" Base de données vectorielle créée et persistée avec succès.")
       
       return vector_db
    except Exception as e:
        print(f"Erreur lors de la création de la Vector DB : {e}")
        return None 
    
    




def load_vector_db():
    """Charge la base de données vectorielle existante."""

    embeddings = get_embedding_model()
    print("retrieving depuis chormadb")
    persistent_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    
    return Chroma(
        client=persistent_client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )














if __name__ == "__main__":

#     if results["documents"]:
#        print("--- Contenu du document VPN ---")
#        print(results["documents"][0])
#     else:
#        print("Aucun document trouvé.")
   
    from pipelineRAG.ingestion import ingestion_preparation
    # #test fonctionnement complet
    chunks = ingestion_preparation()
    vecteur = create_and_store_embeddings(chunks)
