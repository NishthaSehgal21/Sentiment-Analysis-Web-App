"""Sentiment analysis engine using VADER."""

import re
import threading

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


_LOCK = threading.Lock()
_ANALYZER = None

MAX_TEXT_LENGTH = 5000


def get_analyzer() -> SentimentIntensityAnalyzer:
    """Create and return a reusable VADER analyzer."""
    global _ANALYZER

    with _LOCK:
        if _ANALYZER is None:
            _ANALYZER = SentimentIntensityAnalyzer()

        return _ANALYZER


def classify_compound(compound: float) -> str:
    """Classify sentiment using VADER compound score."""
    if compound >= 0.05:
        return "Positive"

    if compound <= -0.05:
        return "Negative"

    return "Neutral"


def text_statistics(text: str) -> dict:
    """Calculate basic statistics for the input text."""
    words = re.findall(r"\b\w+\b", text)
    sentences = [
        sentence
        for sentence in re.split(r"[.!?]+", text)
        if sentence.strip()
    ]

    return {
        "words": len(words),
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "sentences": max(len(sentences), 1) if text.strip() else 0,
        "avg_word_length": (
            round(sum(len(word) for word in words) / len(words), 2)
            if words
            else 0
        ),
    }


def analyze_sentiment(text: str) -> dict:
    """Analyze the sentiment of the supplied text."""

    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    cleaned = text.strip()

    if not cleaned:
        raise ValueError("Text cannot be empty.")

    if len(cleaned) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Text exceeds the maximum of {MAX_TEXT_LENGTH} characters."
        )

    analyzer = get_analyzer()

    scores = analyzer.polarity_scores(cleaned)

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