#!/usr/bin/env python3
"""
sms_spam_classifier.py
- Downloads the SMS Spam Collection dataset if needed
- Trains a simple text classifier (CountVectorizer + LogisticRegression)
- Saves model and vectorizer into `models/`
"""
import os
import zipfile
import urllib.request
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
DATA_DIR = os.path.join("data", "raw")
ZIP_PATH = os.path.join(DATA_DIR, "smsspamcollection.zip")
RAW_FILE = os.path.join(DATA_DIR, "SMSSpamCollection")
MODEL_PATH = os.path.join("models", "spam_classifier.pkl")
VECT_PATH = os.path.join("models", "vectorizer.pkl")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)


def download_and_extract():
    if os.path.exists(RAW_FILE):
        print(f"Dataset already present: {RAW_FILE}")
        return
    print("Downloading dataset...")
    urllib.request.urlretrieve(DATA_URL, ZIP_PATH)
    print(f"Downloaded to {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)
    print(f"Extracted to {DATA_DIR}")


def load_data():
    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f"Expected dataset file not found: {RAW_FILE}")
    df = pd.read_csv(RAW_FILE, sep="\t", header=None, names=["label", "text"])
    return df


def preprocess_labels(df):
    df = df.copy()
    df["label_num"] = df["label"].map({"ham": 0, "spam": 1})
    return df


def train_and_save(df):
    X = df["text"].astype(str)
    y = df["label_num"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    vect = CountVectorizer(lowercase=True, stop_words='english', max_df=0.95, min_df=2)
    X_train_vec = vect.fit_transform(X_train)
    X_test_vec = vect.transform(X_test)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train_vec, y_train)

    preds = clf.predict(X_test_vec)
    print("Accuracy:", accuracy_score(y_test, preds))
    print("Classification report:\n", classification_report(y_test, preds, digits=4))

    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vect, VECT_PATH)
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved vectorizer to {VECT_PATH}")


if __name__ == '__main__':
    try:
        download_and_extract()
        df = load_data()
        df = preprocess_labels(df)
        train_and_save(df)
    except Exception as e:
        print("Error:", e)
        raise
