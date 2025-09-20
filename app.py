from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # allows API calls from frontend JS if needed

# MongoDB setup
client = MongoClient("mongodb+srv://suraj:kota@cluster0.jidnjug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["testdb"]

# Collections
user_collection = db["users"]
todo_collection = db["todos"]

# --------------------------
# Existing Name/Email Form
# --------------------------
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
                user_collection.insert_one({"name": name, "email": email})
                return redirect(url_for("success"))
            except Exception as e:
                error = str(e)

    return render_template("index.html", error=error)

@app.route("/success")
def success():
    return render_template("success.html")

# --------------------------
# To-Do Feature
# --------------------------
@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()
    item_name = data.get("itemName")
    item_description = data.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"message": "Both fields are required"}), 400

    try:
        todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })
        return jsonify({"message": "To-Do item saved successfully!"})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# --------------------------
# Optional: JSON API Route
# --------------------------
@app.route("/api")
def api():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------------
# Run App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)
