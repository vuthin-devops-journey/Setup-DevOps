import datetime
import os

import psycopg2
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Application info", version="2.0.0")

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "devops")
DB_USER = os.environ.get("DB_USER", "devops")
DB_PASS = os.environ.get("DB_PASS", "devops123")
DB_PORT = os.environ.get("DB_PORT", "5432")


def get_db():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )


@app.route("/")
def home():
    return jsonify({"message": "Hello from Team A and B!", "status": "running"})


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })


@app.route("/version")
def version():
    return jsonify({"version": "2.0.0", "app": "devops-journey"})


@app.route("/visits")
def visits():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, "
        "visited_at TIMESTAMP DEFAULT NOW())"
    )
    cur.execute("INSERT INTO visits DEFAULT VALUES")
    cur.execute("SELECT COUNT(*) FROM visits")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"total_visits": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
