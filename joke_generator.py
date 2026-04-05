import requests

JOKE_API_URL = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist"


def fetch_joke():
    """Fetch a random joke from JokeAPI.

    Returns a dict with keys:
      - "joke" (str): the joke text
      - "type" (str): "single" or "twopart"
    On failure, returns a dict with key "error" (str).
    """
    try:
        response = requests.get(JOKE_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return {"error": "Joke API returned an error."}

        if data.get("type") == "twopart":
            joke_text = f"{data['setup']} ... {data['delivery']}"
        else:
            joke_text = data.get("joke", "")

        return {"joke": joke_text, "type": data.get("type", "single")}

    except requests.exceptions.Timeout:
        return {"error": "Request to joke API timed out."}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to joke API."}
    except requests.exceptions.HTTPError:
        return {"error": "Joke API request failed with an HTTP error."}
    except Exception:
        return {"error": "An unexpected error occurred while fetching a joke."}
