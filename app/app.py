from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Routes ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return "This is the about page."

@app.route("/api/greet", methods=["POST"])
def greet():
    data = request.get_json()
    name = data.get("name", "World")
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
