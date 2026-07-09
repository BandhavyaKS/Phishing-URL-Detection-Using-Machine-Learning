from model import MODEL, extract_features


def predict_url(url):
    features = extract_features(url)
    prediction = MODEL.predict([features])[0]
    return 'Phishing' if prediction == 1 else 'Legitimate'