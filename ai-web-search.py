#!/usr/bin/env python3
"""
MCP Server for Web Search
Provides a web search tool that can search the internet and return relevant results.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus
import aiohttp
from bs4 import BeautifulSoup
import re

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearchServer:
    """MCP Server that provides web search functionality."""
    
    def __init__(self):
        self.server = Server("web-search-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        """Set up the MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="web_search",
                    description="Search the web for information using a search query. Returns relevant search results with titles, URLs, and snippets.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find information on the web"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of search results to return (default: 5, max: 10)",
                                "default": 5,
                                "minimum": 1,
                                "maximum": 10
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            if name == "web_search":
                return await self.web_search(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def web_search(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Perform a web search and return results.
        
        Args:
            arguments: Dictionary containing 'query' and optional 'max_results'
        
        Returns:
            List of TextContent with search results
        """
        query = arguments.get("query", "")
        max_results = arguments.get("max_results", 5)
        
        if not query:
            return [TextContent(
                type="text",
                text="Error: Search query is required"
            )]
        
        try:
            # Use DuckDuckGo search (no API key required)
            results = await self._search_duckduckgo(query, max_results)
            
            if not results:
                return [TextContent(
                    type="text",
                    text=f"No search results found for query: {query}"
                )]
            
            # Format results
            formatted_results = self._format_search_results(query, results)
            
            return [TextContent(
                type="text",
                text=formatted_results
            )]
            
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return [TextContent(
                type="text",
                text=f"Error performing web search: {str(e)}"
            )]
    
    async def _search_duckduckgo(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """
        Search using DuckDuckGo.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results with title, url, and snippet
        """
        results = []
        
        try:
            # DuckDuckGo HTML search
            search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        results = self._parse_duckduckgo_results(html, max_results)
                    else:
                        logger.error(f"DuckDuckGo search failed with status: {response.status}")
                        
        except Exception as e:
            logger.error(f"Error in DuckDuckGo search: {e}")
            # Fallback to alternative search method
            results = await self._search_fallback(query, max_results)
        
        return results
    
    def _parse_duckduckgo_results(self, html: str, max_results: int) -> List[Dict[str, str]]:
        """
        Parse DuckDuckGo search results from HTML.
        
        Args:
            html: HTML content from DuckDuckGo
            max_results: Maximum number of results
            
        Returns:
            List of parsed search results
        """
        results = []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find search result containers
            result_containers = soup.find_all('div', class_='result')
            
            for container in result_containers[:max_results]:
                try:
                    # Extract title and URL
                    title_link = container.find('a', class_='result__a')
                    if not title_link:
                        continue
                    
                    title = title_link.get_text(strip=True)
                    url = title_link.get('href', '')
                    
                    # Extract snippet
                    snippet_elem = container.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    logger.warning(f"Error parsing search result: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing DuckDuckGo results: {e}")
        
        return results
    
    async def _search_fallback(self, query: str, max_results: int) -> List[Dict[str, str]]:
        """
        Fallback search method when primary search fails.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of search results
        """
        # This is a simple fallback that could be expanded with other search engines
        # For now, we'll return a message indicating the search failed
        return [{
            'title': 'Search Service Unavailable',
            'url': '',
            'snippet': f'Unable to perform web search for "{query}" at this time. Please try again later.'
        }]
    
    def _format_search_results(self, query: str, results: List[Dict[str, str]]) -> str:
        """
        Format search results for display.
        
        Args:
            query: Original search query
            results: List of search results
            
        Returns:
            Formatted string with search results
        """
        formatted = f"Web Search Results for: '{query}'\n"
        formatted += "=" * 50 + "\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            if result['url']:
                formatted += f"   URL: {result['url']}\n"
            if result['snippet']:
                formatted += f"   {result['snippet']}\n"
            formatted += "\n"
        
        return formatted
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="web-search-server",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

async def main():
    """Main entry point."""
    server = WebSearchServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())