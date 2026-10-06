"""Sentix - Flask backend for the Sentiment Analysis Web App."""

from flask import Flask, jsonify, render_template, request

from sentiment_analyzer import MAX_TEXT_LENGTH, analyze_sentiment

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 64 * 1024  # reject huge payloads


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    text = data.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error": "Please enter some text to analyze."}), 400
    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({"error": f"Text is too long. Maximum {MAX_TEXT_LENGTH} characters."}), 413

    try:
        result = analyze_sentiment(text)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:  # noqa: BLE001 - never leak internals
        return jsonify({"error": "The analyzer could not process this text. Please try again."}), 500

    return jsonify(result), 200


if __name__ == "__main__":
    app.run()  # remove debug=True for submission
