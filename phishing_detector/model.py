# model.py
import os
import re
from urllib.parse import urlparse

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'url_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'phishing_url_model.pkl')

SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'secure', 'account', 'update', 'password', 'bank', 'paypal',
    'signin', 'confirm', 'free', 'claim', 'urgent', 'reset', 'support', 'document',
    'service', 'alert', 'click', 'warning', 'payment', 'suspension', 'download', 'gift'
]


def extract_features(url):
    if not isinstance(url, str):
        url = ''
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    features = []

    features.append(len(url))
    features.append(len(domain))
    features.append(len(path))
    features.append(int(parsed.scheme != 'https'))
    features.append(url.count('@'))
    features.append(url.count('-'))
    features.append(url.count('_'))
    features.append(url.count('.'))
    features.append(url.count('/'))
    features.append(len(re.findall(r'\d', url)))
    features.append(int('www' in domain))
    features.append(int(any(keyword in url for keyword in SUSPICIOUS_KEYWORDS)))
    features.append(int(domain.startswith('www.')))
    features.append(int(re.search(r'\d{1,3}(?:\.\d{1,3}){3}', url) is not None))
    features.append(int(parsed.netloc.count('.') > 1))
    return features


def load_or_train_model():
    expected_feature_count = len(extract_features('https://example.com'))

    if os.path.exists(MODEL_PATH) and os.path.exists(DATA_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            if hasattr(model, 'n_features_in_') and model.n_features_in_ == expected_feature_count:
                return model
        except Exception:
            pass

    df = pd.read_csv(DATA_PATH)
    df['label'] = df['label'].map({'phishing': 1, 'legitimate': 0})

    df['features'] = df['url'].apply(extract_features)
    X = list(df['features'])
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, model.predict(X_test))
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


MODEL = load_or_train_model()