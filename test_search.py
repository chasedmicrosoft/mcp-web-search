#!/usr/bin/env python3
"""
Test script for the AI Web Search MCP Server
This script demonstrates how to test the web search functionality.
"""

import asyncio
import json
import sys
import os

# Add current directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_web_search import WebSearchServer
except ImportError as e:
    print(f"Error importing WebSearchServer: {e}")
    print("Make sure you have installed the dependencies with: ./setup.sh")
    print("And activated the virtual environment with: source venv/bin/activate")
    sys.exit(1)

async def test_web_search():
    """Test the web search functionality."""
    server = WebSearchServer()
    
    # Test search arguments
    test_queries = [
        {"query": "Azure Container Registry best practices", "max_results": 3},
        {"query": "Python MCP server tutorial", "max_results": 5},
        {"query": "artificial intelligence news 2024", "max_results": 2}
    ]
    
    print("Testing Web Search MCP Server")
    print("=" * 40)
    
    for i, args in enumerate(test_queries, 1):
        print(f"\nTest {i}: Searching for '{args['query']}'")
        print("-" * 40)
        
        try:
            results = await server.web_search(args)
            for result in results:
                print(result.text)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*40)

if __name__ == "__main__":
    asyncio.run(test_web_search())