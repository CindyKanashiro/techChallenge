from logging import info
import sqlite3
import pandas as pd
import joblib
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

CSV_FILENAME = "data/books.csv"


def generate_csv_file():
    conn = sqlite3.connect('data/books.db')

    df = pd.read_sql('SELECT title, category FROM books WHERE category != "Default"', conn)
    df.to_csv(CSV_FILENAME, index = False)
    info("csv file created")


def create_model(csv_filename: str):
    df = pd.read_csv(csv_filename)

    x = df["title"].fillna("")
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2), stop_words='english', lowercase=True)),
        ('clf', RandomForestClassifier())
    ])
    pipeline.fit(X_train, y_train)

    
    y_pred = pipeline.predict(X_test)
    info(classification_report(y_test, y_pred))

    joblib.dump(pipeline, "data/model_books.pkl")
