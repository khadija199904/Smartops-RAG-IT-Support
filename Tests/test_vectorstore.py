
from unittest.mock import Mock, patch
from pipelineRAG.vectorstore import create_and_store_embeddings






def test_create_and_store_embeddings_success():
    """Test création base vectorielle avec HttpClient"""
    mock_chunks = [Mock(), Mock(), Mock()]
    
    with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
        with patch('pipelineRAG.vectorstore.chromadb.HttpClient') as mock_http:
            with patch('pipelineRAG.vectorstore.Chroma') as mock_chroma:
                # Setup mocks
                mock_embed.return_value = Mock()
                mock_client = Mock()
                mock_http.return_value = mock_client
                mock_db = Mock()
                mock_chroma.from_documents.return_value = mock_db
                
                from pipelineRAG.vectorstore import create_and_store_embeddings
                
                result = create_and_store_embeddings(mock_chunks)
                
                # Vérifications
                assert result == mock_db
                mock_http.assert_called_once()
                mock_chroma.from_documents.assert_called_once()

def test_create_and_store_embeddings_error():
    """Test gestion erreur création"""
    mock_chunks = [Mock()]
    
    with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
        with patch('pipelineRAG.vectorstore.chromadb.HttpClient') as mock_http:
            mock_embed.return_value = Mock()
            mock_http.side_effect = Exception("Connection failed")
            
                
            result = create_and_store_embeddings(mock_chunks)
                
            assert result is None




def test_load_vector_db_success():
    """Test chargement base vectorielle"""
    with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
        with patch('pipelineRAG.vectorstore.chromadb.HttpClient') as mock_http:
            with patch('pipelineRAG.vectorstore.Chroma') as mock_chroma:
                mock_embed.return_value = Mock()
                mock_client = Mock()
                mock_http.return_value = mock_client
                mock_db = Mock()
                mock_chroma.return_value = mock_db
                
                from pipelineRAG.vectorstore import load_vector_db
                
                result = load_vector_db()
                
                assert result == mock_db
                mock_http.assert_called_once()
                mock_chroma.assert_called_once()