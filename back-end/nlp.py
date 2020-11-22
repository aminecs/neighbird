# Imports the Google Cloud client library
from google.cloud import language_v1


def extract_topic(inquiry_str):
    pass


if __name__ == "__main__":
    """
    Natural Language API sample code
    """

    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    text = "i like apples"
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    print(f'text:{text}')
    print(f'sentiment: {sentiment.score}, {sentiment.magnitude}')
