import json
import unittest
from unittest.mock import patch, MagicMock

import app as flask_app
from joke_generator import fetch_joke


class TestFetchJoke(unittest.TestCase):
    """Unit tests for the joke_generator.fetch_joke() function."""

    def _mock_response(self, json_data, status_code=200):
        mock = MagicMock()
        mock.status_code = status_code
        mock.json.return_value = json_data
        mock.raise_for_status.return_value = None
        return mock

    @patch("joke_generator.requests.get")
    def test_single_joke(self, mock_get):
        mock_get.return_value = self._mock_response(
            {"error": False, "type": "single", "joke": "Why did the chicken cross the road?"}
        )
        result = fetch_joke()
        self.assertIn("joke", result)
        self.assertEqual(result["joke"], "Why did the chicken cross the road?")
        self.assertEqual(result["type"], "single")

    @patch("joke_generator.requests.get")
    def test_twopart_joke(self, mock_get):
        mock_get.return_value = self._mock_response(
            {
                "error": False,
                "type": "twopart",
                "setup": "Why do programmers prefer dark mode?",
                "delivery": "Because light attracts bugs!",
            }
        )
        result = fetch_joke()
        self.assertIn("joke", result)
        self.assertIn("Why do programmers prefer dark mode?", result["joke"])
        self.assertIn("Because light attracts bugs!", result["joke"])
        self.assertEqual(result["type"], "twopart")

    @patch("joke_generator.requests.get")
    def test_api_error_flag(self, mock_get):
        mock_get.return_value = self._mock_response({"error": True})
        result = fetch_joke()
        self.assertIn("error", result)

    @patch("joke_generator.requests.get", side_effect=__import__("requests").exceptions.Timeout)
    def test_timeout(self, mock_get):
        result = fetch_joke()
        self.assertIn("error", result)
        self.assertIn("timed out", result["error"])

    @patch("joke_generator.requests.get", side_effect=__import__("requests").exceptions.ConnectionError)
    def test_connection_error(self, mock_get):
        result = fetch_joke()
        self.assertIn("error", result)
        self.assertIn("connect", result["error"])

    @patch("joke_generator.requests.get")
    def test_http_error(self, mock_get):
        import requests as req
        mock = MagicMock()
        mock.raise_for_status.side_effect = req.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock
        result = fetch_joke()
        self.assertIn("error", result)


class TestJokeRoute(unittest.TestCase):
    """Integration tests for the Flask /joke route."""

    def setUp(self):
        flask_app.app.config["TESTING"] = True
        self.client = flask_app.app.test_client()

    @patch("app.fetch_joke")
    def test_joke_route_success(self, mock_fetch):
        mock_fetch.return_value = {"joke": "Test joke", "type": "single"}
        response = self.client.get("/joke")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["joke"], "Test joke")
        self.assertEqual(data["type"], "single")

    @patch("app.fetch_joke")
    def test_joke_route_error(self, mock_fetch):
        mock_fetch.return_value = {"error": "Could not connect to joke API."}
        response = self.client.get("/joke")
        self.assertEqual(response.status_code, 503)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
