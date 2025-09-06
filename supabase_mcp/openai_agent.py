"""
OpenAI Agent for Supabase MCP Server - A Coordinator agent that interacts with the Supabase MCP server.

This module defines the Coordinator agent that processes queries and determines which tools to invoke
based on the user's requests. It integrates with the OpenAI model to facilitate communication and decision-making.

Dependencies:
- openai
- requests
"""

import os
from openai import OpenAI
from typing import Any, Dict, List

class OpenAIAgent:
    def __init__(self, server_tools=None):
        """
        Initialize the OpenAI agent with access to MCP server tools.
        
        Args:
            server_tools: Dictionary of MCP server tool functions (optional)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            
        self.server_tools = server_tools or {}
        
        # Define available tool categories
        self.tool_categories = {
            "read": "read_table_rows",
            "create": "create_table_records", 
            "update": "update_table_records",
            "delete": "delete_table_records",
        }

    def process_query(self, query: str, context=None) -> Dict[str, Any]:
        """
        Process the user's query and determine the appropriate tool to invoke.

        Args:
            query: The user's query as a string.
            context: Optional MCP context for tool execution

        Returns:
            A dictionary containing the result of the invoked tool.
        """
        try:
            # Use OpenAI model to interpret the query and determine the action
            action_info = self.interpret_query(query)
            action = action_info.get("action")
            parameters = action_info.get("parameters", {})
            
            if action in self.tool_categories:
                tool_name = self.tool_categories[action]
                if tool_name in self.server_tools:
                    # Call the actual MCP server tool
                    return self.server_tools[tool_name](context, **parameters)
                else:
                    # Fallback to placeholder methods if MCP tools not available
                    fallback_method = getattr(self, action + "_table_rows" if action == "read" else action + "_table_records")
                    return fallback_method(query)
            else:
                return {"error": f"No valid action found for the query: {query}"}
        except Exception as e:
            return {"error": f"Error processing query: {str(e)}"}

    def interpret_query(self, query: str) -> Dict[str, Any]:
        """
        Use the OpenAI model to interpret the user's query and return the action and parameters.

        Args:
            query: The user's query as a string.

        Returns:
            Dictionary containing the action and parameters to be performed.
        """
        try:
            # Check if OpenAI client is available
            if not self.client:
                # Fallback: use simple keyword matching
                query_lower = query.lower()
                if any(word in query_lower for word in ["get", "read", "select", "find", "show", "list"]):
                    return {"action": "read", "parameters": {"table_name": "users"}}
                elif any(word in query_lower for word in ["create", "add", "insert", "new"]):
                    return {"action": "create", "parameters": {"table_name": "users", "records": {}}}
                elif any(word in query_lower for word in ["update", "modify", "change", "edit"]):
                    return {"action": "update", "parameters": {"table_name": "users", "updates": {}, "filters": {}}}
                elif any(word in query_lower for word in ["delete", "remove", "drop"]):
                    return {"action": "delete", "parameters": {"table_name": "users", "filters": {}}}
                else:
                    return {"action": "read", "parameters": {"table_name": "users"}}
            
            system_prompt = """
            You are a database query interpreter. Analyze the user's query and determine:
            1. The action to perform: "read", "create", "update", or "delete"
            2. The parameters needed for that action
            
            For read operations, extract: table_name, columns (optional), filters (optional), limit (optional), order_by (optional)
            For create operations, extract: table_name, records (the data to insert)  
            For update operations, extract: table_name, updates (new values), filters (which records to update)
            For delete operations, extract: table_name, filters (which records to delete)
            
            Respond with a JSON object containing "action" and "parameters" keys.
            
            Example:
            Query: "Get all users from the users table"
            Response: {"action": "read", "parameters": {"table_name": "users"}}
            
            Query: "Create a new user with name John and email john@example.com"
            Response: {"action": "create", "parameters": {"table_name": "users", "records": {"name": "John", "email": "john@example.com"}}}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.1
            )
            
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            import json
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # Fallback: try to determine action from simple keywords
                query_lower = query.lower()
                if any(word in query_lower for word in ["get", "read", "select", "find", "show", "list"]):
                    return {"action": "read", "parameters": {"table_name": "users"}}  # Default table
                elif any(word in query_lower for word in ["create", "add", "insert", "new"]):
                    return {"action": "create", "parameters": {"table_name": "users", "records": {}}}
                elif any(word in query_lower for word in ["update", "modify", "change", "edit"]):
                    return {"action": "update", "parameters": {"table_name": "users", "updates": {}, "filters": {}}}
                elif any(word in query_lower for word in ["delete", "remove", "drop"]):
                    return {"action": "delete", "parameters": {"table_name": "users", "filters": {}}}
                else:
                    return {"action": "read", "parameters": {"table_name": "users"}}
                    
        except Exception as e:
            # Fallback to simple read action if OpenAI call fails
            return {"action": "read", "parameters": {"table_name": "users"}}

    def read_table_rows(self, query: str) -> Dict[str, Any]:
        """Placeholder method for read operations when MCP tools are not available."""
        return {"result": "Read operation executed (placeholder)", "query": query}

    def create_table_records(self, query: str) -> Dict[str, Any]:
        """Placeholder method for create operations when MCP tools are not available."""
        return {"result": "Create operation executed (placeholder)", "query": query}

    def update_table_records(self, query: str) -> Dict[str, Any]:
        """Placeholder method for update operations when MCP tools are not available."""
        return {"result": "Update operation executed (placeholder)", "query": query}

    def delete_table_records(self, query: str) -> Dict[str, Any]:
        """Placeholder method for delete operations when MCP tools are not available."""
        return {"result": "Delete operation executed (placeholder)", "query": query}

# Example usage
if __name__ == "__main__":
    # Test the agent without MCP tools (using placeholders)
    agent = OpenAIAgent()
    
    # Test queries
    test_queries = [
        "Create a new user with name John Doe and email john@example.com",
        "Get all users from the users table",
        "Update user status to active where id is 1",
        "Delete inactive users"
    ]
    
    print("Testing OpenAI Agent (without MCP integration):")
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent.process_query(query)
        print(f"Result: {result}")
