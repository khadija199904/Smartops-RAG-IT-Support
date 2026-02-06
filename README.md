
#  RAG IT Support System

un assistant intelligent interne capable de répondre de manière fiable aux questions des techniciens IT à partir d’un PDF de support IT (procédures, incidents, FAQ).

##  Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Tests](#tests)
- [API](#api)
- [Déploiement](#déploiement)
- [Dépannage](#dépannage)
- [Contribution](#contribution)
- [Licence](#licence)

##  Aperçu

Ce projet implémente un système RAG (Retrieval-Augmented Generation) spécialisé dans le support IT. Il permet de:
- Indexer des documents IT support (PDF, etc.)
- Répondre aux questions techniques basées sur ces documents
- Fournir des sources pour chaque réponse
- Offrir une API REST pour l'intégration

##  Fonctionnalités

- **🔍 Ingestion de documents**: Support PDF avec découpage intelligent
- **🧠 Embeddings**: Utilisation de modèles HuggingFace performants
- **💾 Base vectorielle**: ChromaDB avec support HTTP pour scalabilité
- **🤖 LLM**: Intégration Groq pour génération rapide
- **📊 Clustering**: KMeans pour organisation des questions
- **🔒 Sécurité**: Gestion des tokens et variables d'environnement
- **✅ Tests**: Suite complète de tests unitaires
- **🚀 API FastAPI**: Interface REST documentée

## 🏗️ Architecture
```
┌─────────────────┐
│  Documents PDF  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Ingestion & Chunking   │
│  (LangChain)            │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Embeddings Generation  │
│  (HuggingFace)          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  ChromaDB Vector Store  │
│  (HTTP Client)          │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  RAG Chain              │
│  (LangChain + Groq)     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  FastAPI REST API       │
└─────────────────────────┘
```

## Prérequis

- Python 3.+
- Docker (pour ChromaDB)
- Compte HuggingFace (pour les embeddings)
- Compte Groq (pour le LLM)

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/rag-it-support.git
cd rag-it-support
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer ChromaDB
```bash
# Avec Docker
docker run -d -p 8000:8000 chromadb/chroma

# Ou avec Docker Compose
docker-compose up -d chromadb
```

## ⚙️ Configuration

### 1. Variables d'environnement

Créer un fichier `.env` à la racine:
```env
# HuggingFace
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxx

# Groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000
COLLECTION_NAME=it_support_docs

# Modèle embeddings
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# Documents
PDF_PATH=data/data_IT.pdf
```

### 2. Configuration avancée

Éditer `api/core/config.py`:
```python
# Paramètres RAG
TOP_K = 2  # Nombre de documents à récupérer
MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0

# Paramètres chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

## 📚 Utilisation

### Pipeline complet
```bash
# 1. Ingérer les documents
python -m pipelineRAG.ingestion

# 2. Créer les embeddings
python -m pipelineRAG.vectorstore

# 3. Tester une requête
python -m pipelineRAG.query_service
```

### Utilisation programmatique
```python
from pipelineRAG.query_service import query_rag_service

# Poser une question
result = query_rag_service("Comment diagnostiquer un problème réseau?")

print(f"Réponse: {result['result']}")
print(f"Sources: {len(result['source_documents'])} documents")
```

### Lancer l'API
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

Accéder à la documentation: http://localhost:8080/docs

## 📁 Structure du projet
```
rag-it-support/
├── api/
│   ├── core/
│   │   └── config.py           # Configuration
│   ├── routes/
│   │   └── chat.py             # Routes API
│   └── main.py                 # Point d'entrée FastAPI
├── pipelineRAG/
│   ├── ingestion.py            # Chargement documents
│   ├── vectorstore.py          # Gestion ChromaDB
│   ├── retrieval.py            # Chaîne RAG
│   └── query_service.py        # Service de requêtes
├── scripts/
│   ├── train_kmeans_rag.py     # Clustering
│   └── index_questions.py      # Indexation questions
├── tests/
│   ├── test_vectorstore.py
│   ├── test_query_service.py
│   └── conftest.py             # Fixtures pytest
├── data/
│   ├── data_IT.pdf             # Documents source
│   └── it_support_questions.txt
├── .env                        # Variables d'environnement
├── requirements.txt            # Dépendances
├── docker-compose.yml          # Configuration Docker
└── README.md
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest tests/ -v
```

### Tests avec couverture
```bash
pytest tests/ --cov=pipelineRAG --cov-report=html --cov-report=term
```

### Tests spécifiques
```bash
# Vectorstore
pytest tests/test_vectorstore.py -v

# Query service
pytest tests/test_query_service.py -v

# Test spécifique
pytest tests/test_vectorstore.py::test_create_and_store_embeddings_success -v
```

### Couverture de code

Après les tests, ouvrir `htmlcov/index.html` dans un navigateur.

## 🔌 API

### Endpoints principaux

#### POST /chat/query
Poser une question au système RAG

**Request:**
```json
{
  "question": "Comment résoudre un problème réseau?",
  "top_k": 2
}
```

**Response:**
```json
{
  "question": "Comment résoudre un problème réseau?",
  "answer": "Pour résoudre un problème réseau...",
  "sources": [
    {
      "content": "Extrait du document...",
      "metadata": {"page": 45}
    }
  ]
}
```

#### POST /documents/upload
Uploader un nouveau document

**Request:**
```bash
curl -X POST "http://localhost:8080/documents/upload" \
  -F "file=@document.pdf"
```

#### GET /health
Vérifier l'état du système

**Response:**
```json
{
  "status": "healthy",
  "chromadb": "connected",
  "model": "loaded"
}
```

### Documentation interactive

- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## 🐳 Déploiement

### Avec Docker Compose
```bash
docker-compose up -d
```

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE

  api:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - chromadb
    env_file:
      - .env
    environment:
      - CHROMA_HOST=chromadb
      - CHROMA_PORT=8000

volumes:
  chroma_data:
```

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 🔧 Dépannage

### ChromaDB ne se connecte pas
```bash
# Vérifier que ChromaDB tourne
docker ps | grep chroma

# Vérifier les logs
docker logs <container_id>

# Tester la connexion
curl http://localhost:8000/api/v1/heartbeat
```

### Erreur de token HuggingFace
```bash
# Vérifier le token
echo $HF_TOKEN

# Se connecter à HuggingFace
huggingface-cli login
```

### Problèmes de mémoire
```python
# Réduire la taille des chunks
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Réduire le nombre de documents récupérés
TOP_K = 1
```

### Erreur CUDA
```python
# Forcer l'utilisation du CPU
model_kwargs = {'device': 'cpu'}
```

## 📊 Performances

### Métriques typiques

- **Ingestion**: ~10 pages/seconde
- **Embedding**: ~50 chunks/seconde
- **Query**: ~2-5 secondes (selon la complexité)
- **Taille index**: ~10MB pour 100 documents

### Optimisations
```python
# Batch processing pour embeddings
embeddings.embed_documents(chunks, batch_size=32)

# Cache des embeddings
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_embed_query(text):
    return embeddings.embed_query(text)
```

## 🛠️ Scripts utiles

### Indexer les 100 questions
```bash
python scripts/index_questions.py
```

### Clustering KMeans
```bash
python scripts/train_kmeans_rag.py
```

### Nettoyer ChromaDB
```bash
python -c "import chromadb; client = chromadb.HttpClient(host='localhost', port=8000); client.delete_collection('it_support_docs')"
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Guidelines

- Écrire des tests pour les nouvelles fonctionnalités
- Suivre PEP 8 pour le style Python
- Documenter les fonctions avec docstrings
- Mettre à jour le README si nécessaire

## 📝 Changelog

### Version 1.0.0 (2024-01-XX)
- ✨ Version initiale
- 🔍 Support PDF
- 🧠 Embeddings HuggingFace
- 💾 ChromaDB HTTP
- 🤖 Groq LLM
- ✅ Tests unitaires

## 📄 Licence

MIT License - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Développement initial* - [VotreGitHub](https://github.com/votre-username)

## 🙏 Remerciements

- [LangChain](https://python.langchain.com/) - Framework RAG
- [ChromaDB](https://www.trychroma.com/) - Base vectorielle
- [HuggingFace](https://huggingface.co/) - Modèles embeddings
- [Groq](https://groq.com/) - LLM ultra-rapide
- [FastAPI](https://fastapi.tiangolo.com/) - Framework API

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discord: [Lien Discord](https://discord.gg/xxxxx)
- 🐛 Issues: [GitHub Issues](https://github.com/votre-username/rag-it-support/issues)

## 🔗 Liens utiles

- [Documentation LangChain](https://python.langchain.com/docs/get_started/introduction)
- [Guide ChromaDB](https://docs.trychroma.com/)
- [API Groq](https://console.groq.com/docs)
- [HuggingFace Models](https://huggingface.co/models)

---

⭐ Si ce projet vous aide, n'hésitez pas à mettre une étoile!