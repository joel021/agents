import unittest

from unittest.mock import patch
from agents.config import WIKIPEDIA_API_KEY
from agents.utils.web import search_web

class TestWeb(unittest.TestCase):

    @patch("requests.get")
    def test_search_web(self, mock_get):
        query = "Machine learning"
        mock_response = {
            "query": {
                "search": [
                    {"title": "Machine Learning", "snippet": "Machine learning is a method of data analysis..."},
                    {"title": "Deep Learning", "snippet": "Deep learning is a subset of machine learning..."}
                ]
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        results = search_web(query)
        print("Results:", results)
        
        assert isinstance(results, list), "Search results should be a list."
        assert len(results) > 0, "No search results returned."
        assert "title" in results[0] and "snippet" in results[0], "Results should contain title and snippet."
        mock_get.assert_called_once_with(f"{WIKIPEDIA_API_KEY}?action=query&list=search&srsearch={query}&format=json")