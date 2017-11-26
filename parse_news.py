import os
import en_core_web_lg
from get_news import GetNews


MIN_SIMILARITY = 0.9
CERTAIN_SIMILARITY = 0.97
API_KEY = os.getenv('NEWS_API_KEY')
NEWS = GetNews(API_KEY)
NLP = en_core_web_lg.load()


class NewsParser:
    def __init__(self, nlp, news):
        self.nlp = nlp
        self.news = news
        self.sources = [
            'bbc-news', 'independent', 'google-news',
            'the-new-york-times', 'fox-news', 'reuters',
            'cnn', 'independent', 'time', 'the-telegraph'
        ]

    def _get_keywords(self, nlp_item, min_length=3):
        as_lowercase_strings = map(lambda x: x.lower(), map(str, nlp_item.ents))
        as_words = ' '.join(as_lowercase_strings).split()
        final_keywords = filter(lambda x: len(x) >= min_length, as_words)
        return final_keywords

    def get_headlines(self):
        headlines = self.news.get_top_headlines(self.sources)

        for x in headlines:
            x['nlp'] = self.nlp('. '.join((x['title'], x['description'])))
            x['lemmas'] = set(map(lambda x: x.lemma_, x['nlp'].ents))
            x['keywords'] = set(self._get_keywords(x['nlp']))
        return headlines

    def news_grouped_by_similarity(self, headlines, keywords='keywords', min_intersection=3):
        similarities_list = []

        def iterate_nlps(headlines):
            if not headlines:
                similarities_list.sort(key=lambda x: len(x['similarities']), reverse=True)
                return similarities_list

            sentence_to_compare = headlines[0]['nlp']
            sentence_to_compare_keywords = headlines[0][keywords]
            similarity_dict = {
                'main': headlines[0],
                'similarities': []
            }

            for sentence in headlines[1:]:
                should_append = False
                similarity = sentence_to_compare.similarity(sentence['nlp'])
                sentence_keywords = sentence[keywords]
                intersection = len(
                    sentence_to_compare_keywords.intersection(sentence_keywords))

                if similarity >= CERTAIN_SIMILARITY:
                    should_append = True
                elif similarity >= MIN_SIMILARITY:
                    if intersection >= min_intersection:
                        should_append = True

                if should_append:
                    similarity_dict['similarities'].append((similarity, sentence))
                    headlines.remove(sentence)

            similarities_list.append(similarity_dict)

            return iterate_nlps(headlines[1:])
        return iterate_nlps(headlines)

    def parse_results(self, similarities_list):
        def dict_key_filter(dict_, keep):
            return {k: v for k, v in dict_.items() if k in keep}

        parsed_results = {'news': {}}
        news_id = 1

        for news in similarities_list:
            similarities = news['similarities']
            keep = ('title', 'description', 'source', 'url')

            if similarities:
                parsed_results['news'][news_id] = {}
                parsed_results['news'][news_id]['length'] = len(similarities) + 1
                parsed_results['news'][news_id]['headlines'] = [
                    dict_key_filter(i[1], keep) for i in similarities
                ]
                parsed_results['news'][news_id]['headlines'].append(
                    dict_key_filter(news['main'], keep)
                )
                news_id += 1
        return parsed_results

    def final_results(self, keywords='keywords', min_intersection=3):
        headlines = self.get_headlines()
        grouped = self.news_grouped_by_similarity(headlines, keywords, min_intersection)
        return self.parse_results(grouped)
