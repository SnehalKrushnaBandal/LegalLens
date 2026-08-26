import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Sample Dataset for Training
data = {
    'text': [
        "this is a secret message", "confidential data for you", 
        "top secret document attached", "private information strictly confidential",
        "hello how are you doing", "meeting scheduled for tomorrow",
        "please review the report", "the project is on track",
        "win money now click here", "you won a lottery prize",
        "account hacked reset password", "get rich quick with this scheme",
        "free iphone for first 10 users", "click link to claim your reward",
        "buy cheap medicines online", "urgent action required on your account"
    ],
    'label': [
        'secure', 'secure', 'secure', 'secure', 'secure', 'secure', 'secure', 'secure',
        'spam', 'spam', 'spam', 'spam', 'spam', 'spam', 'spam', 'spam'
    ]
}

df = pd.DataFrame(data)

# Create and Train Model Pipeline
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)),
    MultinomialNB()
)

model.fit(df['text'], df['label'])

def classify_message(message):
    """
    Classifies a message as 'secure' or 'spam' using the trained ML model.
    """
    prediction = model.predict([message])[0]
    return prediction

if __name__ == "__main__":
    # Test cases
    test_msgs = ["this is a secret message", "win money now click here"]
    for msg in test_msgs:
        print(f"Message: '{msg}' -> Result: {classify_message(msg)}")
