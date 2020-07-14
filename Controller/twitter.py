import requests
from datetime import datetime, timedelta
import json


class TweeterController:

    authorization = ""
    url_for_get = 'https://api.twitter.com/1.1/search/tweets.json'
    url_for_post = 'https://api.twitter.com/1.1/tweets/search/30day/sentiments.json'

    def __init__(self, OauthToken):
        self.authorization = "Bearer " + OauthToken

    def search_tweets_get(self, search_param):
        request_headers = {'Authorization':self.authorization}
        min_tweet_date = (datetime.now() - timedelta(days=3)).date().__str__()
        tweets_by_search = requests.get(url=self.url_for_get + "?q=" + search_param + '+since:' + min_tweet_date +
                                            "&lang=en",
                                        headers=request_headers)
        return tweets_by_search

    def search_tweets_post(self, search_param, next):
        request_headers = {'Authorization': self.authorization}
        min_tweet_date = (datetime.now() - timedelta(days=3)).date()
        if next == '':
            request_body = {"query": search_param + ", lang:en",
                            "maxResults": 100,
                            "fromDate": min_tweet_date.strftime('%Y%m%d%H%M')}
        else:
            request_body = {"query": search_param + ", lang:en",
                            "maxResults": 100,
                            "fromDate":  min_tweet_date.strftime('%Y%m%d%H%M'),
                            "next": next}

        request_data = json.dumps(request_body)

        tweets_by_search = requests.post(url=self.url_for_post, headers=request_headers, data=request_data)

        return tweets_by_search
