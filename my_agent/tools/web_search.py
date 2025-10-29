import logging

import os
import requests
import pathlib

import dotenv

dotenv.load_dotenv(dotenv_path=pathlib.Path("./../.env"))

#API_KEY = os.getenv("GOOGLE_API_KEY")
# API_KEY = "AIzaSyBxSVxle3tWf77uWGKiSzPvqfcCwCDZMdM"
API_KEY = "AIzaSyBkLpz8J0daF8PF2f14RXwXAouyaxR6Rhw"
CX = "e173d3da7360c4ed8"

logger = logging.getLogger(__name__)

def web_search(query: str) -> dict:
    """Performs a web search and returns the top results.

    
    Args:
        query (str): The search query.
        context (ToolContext): The tool execution context.

    Returns:
        dict: A dictionary containing the search results.
    Example:
        >>> web_search("What is the weather in Nairobi?", context)
        {'results': [{'title': ..., 'snippet': ..., 'url': ...}, ...]}
    """
    
    page = 1
    start = (page - 1) * 10 + 1

    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={query}&start={start}"

    data = requests.get(url).json()

    # Iteration over search results
    search_items = data.get("items")

    results_list = []

    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        # get the page title
        results_list.append({
            "title": search_item.get("title", "N/A"),
            "snippet": search_item.get("snippet", "N/A"),
            "url": search_item.get("link", "N/A"),
            "html_snippet": search_item.get("htmlSnippet", "N/A")
        })
    
    logger.info(f"Performing web search for query: {query}")
    result = {
        "results": results_list
    }
    return result
