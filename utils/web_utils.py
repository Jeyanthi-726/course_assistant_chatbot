import requests
from config.config import SERPAPI_KEY

def web_search(query):
    """Perform live web search using SerpAPI"""
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
        }
        response = requests.get(url, params=params)
        data = response.json()
        if "organic_results" in data:
            results = [res["snippet"] for res in data["organic_results"][:3]]
            return "\n".join(results)
        return "No relevant web results found."
    except Exception as e:
        return f"Error in web search: {e}"
