"""
Interacts with data access layer and 
processes returned data into objects and responses 
to pass to routes/controller layer
"""

from . import data_retriever
from . import models

def convert_to_news_story_object(stories):
    """
    Helper method that accepts a list of dictionaries and returns a list of NewsStory objects
    """
    news_stories_list = [models.NewsStory(story['title'], story['author'], story['publishedAt'], story['content'], story['url'], story['source']) for story in stories if story['content']]

    return news_stories_list

def get_top_news_stories(search_query=None, additional_query_params=None, country='us'):
    """
    Returns list of NewsStory objects containing top news stories
    """
    
    stories = data_retriever.get_top_news(search_query, additional_query_params, country)

    return convert_to_news_story_object(stories)

def get_all_news_stories(additional_query_params=None):
    """
    Returns list of NewsStory objects containing any recent stories
    """

    stories = data_retriever.get_all_news(additional_query_params)

    return convert_to_news_story_object(stories)

def get_tweets_by_search(query, count=25):
    """
    Returns list of Tweet objects related to query
    """
    
    tweets = data_retriever.get_tweets_by_search(query, count=count)

    tweets_list = [models.Tweet(tweet['text'], tweet['user'], tweet['url'] if 'url' in tweet else None, tweet['created_at']) for tweet in tweets]

    return tweets_list

def get_twitter_trends(location_id = None):
    """
    Returns list of TwitterTrend objects
    """

    trends = None

    if location_id:
        trends = data_retriever.get_twitter_trends(location_id)
    else:
        trends = data_retriever.get_twitter_trends()

    twitter_trends_list = [models.TwitterTrend(trend['name'], trend['query'], trend['tweet_volume']) for trend in trends]
    
    return twitter_trends_list

def get_twitter_trends_and_related_information(include_tweets=False, include_news=False, location_id = None):
    """
    Returns list of TwitterTrend objects with options to supplement with related tweets and/or related news stories.
    To find related tweets and news stories, the query_term of a trend is used (defined in Twitter's API).
    """
    
    twitter_trends = get_twitter_trends(location_id)

    # related tweets
    if include_tweets:
        for trend in twitter_trends:
            tweets = get_tweets_by_search(trend.query_term, count=10)
            trend.set_related_tweets(tweets)
            trend.set_aggregated_tweet_sentiment()

    # related news stories
    if include_news:
        for trend in twitter_trends:
            news = get_top_news_stories(trend.query_term)
            trend.set_related_news_stories(news)
            trend.set_aggregated_news_sentiment()

    return twitter_trends

def get_top_news_stories_and_related_information(news_search_query=None, additional_news_params=None, country='us', include_tweets=False):
    """
    Returns list of NewsStory objets with options to:
    - search for a topic using news_search_query
    - search for any parameters accepted by NewsAPI's Top Stories endpoint using additional_news_params
    - supplement with related tweets (defines related as the url of the news story)
    """
    
    news_stories = get_top_news_stories(news_search_query, additional_news_params, country)

    if include_tweets:
        for story in news_stories:
            tweets = get_tweets_by_search(story.url)
            for tweet in tweets:
                story_url_location = tweet.content.find(story.url)
                if story_url_location != -1:
                    content = tweet.content.replace(story.url, '')
                    tweet.set_content_sentiment(content)

            story.set_related_tweets(tweets)
            story.set_aggregated_tweet_sentiment()

    return news_stories
