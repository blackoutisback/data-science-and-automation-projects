# System imports to prevent PyTorch CPU multi-threading freeze on Windows
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Standard library and NLP imports
import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# Load the spaCy medium English language model
nlp = spacy.load("en_core_web_md")

# Add spacytextblob pipeline component for sentiment analysis
nlp.add_pipe("spacytextblob")


def load_and_preprocess_data(file_path):
    """
    Loads the Amazon dataset, removes missing values in 'reviews.text',
    and returns a cleaned pandas Series.
    """
    # Load dataset
    df = pd.read_csv("Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.zip")

    # Drop rows where 'reviews.text' is missing
    clean_df = df.dropna(subset=["reviews.text"])

    return clean_df["reviews.text"]


def clean_text(text):
    """
    Preprocesses raw text by converting to lowercase, stripping whitespace,
    and removing stop words and punctuation.

    # Always add # before all the lines of pseudo-code.
    # FUNCTION clean_text(text):
    #     doc = PROCESS text WITH nlp
    #     tokens = FILTER token IN doc WHERE NOT is_stop AND NOT is_punct
    #     RETURN JOIN tokens WITH " "
    # END FUNCTION

    NOTE: Use this for keyword extraction, display, or topic modeling,
    NOT for direct sentiment analysis scoring.
    """
    doc = nlp(text)
    # Filter out stop words, punctuation, and empty tokens
    tokens = [
        token.text.lower().strip()
        for token in doc
        if not token.is_stop and not token.is_punct and token.text.strip()
    ]
    return " ".join(tokens)


def analyze_sentiment(review_text):
    """
    Analyzes sentiment of a given review using spaCyTextBlob.
    Expects original/unfiltered text to retain negations (e.g., 'not', 'never').
    Returns the polarity, subjectivity, and predicted sentiment label.

    # Always add # before all the lines of pseudo-code.
    # FUNCTION analyze_sentiment(review_text):
    #     doc = PROCESS review_text WITH nlp
    #     polarity = GET doc._.blob.polarity
    #     subjectivity = GET doc._.blob.subjectivity
    #     IF polarity > 0.1 THEN sentiment = "Positive"
    #     ELSE IF polarity < -0.1 THEN sentiment = "Negative"
    #     ELSE sentiment = "Neutral"
    #     RETURN polarity, subjectivity, sentiment
    # END FUNCTION
    """
    doc = nlp(review_text)

    # Retrieve polarity score (-1.0 to 1.0) and subjectivity score
    polarity = doc._.blob.polarity
    subjectivity = doc._.blob.subjectivity

    # Classify sentiment based on polarity
    if polarity > 0.1:
        sentiment_label = "Positive"
    elif polarity < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return {
        "Polarity": round(polarity, 3),
        "Subjectivity": round(subjectivity, 3),
        "Sentiment": sentiment_label,
    }


def compare_reviews_similarity(review1, review2):
    """
    Computes semantic similarity between two reviews using spaCy's word vectors.
    """
    doc1 = nlp(review1)
    doc2 = nlp(review2)
    return round(doc1.similarity(doc2), 4)


# Main execution block
if __name__ == "__main__":
    file_name = (
        "Datafiniti_Amazon_Consumer_Reviews_of_Amazon_Products_May19.csv"
    )

    try:
        # 1. Load data
        reviews = load_and_preprocess_data(file_name)
        print(f"Successfully loaded {len(reviews)} reviews.")

        # 2. Test sentiment analysis on sample reviews
        sample_reviews = [
            reviews.iloc[0],  # Sample 1 from dataset
            reviews.iloc[10],  # Sample 2 from dataset
            "This item is not good at all, very disappointed with the quality.",  # Critical negation test
            "Absolutely loved it! Works like a charm and delivery was super fast.",  # Positive test
        ]

        print("\n--- Sentiment Analysis Results ---")
        for idx, sample in enumerate(sample_reviews, 1):
            # Pass ORIGINAL text to analyze_sentiment to retain negations like 'not'
            result = analyze_sentiment(sample)
            cleaned_sample = clean_text(sample)

            print(f"\nReview #{idx}: {sample}")
            print(f"Cleaned Tokens (For display/keywords): {cleaned_sample}")
            print(
                f"Polarity: {result['Polarity']} | "
                f"Subjectivity: {result['Subjectivity']} | "
                f"Sentiment: {result['Sentiment']}"
            )

        # 3. Test Similarity between two reviews
        rev_a = reviews.iloc[0]
        rev_b = reviews.iloc[1]
        similarity_score = compare_reviews_similarity(rev_a, rev_b)

        print("\n--- Similarity Analysis ---")
        print(f"Review A: {rev_a[:60]}...")
        print(f"Review B: {rev_b[:60]}...")
        print(f"Similarity Score: {similarity_score}")

    except FileNotFoundError:
        print(
            f"Error: Could not locate '{file_name}'. "
            "Ensure it is in the working directory."
        )