#!/usr/bin/env python3
"""
Test script for the OpenAI Agent integration with Supabase MCP Server.

This script tests the agent's ability to interpret queries and determine actions,
both with and without actual database connections.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the supabase_mcp module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase_mcp.openai_agent import OpenAIAgent
from supabase_mcp.integration import IntegratedSupabaseAgent


def test_agent_without_api_key():
    """Test the agent functionality without OpenAI API key (fallback mode)."""
    print("=" * 60)
    print("Testing OpenAI Agent without API key (fallback mode)")
    print("=" * 60)
    
    # Ensure no API key is set
    os.environ.pop('OPENAI_API_KEY', None)
    
    agent = OpenAIAgent()
    
    test_queries = [
        "Get all users from the users table",
        "Create a new user with name John and email john@example.com", 
        "Update user status to active where id is 1",
        "Delete inactive users"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent.process_query(query)
        print(f"Result: {json.dumps(result, indent=2)}")


def test_agent_with_mock_api_key():
    """Test the agent functionality with a mock API key (will fail OpenAI calls but test structure)."""
    print("\n" + "=" * 60)
    print("Testing OpenAI Agent with mock API key")
    print("=" * 60)
    
    # Set a fake API key to test the structure
    os.environ['OPENAI_API_KEY'] = 'mock-key-for-testing'
    
    agent = OpenAIAgent()
    
    test_queries = [
        "Get all users from the users table",
        "Create a new user with name Alice and email alice@example.com"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent.process_query(query)
        print(f"Result: {json.dumps(result, indent=2)}")


def test_integration_without_supabase():
    """Test the integration module without actual Supabase connection."""
    print("\n" + "=" * 60)
    print("Testing Integration without Supabase connection")
    print("=" * 60)
    
    # Test without Supabase context (will use placeholder methods)
    integrated_agent = IntegratedSupabaseAgent()
    
    test_result = integrated_agent.test_functionality()
    print("\nIntegration test results:")
    print(json.dumps(test_result, indent=2))


def main():
    """Run all tests."""
    print("OpenAI Agent Test Suite")
    print("This script tests the agent functionality without requiring actual API keys or database connections.")
    
    try:
        test_agent_without_api_key()
        test_agent_with_mock_api_key()
        test_integration_without_supabase()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        print("\nTo test with actual OpenAI API:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Run the script again")
        print("\nTo test with actual Supabase database:")
        print("1. Set SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables")
        print("2. Use the MCP server with the integrated agent")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()