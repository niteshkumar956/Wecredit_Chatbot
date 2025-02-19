from flask import Flask, request, jsonify, render_template
from chatbot import fintech_chatbot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = fintech_chatbot(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)