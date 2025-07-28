#!/usr/bin/env python3
"""
Test the HTML content extraction functionality offline
"""

import sys
import os

# Add current directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ai_web_search import WebSearchServer
except ImportError as e:
    print(f"Error importing WebSearchServer: {e}")
    sys.exit(1)

def test_html_extraction():
    """Test the HTML text extraction functionality."""
    server = WebSearchServer()
    
    print("Testing HTML Text Extraction")
    print("=" * 50)
    
    # Test HTML samples
    test_html_samples = [
        {
            "name": "Simple HTML",
            "html": """
            <html>
                <head><title>Test Page</title></head>
                <body>
                    <h1>Welcome to Test Page</h1>
                    <p>This is a paragraph with some text.</p>
                    <p>This is another paragraph with <strong>bold text</strong>.</p>
                </body>
            </html>
            """
        },
        {
            "name": "HTML with scripts and styles",
            "html": """
            <html>
                <head>
                    <title>Test Page</title>
                    <style>body { color: red; }</style>
                </head>
                <body>
                    <h1>Content to Keep</h1>
                    <script>console.log('This should be removed');</script>
                    <p>This paragraph should remain.</p>
                    <nav>Navigation should be removed</nav>
                    <footer>Footer should be removed</footer>
                </body>
            </html>
            """
        },
        {
            "name": "Empty HTML",
            "html": "<html><head></head><body></body></html>"
        }
    ]
    
    for i, test_case in enumerate(test_html_samples, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            extracted_text = server._extract_text_from_html(test_case['html'])
            print(f"Extracted: '{extracted_text}'")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*50)

def test_content_truncation():
    """Test the content truncation functionality."""
    server = WebSearchServer()
    
    print("Testing Content Truncation")
    print("=" * 50)
    
    # Test truncation
    test_cases = [
        {
            "name": "Short content (no truncation)",
            "content": "This is a short piece of content.",
            "max_length": 1000
        },
        {
            "name": "Long content (with truncation)",
            "content": "This is a very long piece of content. " * 100,  # ~3700 characters
            "max_length": 200
        },
        {
            "name": "Content with sentences (smart truncation)",
            "content": "First sentence. Second sentence. Third sentence. Fourth sentence. Fifth sentence.",
            "max_length": 50
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Original length: {len(test_case['content'])}")
        print("-" * 30)
        
        try:
            truncated = server._truncate_content(test_case['content'], test_case['max_length'])
            print(f"Truncated length: {len(truncated)}")
            print(f"Truncated: '{truncated[:100]}{'...' if len(truncated) > 100 else ''}'")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_html_extraction()
    test_content_truncation()