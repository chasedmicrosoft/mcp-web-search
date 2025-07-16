# MCP Web Search Server

This directory contains a Model Context Protocol (MCP) server that provides web search functionality.

## Files

- `ai_web_search.py` - Main MCP server implementation
- `test_search.py` - Test script to verify search functionality
- `requirements.txt` - Python dependencies
- `setup.sh` - Setup script to create virtual environment and install dependencies
- `venv/` - Python virtual environment (created by setup.sh)
- `mcp-config.json` - MCP server configuration (for standalone usage)
- `README-web-search.md` - Detailed documentation

## Setup

1. Run the setup script:
   ```bash
   cd mcp-web-search
   ./setup.sh
   ```

2. Test the search functionality:
   ```bash
   cd mcp-web-search
   source venv/bin/activate
   python test_search.py
   ```

3. Run the MCP server:
   ```bash
   cd mcp-web-search
   source venv/bin/activate
   python ai_web_search.py
   ```

## VS Code Integration

The server is configured in VS Code's `settings.json` under `chat.mcp.servers` as `my.search.mcp`.

## Features

- Web search using DuckDuckGo (no API key required)
- Configurable number of results (1-10)
- Returns formatted results with titles, URLs, and snippets
- Comprehensive error handling and logging

## Dependencies

- Python 3.10+
- MCP library for server functionality
- DuckDuckGo search library for web searches
- Beautiful Soup for HTML parsing
- Requests for HTTP operations
