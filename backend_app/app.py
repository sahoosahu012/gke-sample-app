from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json

app = Flask(__name__)
CORS(app)

DATA_DIR = os.environ.get("DATA_DIR", "/tmp/data")
DATA_FILE = os.path.join(DATA_DIR, "names.json")
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def read_names():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_names(names):
    with open(DATA_FILE, "w") as f:
        json.dump(names, f)

@app.route("/api/add-name", methods=["POST"])
def add_name():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error":"name required"}), 400
    names = read_names()
    names.append(name)
    write_names(names)
    return jsonify({"message":"added","names":names}), 201

@app.route("/api/names", methods=["GET"])
def get_names():
    return jsonify({"names": read_names()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

