
from pipelineRAG.vectorstore import load_vector_db
from langchain_core.prompts import ChatPromptTemplate ,PromptTemplate

from langchain_groq import ChatGroq
from api.core.config import GROQ_API_KEY
from langchain_classic.chains.retrieval_qa.base import RetrievalQA



MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0
TOP_K = 8

system_prompt = (
    "Tu es un assistant technique expert en IT. "
    "Utilise exclusivement le contexte fourni pour répondre à la question. "
    "Si la réponse n'est pas présente dans le contexte, dis exactement ceci : "
    "'Je ne trouve pas l'information dans les documents fournis.' "
    "Ne donne pas d'explications basées sur tes propres connaissances.\n\n"
    "Contexte:\n{context}"
)
  



def get_retriever():
    vecteur_db = load_vector_db()
    if  vecteur_db:
        retriever = vecteur_db.as_retriever(search_kwargs={"k": TOP_K})

        return retriever
    else:  
        raise ValueError("Erreur : La base vectorielle est vide ou inexistante.")
    
    


prompt_template = """Tu es un assistant technique expert en IT.
Utilise exclusivement le contexte fourni pour répondre à la question.
Si la réponse n'est pas présente dans le contexte, dis exactement ceci :
'Je ne trouve pas l'information dans les documents fournis.'
Ne donne pas d'explications basées sur tes propres connaissances.

Contexte:
{context}

Question: {question}

Réponse:"""

    


def get_llm():
    
    llm = ChatGroq(model=MODEL_NAME, temperature=TEMPERATURE,api_key=GROQ_API_KEY)
    return llm

def build_rag_chain():
    retriever = get_retriever()

    llm = get_llm()
    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", system_prompt),  # Contient {context}
    #     ("human", "{query}"),        # Contient {query}
    # ])
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    
    qa_chain = RetrievalQA.from_chain_type(
     llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}   
         )
    
    
    return qa_chain

if __name__ == "__main__":
   

   
#    r = get_retriever()
#    print(r)
    chain = build_rag_chain()
    query = "Quelle est la procédure pour un problème de connexion réseau ?"
    result = chain.invoke({"query": query})
    print (result)
