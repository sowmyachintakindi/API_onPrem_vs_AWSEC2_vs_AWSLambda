from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

# In-memory "database"
items = {}

# ----------------------------------------
# Health Check
# ----------------------------------------
@app.route("/")
def root():
    return jsonify(status="ok", message="API is running!")

# ----------------------------------------
# CRUD Endpoints
# ----------------------------------------
@app.route("/items/", methods=["POST"])
def create_item():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify(error="Name is required"), 400
    if name in items:
        return jsonify(error="Item already exists"), 400
    items[name] = data
    return jsonify(message="Item created", item=data)

@app.route("/items/<name>", methods=["GET"])
def read_item(name):
    if name not in items:
        return jsonify(error="Item not found"), 404
    return jsonify(items[name])

@app.route("/items/<name>", methods=["PUT"])
def update_item(name):
    if name not in items:
        return jsonify(error="Item not found"), 404
    data = request.json
    items[name] = data
    return jsonify(message="Item updated", item=data)

@app.route("/items/<name>", methods=["DELETE"])
def delete_item(name):
    if name not in items:
        return jsonify(error="Item not found"), 404
    del items[name]
    return jsonify(message=f"Item '{name}' deleted")

# ----------------------------------------
# Performance Testing Endpoints
# ----------------------------------------
@app.route("/fast")
def fast_endpoint():
    return jsonify(status="ok", response_time="fast")

@app.route("/slow")
def slow_endpoint():
    time.sleep(2)
    return jsonify(status="ok", response_time="slow (2s)")

@app.route("/random")
def random_endpoint():
    delay = random.uniform(0.1, 3.0)
    time.sleep(delay)
    return jsonify(status="ok", response_time=f"{delay:.2f}s")

@app.route("/unstable")
def unstable_endpoint():
    if random.random() < 0.2:
        return jsonify(error="Random failure occurred"), 500
    return jsonify(status="ok", message="Request succeeded")

# ----------------------------------------
# Run Server
# ----------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

