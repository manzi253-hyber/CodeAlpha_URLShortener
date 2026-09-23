import os
import sqlite3
import string
import secrets
from urllib.parse import urlparse

from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'shortener.db')


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT NOT NULL UNIQUE,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        connection.commit()


def is_valid_url(value):
    if not value:
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def generate_short_code():
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ''.join(secrets.choice(alphabet) for _ in range(6))
        with get_db_connection() as connection:
            existing = connection.execute(
                'SELECT 1 FROM urls WHERE short_code = ?', (code,)
            ).fetchone()
        if not existing:
            return code


@app.route('/')
def index():
    with get_db_connection() as connection:
        links = connection.execute(
            'SELECT short_code, original_url FROM urls ORDER BY id DESC LIMIT 10'
        ).fetchall()
    return render_template('index.html', links=links)


@app.route('/shorten', methods=['POST'])
def shorten_url():
    payload = request.get_json(silent=True) or request.form
    original_url = (payload.get('url') or '').strip()

    if not is_valid_url(original_url):
        return jsonify({'error': 'Please provide a valid URL.'}), 400

    with get_db_connection() as connection:
        existing = connection.execute(
            'SELECT short_code FROM urls WHERE original_url = ?', (original_url,)
        ).fetchone()
        if existing:
            short_code = existing['short_code']
        else:
            short_code = generate_short_code()
            connection.execute(
                'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
                (short_code, original_url),
            )
            connection.commit()

    short_url = request.host_url.rstrip('/') + '/' + short_code
    return jsonify({'short_url': short_url, 'short_code': short_code}), 201


@app.route('/<short_code>')
def redirect_url(short_code):
    with get_db_connection() as connection:
        row = connection.execute(
            'SELECT original_url FROM urls WHERE short_code = ?', (short_code,)
        ).fetchone()
    if row is None:
        return jsonify({'error': 'Short URL not found.'}), 404
    return redirect(row['original_url'], code=302)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
