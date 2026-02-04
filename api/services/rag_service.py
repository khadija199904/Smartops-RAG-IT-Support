# import mlflow
from pipelineRAG.retrieval import build_rag_chain





def query_rag_service(question):

    chain = build_rag_chain()
    result = chain.invoke({"query": question})

    return result