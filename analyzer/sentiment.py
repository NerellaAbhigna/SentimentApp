import joblib
import os
import numpy as np

# Absolute path handling (VERY IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

logreg_model = joblib.load(
    os.path.join(MODEL_DIR, "logreg_model.pkl")
)

tfidf_vectorizer = joblib.load(
    os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
)

LABEL_MAP = {
    0: "Negative",
    1: "Neutral",
    2: "Positive"
}

def predict_sentiment(comments):
    """
    Predict sentiment using Logistic Regression + TF-IDF
    """

    X = tfidf_vectorizer.transform(comments)

    preds = logreg_model.predict(X)
    probs = logreg_model.predict_proba(X)

    results = []

    for comment, label, prob in zip(comments, preds, probs):
        results.append({
            "comment": comment,
            "sentiment": LABEL_MAP[label],
            "confidence": round(np.max(prob), 3)
        })


    return results
