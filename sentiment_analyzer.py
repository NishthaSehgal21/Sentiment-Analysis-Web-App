"""Sentiment analysis engine built on VADER (NLTK)."""

import os
import re
import threading

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

os.environ.setdefault("NLTK_ALLOW_PROXIED_URLOPEN", "1")
try:
    import nltk.pathsec
    nltk.pathsec.ALLOW_PROXIED_FETCH = True
except Exception:
    pass

_LOCK = threading.Lock()
_ANALYZER = None

MAX_TEXT_LENGTH = 5000


def _ensure_lexicon() -> None:
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)


def get_analyzer() -> SentimentIntensityAnalyzer:
    global _ANALYZER
    with _LOCK:
        if _ANALYZER is None:
            _ensure_lexicon()
            _ANALYZER = SentimentIntensityAnalyzer()
        return _ANALYZER


def classify_compound(compound: float) -> str:
    if compound >= 0.05:
        return "Positive"
    if compound <= -0.05:
        return "Negative"
    return "Neutral"


def text_statistics(text: str) -> dict:
    words = re.findall(r"\b\w+\b", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    return {
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "sentences": max(len(sentences), 1) if text.strip() else 0,
        "avg_word_length": round(sum(len(w) for w in words) / len(words), 2) if words else 0,
    }


def analyze_sentiment(text: str) -> dict:
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Text cannot be empty.")
    if len(cleaned) > MAX_TEXT_LENGTH:
        raise ValueError(f"Text exceeds the maximum of {MAX_TEXT_LENGTH} characters.")

    scores = get_analyzer().polarity_scores(cleaned)
    compound = round(scores["compound"], 4)
    sentiment = classify_compound(compound)
    intensity = round(abs(compound), 4)

    interpretations = {
        "Positive": (
            "The text expresses a positive emotional tone."
            if compound < 0.5
            else "The text expresses a strongly positive emotional tone."
        ),
        "Negative": (
            "The text expresses a negative emotional tone."
            if compound > -0.5
            else "The text expresses a strongly negative emotional tone."
        ),
        "Neutral": "The text is largely factual or emotionally balanced.",
    }

    return {
        "sentiment": sentiment,
        "score": compound,
        "intensity": intensity,
        "vader": {
            "positive": round(scores["pos"], 4),
            "negative": round(scores["neg"], 4),
            "neutral": round(scores["neu"], 4),
            "compound": compound,
        },
        "interpretation": interpretations[sentiment],
        "text_statistics": text_statistics(cleaned),
    }
