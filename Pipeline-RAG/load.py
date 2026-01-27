

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/data_IT.pdf")

pages = loader.load()
print(pages)
