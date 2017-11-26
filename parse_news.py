import os
import get_news
import set_nlp


API_KEY = os.getenv('NEWS_API_KEY')
MIN_SIMILARITY = 0.9
MIN_INTERSECTION = 1

nlp = set_nlp.nlp
news = get_news.GetNews(API_KEY)

headlines = news.get_top_headlines(
    [
        'bbc-news', 'independent', 'google-news',
        'the-new-york-times', 'fox-news', 'reuters',
        'cnn'
    ]
)
titles = list(map(lambda x: '. '.join((x['title'], x['description'])), headlines))


def find_similarity(sentences):
    similarities_list = []
    _sentences = list(map(nlp, sentences))

    def iterate_nlps(nlp_sentences):
        if not nlp_sentences:
            return similarities_list

        sentence_to_compare = nlp_sentences[0]
        sentence_to_compare_entities = set(map(lambda x: x.lemma_, sentence_to_compare.ents))
        similarity_dict = {
            'sentence': sentence_to_compare,
            'similarities': []
        }

        for sentence in nlp_sentences[1:]:
            similarity = sentence_to_compare.similarity(sentence)
            sentence_entities = set(map(lambda x: x.lemma_, sentence.ents))
            if similarity >= MIN_SIMILARITY:
                if len(sentence_to_compare_entities.intersection(sentence_entities)) >= MIN_INTERSECTION:
                    similarity_dict['similarities'].append((similarity, sentence))

        similarities_list.append(similarity_dict)

        return iterate_nlps(nlp_sentences[1:])
    return iterate_nlps(_sentences)
