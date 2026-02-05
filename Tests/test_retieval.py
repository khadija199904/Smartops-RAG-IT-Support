import pytest
from unittest.mock import Mock, patch, MagicMock
def test_rag_chain_invoke():
    """Test invocation chaîne RAG"""

    mock_chain = Mock()
    mock_result = {
        "result":"Reponse test" ,
        "source_documents":[Mock(),Mock()]
    }
    mock_chain.invoke.return_value = mock_result

    query = "Test question?"
    result = mock_chain.invoke({"query":query})

    assert result == mock_result
    assert "result" in result
    assert "source_documents" in result
    mock_chain.assert_called_once_with({"query":query})