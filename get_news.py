import requests


class GetNews:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_base_url = 'https://newsapi.org/v2'

    def get_sources(self, filters=None, items=None):
        """Get news sources.

        items: <list>
          choose what items to get from the response
        filter: <dict>
          filter the response

        eg:
          >>  get_sources(
                  filters={'language': 'es', 'category': 'sport'},
                  items=['name', 'language']
              )
          >>  [{'language': 'es', 'name': 'Marca'}]

        documentation: https://newsapi.org/docs/endpoints/sources
        """
        url = self.api_base_url + '/sources'
        response = requests.get(url, params={'apiKey': self.api_key})
        sources = response.json()['sources']
        if filters:
            sources = list(filter(lambda x: all(x[y] == z for y, z in filters.items()), sources))
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
