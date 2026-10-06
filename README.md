# Sentix - Sentiment Analysis Web App

## 1. Overview
Sentix is a full-stack NLP web application that analyzes the sentiment of any user-provided text using VADER sentiment analysis (NLTK). It classifies text as **Positive**, **Negative**, or **Neutral**, reports real compound polarity scores, and visualizes results with a gauge, charts, and analytics.

## 2. Problem Statement
Raw text (reviews, feedback, social media posts) carries emotional signal that is hard to quantify manually. Organizations need a quick, transparent way to gauge sentiment at scale.

## 3. Objective
Build a reliable, locally runnable sentiment analysis product with a professional animated frontend, real NLP scoring (no fakes, no paid APIs), and clean architecture.

## 4. Features
- Real VADER sentiment analysis via a Flask backend
- Compound polarity score, intensity, and VADER pos/neg/neu breakdown
- Animated analysis pipeline and result reveal
- SVG sentiment gauge (Negative ← Neutral → Positive)
- Chart.js visualizations for score composition and text statistics
- Quick example buttons, clear button, character/word counters
- Recent-analysis history (localStorage) with Clear History
- Responsive dark glassmorphism UI, hero particle animation
- Accessible: labels, aria attributes, keyboard focus states

## 5. Technologies Used
- **Backend:** Python, Flask, NLTK (VADER)
- **Frontend:** HTML5, CSS3, JavaScript (fetch/AJAX)
- **Charts:** Chart.js (CDN)
- **Testing:** Python `unittest`

## 6. How Sentiment Analysis Works
VADER (Valence Aware Dictionary and sEntiment Reasoner) scores text using a lexicon of words with human-rated sentiment, plus rules for capitalization, punctuation (`!!!`), and negation/intensifiers. It returns:
- `compound`: normalized score in [-1, 1]
- `pos`, `neg`, `neu`: proportion of text that is positive/negative/neutral

Classification thresholds (standard VADER convention):
- `compound >= 0.05` → Positive
- `compound <= -0.05` → Negative
- otherwise → Neutral

Intensity is `abs(compound)`. All metrics come from the actual analyzer output.

## 7. Architecture
Browser (HTML/CSS/JS) → `POST /analyze` (JSON) → Flask route → `sentiment_analyzer.analyze_sentiment()` → VADER → JSON response → UI renders gauge/charts/history.

## 8. Project Structure
```
Sentiment_Analysis_Web_App/
├── app.py
├── sentiment_analyzer.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── assets/
└── tests/
    └── test_sentiment.py
```

## 9. Installation
```bash
cd Sentiment_Analysis_Web_App
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```
The first run automatically downloads the small `vader_lexicon` data file.

## 10. Running the Application
```bash
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## 11. Example Inputs
- Positive: "This product exceeded my expectations and I absolutely love it."
- Negative: "The experience was disappointing and the service was extremely slow."
- Neutral: "The package arrived today and contains the requested items."

## 12. Screenshots
<!-- Add screenshots of the hero, analyzer result, analytics, and mobile layout here. -->

## 13. Testing
```bash
python -m unittest discover tests
```
Tests cover positive, negative, neutral, and empty input, plus the scoring structure and text statistics.

## 14. Future Enhancements
- Fine-tuned transformer models (e.g., DistilBERT) for higher accuracy
- Batch file upload (.csv) analysis
- Exportable reports and CSV download of history
- Per-sentence sentiment highlighting

## 15. Learning Outcomes
- Building REST APIs with Flask and consuming them via fetch
- Applying VADER NLP for real sentiment scoring
- Responsive, accessible UI with glassmorphism and CSS/JS animations
- Writing executable unit tests for NLP logic

## 16. Author
Author: [YOUR NAME]
