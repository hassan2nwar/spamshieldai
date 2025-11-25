import pickle
from pathlib import Path
import joblib

# Load the model and vectorizer
model_path = Path('models/spam_classifier.pkl')
vec_path = Path('models/vectorizer.pkl')

if not model_path.exists() or not vec_path.exists():
    raise SystemExit('Required model files not found in `models/`. Run training first.')

# The training script uses joblib.dump; prefer joblib.load, fall back to pickle.load
try:
    model = joblib.load(model_path)
except Exception:
    with model_path.open('rb') as f:
        model = pickle.load(f)

try:
    vectorizer = joblib.load(vec_path)
except Exception:
    with vec_path.open('rb') as f:
        vectorizer = pickle.load(f)

# Test messages
test_messages = [
    "Congratulations! You've won $1000. Click here to claim NOW!",
    "Hey, are we still meeting for coffee tomorrow?",
    "URGENT: Your account has been compromised. Verify immediately.",
    "Thanks for your help with the project yesterday!",
    "FREE entry in 2 a wkly comp to win FA Cup final tkts",
    "Can you pick up some milk on your way home?",
]

print('\n' + '='*70)
print('🔍 SPAM DETECTION RESULTS')
print('='*70)

for msg in test_messages:
    # Vectorize and predict
    msg_vector = vectorizer.transform([msg])

    # Some saved models may be a full pipeline; handle both cases
    try:
        pred = model.predict(msg_vector)[0]
    except Exception:
        # If the model expects raw text (e.g. full pipeline), pass the raw message
        pred = model.predict([msg])[0]

    confidence = None
    try:
        proba = model.predict_proba(msg_vector)
        # If predict_proba accepted raw text above, handle that too
    except Exception:
        try:
            proba = model.predict_proba([msg])
        except Exception:
            proba = None

    if proba is not None:
        # Choose the predicted index (0 or 1)
        confidence = proba[0][int(pred)] * 100

    label = "🚨 SPAM" if int(pred) == 1 else "✅ HAM"

    if confidence is not None:
        print(f"Message: {msg}\nPrediction: {label} ({confidence:.1f}% confidence)\n")
    else:
        print(f"Message: {msg}\nPrediction: {label}\n")
