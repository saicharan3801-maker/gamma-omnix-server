import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

@app.get("/")
def home():
    return jsonify({
        "name": "GAMMA OMNIX AI",
        "status": "online"
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.post("/chat")
def chat():
    if not client:
        return jsonify({"error": "Server API key is not configured"}), 503

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message
        )
        return jsonify({"reply": response.text or "No response received"})
    except Exception:
        app.logger.exception("Gemini request failed")
        return jsonify({"error": "AI request failed"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
  
