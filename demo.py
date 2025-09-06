#!/usr/bin/env python3
"""
Demonstration script for the OpenAI Agent integration with Supabase MCP Server.

This script shows how the integrated system works and provides examples of usage.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the supabase_mcp module to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase_mcp.openai_agent import OpenAIAgent
from supabase_mcp.integration import IntegratedSupabaseAgent


def demonstrate_agent_capabilities():
    """Demonstrate the agent capabilities."""
    print("🤖 OpenAI Agent Integration with Supabase MCP Server")
    print("=" * 60)
    
    print("\n📋 What this integration provides:")
    print("✅ Natural language query interpretation")
    print("✅ Automatic tool selection based on user intent")
    print("✅ Integration with Supabase database operations")
    print("✅ Fallback functionality when OpenAI API is not available")
    print("✅ Comprehensive error handling and validation")
    
    print("\n🛠️  Available Database Operations:")
    operations = [
        ("read_table_rows", "Read/query data from tables"),
        ("create_table_records", "Insert new records into tables"),
        ("update_table_records", "Modify existing records"),
        ("delete_table_records", "Remove records from tables"),
        ("process_natural_language_query", "Process queries in natural language")
    ]
    
    for op, desc in operations:
        print(f"   • {op:<30} - {desc}")


def demonstrate_query_interpretation():
    """Demonstrate query interpretation without external dependencies."""
    print("\n🎯 Query Interpretation Demo (Fallback Mode)")
    print("-" * 50)
    
    # Test without API key to show fallback functionality
    os.environ.pop('OPENAI_API_KEY', None)
    
    agent = OpenAIAgent()
    
    sample_queries = [
        ("Get all users", "Database read operation"),
        ("Create a new user named Alice", "Database create operation"),
        ("Update user status to premium", "Database update operation"),
        ("Delete inactive accounts", "Database delete operation")
    ]
    
    for query, expected in sample_queries:
        result = agent.interpret_query(query)
        action = result.get("action", "unknown")
        print(f"Query: '{query}'")
        print(f"   → Action: {action} ({expected})")
        print(f"   → Parameters: {result.get('parameters', {})}")
        print()


def demonstrate_integration():
    """Demonstrate the full integration."""
    print("\n🔗 Integration Demo")
    print("-" * 30)
    
    agent = IntegratedSupabaseAgent()
    
    print("Agent initialized with:")
    print(f"   • Server tools available: {len(agent.server_tools)}")
    print(f"   • Tool names: {list(agent.server_tools.keys())}")
    print(f"   • OpenAI agent: {'Available' if agent.agent else 'Not available'}")
    
    print("\nSample query processing:")
    query = "Show me all users in the database"
    result = agent.process_user_query(query)
    print(f"Query: '{query}'")
    print(f"Result: {json.dumps(result, indent=2)}")


def show_environment_setup():
    """Show how to set up the environment."""
    print("\n⚙️  Environment Setup")
    print("-" * 25)
    
    print("1. Required Environment Variables:")
    print("   SUPABASE_URL=your-supabase-project-url")
    print("   SUPABASE_SERVICE_KEY=your-supabase-service-role-key")
    print("   OPENAI_API_KEY=your-openai-api-key (optional)")
    
    print("\n2. Example .env file (see .env.example):")
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
            print("   " + content.replace('\n', '\n   '))
    
    print("\n3. Docker Usage:")
    print("   docker build -t supabase-mcp .")
    print("   docker run --env-file .env supabase-mcp")


def show_usage_examples():
    """Show usage examples."""
    print("\n📖 Usage Examples")
    print("-" * 20)
    
    print("1. Basic MCP Server Usage:")
    print("   python supabase_mcp/server.py")
    
    print("\n2. Agent Testing:")
    print("   python test_agent.py")
    
    print("\n3. With Real OpenAI API:")
    print("   export OPENAI_API_KEY='your-key'")
    print("   python test_agent.py")
    
    print("\n4. Natural Language Queries (when integrated):")
    examples = [
        "Get all active users created this month",
        "Create a new user with name John and email john@example.com",
        "Update all users with status 'pending' to 'active'",
        "Delete users who haven't logged in for 6 months"
    ]
    
    for example in examples:
        print(f"   • \"{example}\"")


def main():
    """Run the demonstration."""
    try:
        demonstrate_agent_capabilities()
        demonstrate_query_interpretation()
        demonstrate_integration()
        show_environment_setup()
        show_usage_examples()
        
        print("\n✅ Integration Complete!")
        print("\nThe OpenAI model is now properly integrated with the Supabase MCP server.")
        print("The system provides both automated query interpretation and fallback functionality.")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()