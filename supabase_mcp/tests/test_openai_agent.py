"""
Tests for the OpenAI Agent integration with Supabase MCP Server.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from supabase_mcp.openai_agent import OpenAIAgent
from supabase_mcp.integration import IntegratedSupabaseAgent


class TestOpenAIAgent:
    """Test cases for the OpenAI Agent."""
    
    def test_agent_initialization_without_api_key(self):
        """Test that agent initializes correctly without OpenAI API key."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            assert agent.client is None
            assert agent.server_tools == {}
            assert "read" in agent.tool_categories
    
    def test_agent_initialization_with_api_key(self):
        """Test that agent initializes correctly with OpenAI API key."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = OpenAIAgent()
            assert agent.client is not None
            assert agent.server_tools == {}
    
    def test_query_interpretation_fallback_read(self):
        """Test query interpretation fallback for read operations."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            result = agent.interpret_query("Get all users")
            assert result["action"] == "read"
            assert "table_name" in result["parameters"]
    
    def test_query_interpretation_fallback_create(self):
        """Test query interpretation fallback for create operations."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            result = agent.interpret_query("Create a new user")
            assert result["action"] == "create"
            assert "table_name" in result["parameters"]
    
    def test_query_interpretation_fallback_update(self):
        """Test query interpretation fallback for update operations."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            result = agent.interpret_query("Update user status")
            assert result["action"] == "update"
            assert "table_name" in result["parameters"]
    
    def test_query_interpretation_fallback_delete(self):
        """Test query interpretation fallback for delete operations."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            result = agent.interpret_query("Delete inactive users")
            assert result["action"] == "delete"
            assert "table_name" in result["parameters"]
    
    def test_process_query_without_server_tools(self):
        """Test processing query without server tools (uses placeholder methods)."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            result = agent.process_query("Get all users")
            assert "result" in result
            assert "placeholder" in result["result"]
    
    def test_process_query_with_server_tools(self):
        """Test processing query with mock server tools."""
        with patch.dict(os.environ, {}, clear=True):
            mock_tool = MagicMock(return_value={"data": [{"id": 1, "name": "John"}]})
            server_tools = {"read_table_rows": mock_tool}
            
            agent = OpenAIAgent(server_tools=server_tools)
            result = agent.process_query("Get all users", context="mock_context")
            
            assert "data" in result
            mock_tool.assert_called_once()
    
    def test_process_query_error_handling(self):
        """Test error handling in query processing."""
        with patch.dict(os.environ, {}, clear=True):
            agent = OpenAIAgent()
            
            # Test with invalid query that might cause errors
            with patch.object(agent, 'interpret_query', side_effect=Exception("Test error")):
                result = agent.process_query("invalid query")
                assert "error" in result
                assert "Test error" in result["error"]


class TestIntegratedSupabaseAgent:
    """Test cases for the Integrated Supabase Agent."""
    
    def test_agent_initialization(self):
        """Test that integrated agent initializes correctly."""
        agent = IntegratedSupabaseAgent()
        assert agent.supabase_context is None
        assert len(agent.server_tools) == 4
        assert "read_table_rows" in agent.server_tools
        assert agent.agent is not None
    
    def test_agent_initialization_with_context(self):
        """Test that integrated agent initializes with context."""
        mock_context = MagicMock()
        agent = IntegratedSupabaseAgent(supabase_context=mock_context)
        assert agent.supabase_context == mock_context
    
    def test_process_user_query(self):
        """Test processing user query through integrated agent."""
        with patch.dict(os.environ, {}, clear=True):
            agent = IntegratedSupabaseAgent()
            result = agent.process_user_query("Get all users")
            # Should use placeholder since no real context provided
            assert "result" in result or "error" in result
    
    def test_test_functionality(self):
        """Test the test functionality method."""
        with patch.dict(os.environ, {}, clear=True):
            agent = IntegratedSupabaseAgent()
            results = agent.test_functionality()
            
            # Should have results for all test queries
            assert len(results) == 4
            for query, result in results.items():
                assert isinstance(result, dict)
                # Each result should have either a result or error key
                assert "result" in result or "error" in result


class TestAgentIntegration:
    """Integration tests for the complete agent system."""
    
    def test_end_to_end_without_external_dependencies(self):
        """Test complete workflow without external API dependencies."""
        with patch.dict(os.environ, {}, clear=True):
            # Test the complete workflow
            agent = IntegratedSupabaseAgent()
            
            test_queries = [
                "Get all users",
                "Create user John",
                "Update user status",
                "Delete old records"
            ]
            
            for query in test_queries:
                result = agent.process_user_query(query)
                assert isinstance(result, dict)
                # Should either succeed with placeholder or fail gracefully
                assert "result" in result or "error" in result
    
    @patch('supabase_mcp.openai_agent.OpenAI')
    def test_with_mock_openai(self, mock_openai_class):
        """Test with mocked OpenAI client."""
        # Setup mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"action": "read", "parameters": {"table_name": "users"}}'
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            agent = OpenAIAgent()
            result = agent.interpret_query("Get all users")
            
            assert result["action"] == "read"
            assert result["parameters"]["table_name"] == "users"
            mock_client.chat.completions.create.assert_called_once()