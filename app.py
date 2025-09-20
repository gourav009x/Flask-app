from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


client = MongoClient("mongodb+srv://suraj:kota@cluster0.jidnjug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["testdb"]   # change to your DB name
collection = db["users"]


# API Route
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            error = "Both name and email are required."
        else:
            try:
                collection.insert_one({"name": name, "email": email})
                return redirect(url_for("success"))
            except Exception as e:
                error = str(e)

    return render_template("index.html", error=error)

@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
