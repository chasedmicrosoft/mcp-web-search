# AI Web Search MCP Server

A Model Context Protocol (MCP) server that provides web search functionality using DuckDuckGo as the search engine.

## Features

- 🔍 **Web Search**: Search the web for information using natural language queries
- 📖 **URL Reading**: Read the full content of web pages from URLs (useful for getting complete context from search results)
- 📊 **Configurable Results**: Control the number of search results returned (1-10)
- 🚀 **Fast & Reliable**: Uses DuckDuckGo for privacy-focused search without API keys
- 🛠 **MCP Compatible**: Fully compatible with the Model Context Protocol standard

## Files Overview

- `ai_web_search.py` - Main MCP server implementation
- `requirements.txt` - Python dependencies
- `setup.sh` - Setup script for virtual environment
- `test_search.py` - Test script to verify functionality
- `README-web-search.md` - This documentation file

## Quick Start

### 1. Setup Virtual Environment

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Run the MCP Server

```bash
python ai_web_search.py
```

### 4. Test the Server (Optional)

```bash
python test_search.py
```

## Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python ai_web_search.py
```

## Usage

### Tool: `web_search`

Searches the web for information and returns relevant results.

**Parameters:**
- `query` (required): The search query string
- `max_results` (optional): Maximum number of results to return (default: 5, max: 10)

**Example:**
```json
{
  "name": "web_search",
  "arguments": {
    "query": "Azure Container Registry best practices",
    "max_results": 5
  }
}
```

**Response:**
Returns formatted search results including:
- Title of each result
- URL of each result
- Snippet/description of each result

### Tool: `read_url`

Reads the full content of a web page from a given URL. This is particularly useful for getting the complete context of pages found in search results.

**Parameters:**
- `url` (required): The URL of the web page to read

**Example:**
```json
{
  "name": "read_url",
  "arguments": {
    "url": "https://example.com/article"
  }
}
```

**Response:**
Returns the full text content of the webpage with:
- HTML content converted to readable text
- Scripts, styles, and navigation elements removed
- Content truncated to 10,000 characters with smart boundary detection
- Proper error handling for network issues or invalid URLs

## Dependencies

- **mcp**: Model Context Protocol Python SDK
- **aiohttp**: Async HTTP client for web requests
- **beautifulsoup4**: HTML parsing for search results
- **lxml**: XML/HTML parser backend

## Configuration

The server uses DuckDuckGo for search, which:
- Requires no API keys
- Provides privacy-focused search
- Has built-in rate limiting
- Returns high-quality results

## Error Handling

The server includes comprehensive error handling:
- Network connectivity issues
- Search service unavailability
- Invalid query parameters
- HTML parsing errors

## Development

### Adding Features

To add new features to the server:

1. Add new tools in the `setup_handlers()` method
2. Implement the tool logic as async methods
3. Update the tool list in `handle_list_tools()`
4. Add corresponding handlers in `handle_call_tool()`

### Testing

Run the test script to verify functionality:

```bash
python test_search.py
```

The test script includes sample searches for:
- Azure-related queries
- Technical documentation
- General web content

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated and dependencies are installed
2. **Network Issues**: Check internet connectivity and firewall settings
3. **No Results**: Try different search terms or check if the search service is available

### Debug Mode

To enable debug logging, modify the logging level in `ai_web_search.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project follows the same license as the parent repository.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the error logs
3. Create an issue in the repository
