# tests/test_fixtures_query_service.py
import pytest
from unittest.mock import Mock, patch
from api.services.rag_service import query_rag_service

@pytest.fixture
def mock_rag_chain():
    """Fixture chaîne RAG"""
    chain = Mock()
    chain.invoke.return_value = {
        "result": "Réponse standard",
        "source_documents": [Mock()]
    }
    return chain

@pytest.fixture
def mock_question():
    """Fixture question standard"""
    return "Comment diagnostiquer un problème IT?"

def test_with_chain(mock_rag_chain):
    """Test avec fixture chaîne"""
    with patch('api.services.rag_service.build_rag_chain', return_value=mock_rag_chain):
        
        result = query_rag_service("Test?")
        
        assert result["result"] == "Réponse standard"

def test_with_question(mock_rag_chain, mock_question):
    """Test avec fixture question"""
    with patch('pipelineRAG.query_service.build_rag_chain', return_value=mock_rag_chain):
        
        result = query_rag_service(mock_question)
        
        mock_rag_chain.invoke.assert_called_once_with({"query": mock_question})
        assert "result" in result
        assert "source_documents" in result