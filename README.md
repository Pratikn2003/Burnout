# Burnout

A Flask-based Burnout Predictor application that uses machine learning to assess burnout risk and provides stress-relief features.

## Features

- User registration and authentication
- Daily burnout prediction using a Random Forest ML model
- History and dashboard views
- **Random Joke Generator** – a stress-relief endpoint that fetches a fresh joke on demand

## Random Joke Endpoint

### `GET /joke`

Returns a random joke fetched from [JokeAPI](https://v2.jokeapi.dev).

**Example request:**
```bash
curl http://localhost:5000/joke
```

**Success response (`200 OK`):**
```json
{
  "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
  "type": "twopart"
}
```

**Error response (`503 Service Unavailable`):**
```json
{
  "error": "Could not connect to joke API."
}
```

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Running Tests

```bash
python -m pytest test_joke.py -v
```
