import unittest

from agents.utils.web import search_web

class TestWeb(unittest.TestCase):

    def test_search_web(self):
        query = "Machine learning"
        results = search_web(query)

        print("Results:", results)

        assert isinstance(results, list), "Search results should be a list."
        assert len(results) > 0, "No search results returned."
        assert "title" in results[0] and "snippet" in results[0], "Results should contain title and snippet."