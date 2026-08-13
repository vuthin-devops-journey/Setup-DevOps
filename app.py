from flask import Flask, jsoni
import datetime

return jsonify({"message": "Hello DevOps!", "status": "running"})app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello from Team A! and B!", "status": "running"})


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })


@app.route("/version")
def version():
    return jsonify({"version": "1.0.0", "app": "devops-journey"})


if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)

