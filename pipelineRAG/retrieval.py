
from pipelineRAG.vectorstore import load_vector_db
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# from api.core.config import HF_TOKEN
# from langchain.chains import RetrievalQA


def get_retriever():
    vecteur_db = load_vector_db()
    if  vecteur_db:
        retriever = vecteur_db.as_retriever(search_kwargs={"k": 3})

        return retriever
    else:  
        raise ValueError("Erreur : La base vectorielle est vide ou inexistante.")
    
    
template = (
    "Tu es un assistant technique expert en IT. "
    "Utilise exclusivement le contexte fourni pour répondre à la question. "
    "Si la réponse n'est pas présente dans le contexte, dis exactement ceci : "
    "'Je ne trouve pas l'information dans les documents fournis.' "
    "Ne donne pas d'explications basées sur tes propres connaissances.\n\n"
    "Contexte:\n{context}"
)
  

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}"),
])


def get_llm():

    llm = ChatGroq(
          model="qwen/qwen3-32b",
          temperature=0,
          max_tokens=None,
          reasoning_format="parsed",
          timeout=None,
            max_retries=2)
    
    
    return llm

def build_rag_chain():
    retriever = get_retriever()
    llm = get_llm()
    
    llm_responce = 

if __name__ == "__main__":
   

   
   r = get_retrieve()
   print(r)
#    query = "Quelle est la procédure pour un problème de connexion réseau ?"
#    result = chain.invoke({"query": query})
#    print(f"Nombre de documents dans la base : {db._collection.count()}")
# #    docs = db.similarity_search(query, k=1) # On demande le résultat le plus proche
   

     
#    print(f"   Aperçu du résultat trouvé : {docs[0].page_content[:100]}...")
#    print(f"   Source (Page) : {docs[0].metadata.get('page')}")