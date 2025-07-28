#!/usr/bin/env python3
"""
Test script for the read_url tool in the AI Web Search MCP Server
This script tests the new read functionality.
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

async def test_read_url():
    """Test the read URL functionality."""
    server = WebSearchServer()
    
    # Test read URL arguments
    test_cases = [
        {
            "name": "Empty URL (error case)",
            "args": {"url": ""},
        },
        {
            "name": "Invalid URL (error case)", 
            "args": {"url": "https://invalid-url-that-does-not-exist.com"},
        },
        {
            "name": "Simple HTML page",
            "args": {"url": "https://httpbin.org/html"},
        },
    ]
    
    print("Testing Read URL Tool")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 50)
        
        try:
            results = await server.read_url(test_case['args'])
            for result in results:
                # Truncate long content for display
                content = result.text
                if len(content) > 1000:
                    content = content[:1000] + "...[truncated for display]"
                print(content)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(test_read_url())