import os
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return jsonify({
        "usage": "GET /solve?prop=<formula>",
        "example": "/solve?prop=" + "(a&b|c)->d<->~e"
    })

@app.route("/solve")
def solve():
    prop = request.args.get("prop", "")
    if not prop:
        return jsonify({"error": "missing 'prop' query parameter"}), 400
    try:
        result = subprocess.run(
            ["./marina", prop],
            capture_output=True, text=True, timeout=5
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "solver timed out"}), 504

    if result.returncode != 0:
        return jsonify({"error": result.stderr.strip() or "invalid formula"}), 400

    return jsonify({"prop": prop, "result": result.stdout.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render injects PORT
    app.run(host="0.0.0.0", port=port)
