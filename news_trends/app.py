"""
App entrypoint
"""

from flask import Flask, request
import os
import json

app = Flask(__name__)

from . import config
app.config.from_object(config.Config)

from . import data_processor

@app.route('/')
def check_if_up():
    """
    Healthcheck endpoint.
    """
    return "Server is running!"

@app.route('/topNews')
def get_top_news():
    """
    Accepts query parameters 'tweets', 'q', and 'additional_params'.
    Returns JSONified representation of list of NewsStory objects
    """
    
    # TODO: add option to select different country

    include_tweets = request.args.get('tweets')
    search_query = request.args.get('q')

    additional_params_string = None
    query_string = request.query_string.decode('utf-8')
    additional_params_location = query_string.find('additionalParams')
    
    if additional_params_location != -1:
        additional_params_string = query_string[additional_params_location:].replace('additionalParams=', '')

    stories = data_processor.get_top_news_stories_and_related_information(search_query, additional_params_string, include_tweets=include_tweets)
    
    return json.dumps({'stories': [story.serialize() for story in stories]})

@app.route('/trends', methods=['GET'])
def get_top_trends():
    """
    Accepts query parameters tweets, news, location_id.
    Returns JSONified representation of a list of TweetTrend objects
    """
    include_tweets = request.args.get('tweets')
    include_news = request.args.get('news')
    location_id = request.args.get('location_id')

    if location_id:
        trends = data_processor.get_twitter_trends_and_related_information(include_tweets, include_news, location_id)
    else:
        trends = data_processor.get_twitter_trends_and_related_information(include_tweets, include_news)

    return json.dumps({'trends': [trend.serialize() for trend in trends]})

@app.route('/tweets', methods=['GET'])
def get_tweets_by_search():
    """
    Accepts query parameters q and count. 'q' is required.
    Returns JSONified representation of list of Tweet objects.
    """
    search_query = request.args.get('q')
    count = request.args.get('count')

    tweets = data_processor.get_tweets_by_search(search_query, count) if count else data_processor.get_tweets_by_search(search_query)

    return json.dumps({'tweets': [tweet.serialize() for tweet in tweets]})

if __name__ == '__main__':
    app.run()