"""
Integration module for connecting OpenAI Agent with Supabase MCP Server.

This module provides the integration between the OpenAI agent and the MCP server tools,
allowing the agent to use the actual Supabase database operations.
"""

from typing import Dict, Any, Optional
from .server import (
    read_table_rows,
    create_table_records,
    update_table_records,
    delete_table_records
)
from .openai_agent import OpenAIAgent


class IntegratedSupabaseAgent:
    """
    A Supabase MCP agent that integrates OpenAI query interpretation with Supabase database operations.
    """
    
    def __init__(self, supabase_context=None):
        """
        Initialize the integrated agent.
        
        Args:
            supabase_context: The Supabase context from the MCP server
        """
        self.supabase_context = supabase_context
        
        # Create server tools mapping
        self.server_tools = {
            "read_table_rows": read_table_rows,
            "create_table_records": create_table_records,
            "update_table_records": update_table_records,
            "delete_table_records": delete_table_records,
        }
        
        # Initialize the OpenAI agent with access to server tools
        self.agent = OpenAIAgent(server_tools=self.server_tools)
    
    def process_user_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query using OpenAI interpretation and MCP server execution.
        
        Args:
            query: Natural language query from the user
            
        Returns:
            Dictionary containing the result of the database operation
        """
        return self.agent.process_query(query, context=self.supabase_context)
    
    def test_functionality(self) -> Dict[str, Any]:
        """
        Test the agent functionality with sample queries.
        
        Returns:
            Dictionary containing test results
        """
        test_queries = [
            "Get all users from the users table",
            "Create a new user with name John and email john@example.com",
            "Update user status to active where id is 1",
            "Delete users where is_active is false"
        ]
        
        results = {}
        for query in test_queries:
            try:
                result = self.process_user_query(query)
                results[query] = result
            except Exception as e:
                results[query] = {"error": str(e)}
        
        return results


def create_agent_with_mcp_context(supabase_context) -> IntegratedSupabaseAgent:
    """
    Factory function to create an integrated agent with MCP context.
    
    Args:
        supabase_context: The Supabase context from the MCP server
        
    Returns:
        IntegratedSupabaseAgent instance
    """
    return IntegratedSupabaseAgent(supabase_context)