import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import shutil
from pipelineRAG.vectorstore import get_embedding_model
from pipelineRAG.vectorstore import create_and_store_embeddings

def test_get_embedding_model_success():
    """Test chargement modèle avec token valide"""
    with patch('pipelineRAG.vectorstore.HF_TOKEN', 'fake_token'):
        with patch('pipelineRAG.vectorstore.HuggingFaceEmbeddings') as mock_hf:
            
            
            model = get_embedding_model()
            
            assert mock_hf.called
            call_args = mock_hf.call_args[1]
            assert call_args['model_kwargs']['device'] == 'cpu'
            assert call_args['encode_kwargs']['normalize_embeddings'] is True







def test_create_and_store_embeddings_success():
    """Test création base vectorielle"""
    mock_chunks = [Mock(), Mock()]
    
    with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
        with patch('pipelineRAG.vectorstore.Chroma') as mock_chroma:
            with patch('os.path.exists', return_value=False):
                mock_embed.return_value = Mock()
                mock_db = Mock()
                mock_chroma.from_documents.return_value = mock_db
                
                
                
                result = create_and_store_embeddings(mock_chunks)
                
                assert result == mock_db
                mock_chroma.from_documents.assert_called_once()



def test_create_and_store_embeddings_error():
    """Test gestion erreur création"""
    mock_chunks = [Mock()]
    
    with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
        with patch('pipelineRAG.vectorstore.Chroma') as mock_chroma:
            with patch('os.path.exists', return_value=False):
                mock_embed.return_value = Mock()
                mock_chroma.from_documents.side_effect = Exception("DB Error")
                
                
                result = create_and_store_embeddings(mock_chunks)
                
                assert result is None




def test_load_vector_db_exists():
    """Test chargement base existante"""
    with patch('os.path.exists', return_value=True):
        with patch('pipelineRAG.vectorstore.get_embedding_model') as mock_embed:
            with patch('pipelineRAG.vectorstore.Chroma') as mock_chroma:
                mock_embed.return_value = Mock()
                mock_db = Mock()
                mock_chroma.return_value = mock_db
                
                from pipelineRAG.vectorstore import load_vector_db
                
                result = load_vector_db()
                
                assert result == mock_db
                mock_chroma.assert_called_once()