import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sentiment_analyzer import analyze_sentiment, classify_compound, text_statistics


class TestClassifyCompound(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(classify_compound(0.5), "Positive")

    def test_negative(self):
        self.assertEqual(classify_compound(-0.5), "Negative")

    def test_neutral(self):
        self.assertEqual(classify_compound(0.0), "Neutral")


class TestAnalyzeSentiment(unittest.TestCase):
    def test_positive_sentence(self):
        r = analyze_sentiment("This product is absolutely amazing and I love it!")
        self.assertEqual(r["sentiment"], "Positive")
        self.assertGreater(r["score"], 0)

    def test_negative_sentence(self):
        r = analyze_sentiment("This is the worst, most disappointing experience ever.")
        self.assertEqual(r["sentiment"], "Negative")
        self.assertLess(r["score"], 0)

    def test_neutral_sentence(self):
        r = analyze_sentiment("The package arrived today and contains the requested items.")
        self.assertEqual(r["sentiment"], "Neutral")

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            analyze_sentiment("   ")

    def test_structure(self):
        r = analyze_sentiment("I love it!")
        for key in ("sentiment", "score", "intensity", "vader", "interpretation", "text_statistics"):
            self.assertIn(key, r)


class TestTextStatistics(unittest.TestCase):
    def test_counts(self):
        s = text_statistics("Hello world. This is a test.")
        self.assertEqual(s["words"], 6)
        self.assertEqual(s["sentences"], 2)


if __name__ == "__main__":
    unittest.main()
