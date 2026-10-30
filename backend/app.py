"""Nákupní seznam — server pro Home Assistant add-on.

Stav (seznamy) drží v SQLite v /data, takže je společný pro všechny
uživatele a přežije restart i update add-onu.
"""
import json
import os
import sqlite3
import threading
from contextlib import closing
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.environ.get("NAKUPNI_DB", os.path.join(BASE_DIR, "nakupni.db"))
PORT = int(os.environ.get("PORT", "8091"))

app = Flask(__name__, static_folder=None)
_lock = threading.Lock()


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS state (
               id INTEGER PRIMARY KEY CHECK (id = 1),
               data TEXT,
               version INTEGER NOT NULL DEFAULT 0,
               updated_at TEXT,
               updated_by TEXT
           )"""
    )
    return conn


def _user():
    return (request.headers.get("X-Remote-User")
            or request.headers.get("X-Forwarded-User")
            or request.headers.get("X-Ingress-User")
            or "unknown")


@app.get("/healthz")
def healthz():
    with closing(_connect()) as conn:
        row = conn.execute("SELECT version FROM state WHERE id = 1").fetchone()
    return jsonify(ok=True, version=row[0] if row else 0)


@app.get("/api/state")
def get_state():
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT data, version, updated_at, updated_by FROM state WHERE id = 1"
        ).fetchone()
    if not row:
        return jsonify(version=0, data=None, updatedBy=None)
    data = json.loads(row[0]) if row[0] else None
    return jsonify(version=row[1], data=data, updatedAt=row[2], updatedBy=row[3])


@app.put("/api/state")
def put_state():
    body = request.get_json(force=True, silent=True) or {}
    data = body.get("data")
    if not isinstance(data, dict):
        return jsonify(error="data musí být objekt"), 400

    base = body.get("base", 0)
    try:
        base = int(base)
    except (TypeError, ValueError):
        base = 0

    user = _user()
    with _lock, closing(_connect()) as conn:
        row = conn.execute("SELECT data, version FROM state WHERE id = 1").fetchone()
        version = row[1] if row else 0

        if base != version:
            return jsonify(error="conflict", version=version,
                           data=json.loads(row[0]) if row and row[0] else None,
                           updatedBy=user), 409

        new_version = version + 1
        conn.execute(
            """INSERT INTO state (id, data, version, updated_at, updated_by)
               VALUES (1, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   data = excluded.data,
                   version = excluded.version,
                   updated_at = excluded.updated_at,
                   updated_by = excluded.updated_by""",
            (json.dumps(data, ensure_ascii=False), new_version, _now(), user),
        )
        conn.commit()

    return jsonify(version=new_version, updatedBy=user)


@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html", max_age=0)


@app.get("/<path:path>")
def static_files(path):
    target = os.path.normpath(os.path.join(STATIC_DIR, path))
    if target.startswith(STATIC_DIR) and os.path.isfile(target):
        return send_from_directory(STATIC_DIR, path)
    # neznámá cesta → aplikace (SPA), funguje i pod ingress prefixem
    return send_from_directory(STATIC_DIR, "index.html", max_age=0)


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    app.run(host="0.0.0.0", port=PORT, threaded=True)
