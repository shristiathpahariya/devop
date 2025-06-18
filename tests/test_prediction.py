import pytest
import joblib
from src import predict  # Make sure your original script is named predict.py and lives in src/

# Paths to your saved model and vectorizer
MODEL_PATH = 'model/model.pkl'
VECTORIZER_PATH = 'model/vectorizer.pkl'

@pytest.fixture(scope='module')
def model_and_vectorizer():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer

def test_model_prediction(model_and_vectorizer):
    model, vectorizer = model_and_vectorizer

    sample_text = "The product is amazing and I love it!"
    prediction = predict.predict_sentiment(model, vectorizer, sample_text)

    assert prediction in ['positive', 'negative', 'neutral'], f"Unexpected label: {prediction}"
