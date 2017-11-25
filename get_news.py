import requests


class GetNews:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base_url = 'https://newsapi.org/v2'

    def get_sources(self, items=None):
        """Get news sources.

        items: <list>
          used to parse the response
          documentation: https://newsapi.org/docs/endpoints/sources
        """
        url = self.api_base_url + '/sources'
        response = requests.get(url, params={'apiKey': self.api_key})
        sources = response.json()['sources']
        if items:
            return list(map(lambda x: {y: x[y] for y in items}, sources))
        return sources

    def get_top_headlines(self, sources):
        """Get top headlines.

        sources: <list>
          A list of strings with the ids of the news sources
          eg: the values of self.get_sources('id')
          documentation: https://newsapi.org/docs/endpoints/top-headlines
        """
        url = self.api_base_url + '/top-headlines'
        params = {
            'apiKey': self.api_key,
            'sources': ','.join(sources)
        }
        response = requests.get(url, params)
        return response.json()['articles']
