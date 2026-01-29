
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from api.core.config import PDF_PATH
import os 


def ingestion_preparation(file_path=PDF_PATH):
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"Erreur : Le fichier n'existe pas à l'emplacement : {file_path}")
  
  try : 
       # charger le PDF
      loader = PyPDFLoader(file_path)
      docs = loader.load()

       # split documments into cunks
      text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000,  
      chunk_overlap=100,  
      separators=["\n\n", "\n", " ", ""]  
         )
      chunks = text_splitter.split_documents(docs)
      

      return chunks
  except Exception as e:
      raise Exception(f"Une erreur est survenue lors de l'ingestion : {e}")
  
if __name__ == "__main__":      
   chunks = ingestion_preparation(file_path=PDF_PATH)
   print(f"Nombre de chunks créés : {len(chunks)}")
   sample_chunk = chunks[0]
   print("\n--- Exemple de métadonnées du premier chunk ---")
   print(sample_chunk.metadata)
      
          
