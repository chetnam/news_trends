"""
Serves as the data access layer
Interaction to APIs, database would be contained in this file
"""

import tweepy
from tweepy import OAuthHandler, TweepError
import requests
import json

from . import settings # import env_vars
env_vars = settings.env_vars
from . import utils
from . import connections

# objects to share
conns = connections.Connections()
news_api_key = env_vars['NEWS_API_KEY']

# -----------------------TWITTER--------------------
# 23424977 is WOEID for USA
def get_twitter_trends(location_id=23424977):
    """
    Returns list of dictionaries, each dictionary a trend.
    Location defaults to US trends; set location_id to 1 for global trends
    """
    try:
        twitter_api = conns.get_twitter_api_connection()
        results = twitter_api.trends_place(id=location_id)
        return results[0]['trends']
    except TweepError as te:
        if te.api_code == 34:
            # if page does not exist
            return []
        else:
            raise te

def get_tweets_by_search(query, count=25, result_type="recent", lang="en"):
    """
    Returns a list dictionaries, each dictionary represents a tweet
    Given query will be truncated to 500 characters if longer.
    """

    # twitter api has 500 charater limit for query
    if len(query) > 500:
        query = query[0:500]

    twitter_api = conns.get_twitter_api_connection()

    results = [status._json for status in tweepy.Cursor(twitter_api.search, q=query, result_type=result_type, include_entities=False, lang=lang).items(count)]
    
    return results

# -----------------------NEWS------------------------
def get_news_response(request_url):
    """
    Helper method to deal with all news API requests
    """
    response = requests.get(request_url)
    
    if response.status_code!=200:
        # TODO: get error message from response
        raise Exception(f'News API returned status_code {response.status_code}, {json.loads(response.content)["message"]}')

    # returns list of dictionaries
    return json.loads(response.content)['articles']

def get_top_news(search_query=None, additional_query_params=None, country='us', api_key=news_api_key):
    """
    Returns list of dictionaries, each dictionary a news story

    additional_query_params allows ability to use any parameters NewsAPI provides that aren't handled otherwise (i.e. besides country and search_query)
    if using 'news_sources' in additional_query_params, country must be set to None; otherwise, unexpected behavior might occur

    additional_query_params must be a string
    """

    base_news_url = 'https://newsapi.org/v2/top-headlines'

    # build query_string
    query_string = ''

    query_string = utils.build_part_of_query_string('country', country, query_string)
    query_string = utils.build_part_of_query_string('q', search_query, query_string)

    if additional_query_params:
        if additional_query_params[0]=='&':
            additional_query_params = additional_query_params[1:]
        query_string = utils.build_part_of_query_string('', additional_query_params, query_string)
    
    # add api_key
    query_string = utils.build_part_of_query_string('apiKey', api_key, query_string)

    request_url = f'{base_news_url}?{query_string}'
    
    return get_news_response(request_url)

def get_all_news(additional_query_params = None, api_key=news_api_key):
    """
    Returns list of dictionaries, each dictionary a news story.
    Passes requests to 'Everything' endpoint of NewsAPI.
    additional_query_params must be a string
    """
    base_news_url = 'https://newsapi.org/v2/everything'

    if additional_query_params and additional_query_params[0]=='&':
        additional_query_params = additional_query_params[1:]

    request_url = f'{base_news_url}?{f"{additional_query_params}&" if additional_query_params else ""}apiKey={api_key}'

    return get_news_response(request_url)
    

# ----------------------HELPERS---------------------------