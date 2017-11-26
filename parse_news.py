import os
import get_news
import set_nlp


API_KEY = os.getenv('NEWS_API_KEY')
MIN_SIMILARITY = 0.9
CERTAIN_SIMILARITY = 0.97
MIN_INTERSECTION = 2


nlp = set_nlp.nlp
news = get_news.GetNews(API_KEY)


def get_headlines():
    sources = [
        'bbc-news', 'independent', 'google-news',
        'the-new-york-times', 'fox-news', 'reuters',
        'cnn', 'independent', 'time', 'the-telegraph'
    ]
    headlines = news.get_top_headlines(sources)

    for x in headlines:
        x['nlp'] = nlp('. '.join((x['title'], x['description'])))
        x['lemmas'] = set(map(lambda x: x.lemma_, x['nlp'].ents))

    return headlines


def find_similarity(sentences):
    similarities_list = []

    def iterate_nlps(headlines):
        if not headlines:
            return similarities_list

        sentence_to_compare = headlines[0]['nlp']
        sentence_to_compare_lemmas = headlines[0]['lemmas']
        similarity_dict = {
            'main': headlines[0],
            'similarities': []
        }

        for sentence in headlines[1:]:
            should_append = False
            similarity = sentence_to_compare.similarity(sentence['nlp'])
            sentence_lemmas = sentence['lemmas']
            intersection = len(
                sentence_to_compare_lemmas.intersection(sentence_lemmas))

            if similarity >= CERTAIN_SIMILARITY:
                should_append = True
            elif similarity >= MIN_SIMILARITY:
                if intersection >= MIN_INTERSECTION:
                    should_append = True

            if should_append:
                similarity_dict['similarities'].append((similarity, sentence))
                headlines.remove(sentence)

        similarities_list.append(similarity_dict)

        return iterate_nlps(headlines[1:])
    return iterate_nlps(sentences)
