# CodeAlpha URL Shortener

A simple URL shortener built with **Python**, **Flask**, and **SQLite**. It accepts a long URL, generates a unique six-character short code, stores the mapping in a local database, and redirects visitors to the original URL.

## Features

- Create short URLs through a browser form or JSON API.
- Generate unique six-character codes using letters and numbers.
- Store URL mappings in SQLite.
- Redirect short links to their original destinations.
- Return helpful validation and not-found errors.
- Display the ten most recently created links.
- Responsive interface for desktop and mobile screens.

## Requirements

- Python 3.10 or newer
- `pip`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/manzi253-hyber/CodeAlpha_URLShortener.git
   cd CodeAlpha_URLShortener
   ```

2. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the development server:

   ```bash
   python -m flask --app app run --host 127.0.0.1 --port 5000
   ```

4. Open <http://127.0.0.1:5000> in your browser.

The SQLite database is created automatically as `shortener.db` when the application is initialized. It is ignored by Git because it contains local runtime data.

## API Usage

### Create a short URL

Send a `POST` request to `/shorten` with a URL in JSON format:

```bash
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Example response:

```json
{
  "short_code": "aB3xYz",
  "short_url": "http://127.0.0.1:5000/aB3xYz"
}
```

The endpoint also accepts form data with a `url` field. Submitting the same original URL again returns its existing short code instead of creating a duplicate.

### Open a short URL

Visit the generated link:

```text
http://127.0.0.1:5000/aB3xYz
```

The server responds with a redirect to the saved original URL. Unknown codes return a `404` response.

## Project Structure

```text
.
├── app.py                 # Flask application and API routes
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web interface
├── static/
│   ├── script.js          # Form submission behavior
│   └── style.css          # Interface styles
└── .gitignore             # Ignored local files
```

## Validation

The shortener requires URLs with a scheme and host, such as:

```text
https://example.com
http://localhost:3000
```

Invalid or empty values return an error instead of being saved.

## License

This project is available under the license in the repository's `LICENSE` file.
