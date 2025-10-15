from flask import Flask, render_template, request, redirect
import requests, os

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://app2:5000") # default to in-cluster service

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            try:
                requests.post(f"{BACKEND_URL}/api/add-name", json={"name": name}, timeout=3)
            except Exception:
                pass
        return redirect("/")
    # GET
    names = []
    try:
        res = requests.get(f"{BACKEND_URL}/api/names", timeout=3)
        names = res.json().get("names", [])
    except Exception:
        names = []
    return render_template("index.html", names=names)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


