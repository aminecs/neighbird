# Imports the Google Cloud client library
from google.cloud import language_v1
import spacy

SIMILARITY_THRESHOLD = 0.7


class NLPAnalyzer:
    __instance = None
    __gcp_client = None
    __spacy_nlp = None

    @staticmethod
    def get_instance():
        if NLPAnalyzer.__instance is None:
            NLPAnalyzer.__instance = NLPAnalyzer()
            NLPAnalyzer.__gcp_client = language_v1.LanguageServiceClient()
            NLPAnalyzer.__spacy_nlp = spacy.load("en_core_web_lg")
        return NLPAnalyzer.__instance

    def sort_by_cosine_similarity(self, target_inquiry, other_inquiries):
        target_doc = self.__spacy_nlp(target_inquiry.inquiry_str)

        sorted_inquiries = []
        for inquiry in other_inquiries:
            sorted_inquiries.append((inquiry, target_doc.similarity(self.__spacy_nlp(inquiry.inquiry_str))))

        sorted_inquiries = sorted(sorted_inquiries, key=lambda inquiry_tuple: inquiry_tuple[1], reverse=True)
        return sorted_inquiries

    def sort_by_sentiment_similarity(self, target_inquiry, other_inquiries):
        target_score = self._sentiment_score(target_inquiry.entities)

        sorted_inquiries = []
        for inquiry in other_inquiries:
            sorted_inquiries.append((inquiry, abs(abs(target_score) - abs(self._sentiment_score(inquiry.entities)))))

        sorted_inquiries = sorted(sorted_inquiries, key=lambda inquiry_tuple: inquiry_tuple[1])
        return sorted_inquiries

    def sort_by_cosine_and_sentiment_similarity(self, target_inquiry, other_inquiries):
        target_score = self._sentiment_score(target_inquiry.entities)
        target_doc = self.__spacy_nlp(target_inquiry.inquiry_str)

        sorted_inquiries = []
        for inquiry in other_inquiries:
            similarity = target_doc.similarity(self.__spacy_nlp(inquiry.inquiry_str))
            sentiment = self._sentiment_score(inquiry.entities)
            sorted_inquiries.append((inquiry, abs(abs(1 * target_score) - abs(similarity * sentiment))))

        sorted_inquiries = sorted(sorted_inquiries, key=lambda inquiry_tuple: inquiry_tuple[1])
        return sorted_inquiries

    def get_entity_analysis(self, text, print_info=False):
        # The text to analyze
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # retrieve entities and their sentiments
        response = self.__gcp_client.analyze_entity_sentiment(document=document, encoding_type='UTF32')

        if print_info:
            print(f'--------------------------------------------------------------------\ntext: {text}')
            for entity in response.entities:
                print(f'entity: {entity.name}, sentiment score: {entity.sentiment.score}, '
                      f'sentiment magnitude: {entity.sentiment.magnitude}, salience: {entity.salience}')

        entities = [{'entity': entity.name,
                     'sentiment_score': entity.sentiment.score,
                     'sentiment_magnitude': entity.sentiment.magnitude,
                     'salience': entity.salience} for entity in response.entities]

        # document = language_v1.Document(content=text * 20, type_=language_v1.Document.Type.PLAIN_TEXT)
        # # classify text
        # response = client.classify_text(request={'document': document})
        # categories = response.categories
        # print(categories)

        return entities

    def _sentiment_score(self, entities):
        score = 0
        for entity in entities:
            if entity['sentiment_score'] > 0:
                sign = 1
            else:
                sign = -1
            score += entity['sentiment_score'] * entity['sentiment_magnitude'] + entity['salience'] * sign
        return score


if __name__ == "__main__":
    """
    testing out sentiment and cosine similarity
    """
    from inquiry import Inquiry

    analyzer = NLPAnalyzer.get_instance()

    target_inquiry = 'basketball game last night'
    other_inquiries = ['i loved the basketball game yesterday', 'i hated the basketball game yesterday',
                       'the basketball game yesterday', 'i did not watch the basketball game yesterday',
                       'i liked cooking last night']

    target_inquiry = Inquiry(None, 1, target_inquiry)
    other_inquiries = [Inquiry(None, 1, oi) for oi in other_inquiries]

    print(f'target inquiry: "{target_inquiry.inquiry_str}", '
          f'sentiment score={analyzer._sentiment_score(target_inquiry.entities)}, entities: {target_inquiry.entities}')
    print('---------------------------------- sorted by cosine similarity-----------------------------')
    for i in analyzer.sort_by_cosine_similarity(target_inquiry, other_inquiries):
        print(i[0].inquiry_str, i[1])
    print('---------------------------------- sorted by sentiment similarity-----------------------------')
    for i in analyzer.sort_by_sentiment_similarity(target_inquiry, other_inquiries):
        print(i[0].inquiry_str, i[1], i[0].entities)
    print('------------------------------- sorted by combination of cosine and sentiment ------------------------')
    for i in analyzer.sort_by_cosine_and_sentiment_similarity(target_inquiry, other_inquiries):
        print(i[0].inquiry_str, i[1])
