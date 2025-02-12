import requests
from agents.config import WIKIPEDIA_API_URL

def search_web(query: str):
    search_url = f"{WIKIPEDIA_API_URL}?action=query&list=search&srsearch={query}&format=json"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        results = response.json().get("query", {}).get("search", [])
        return [{"title": item["title"], "snippet": item["snippet"]} for item in results[:8]] 
    except requests.RequestException as e:
        return []
