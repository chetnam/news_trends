"""
Provides models to represent and process accessed data.
Contains classes NewsStory, User (twitter), Tweet, TwitterTrend
"""

from . import utils

class NewsStory:

    def __init__(self, title, author, published_at, content, url, source=None):
        self.title = title
        self.author = author
        self.published_at = published_at
        self.content = content 

        # store upto 1000 first characters
        self.lead = content[0: min(1000, len(self.content))]
        self.url = url
        if source:
            self.source = source['name']

        self.set_content_sentiment(self.content)
        
    def set_related_tweets(self, tweets):
        self.related_tweets = tweets

    def set_aggregated_tweet_sentiment(self):
        if self.related_tweets:
            tweet_polarity_list = [tweet.polarity for tweet in self.related_tweets]
            self.mean_tweet_polarity = utils.mean(tweet_polarity_list)
            self.median_tweet_polarity = utils.median(tweet_polarity_list)
        else:
            # TODO: possibly set these to an unviable value to signify non-existence
            self.mean_tweet_polarity = 0
            self.median_tweet_polarity = 0

    def set_content_sentiment(self, content):
        
        self.polarity, self.subjectivity = utils.get_textual_sentiment_and_objectivity(content)

    def calculate_and_set_keywords(self):
        pass

    def serialize(self):
        """
        Create dict out of object, to enable easier jsonification
        """
        d = {'title': self.title, 'author': self.author, 'published_at': self.published_at, 'lead': self.lead, 'url': self.url, 'story_polarity': self.polarity, 'story_subjectivity': self.subjectivity}

        if hasattr(self, 'source'):
            d['source'] = self.source

        if hasattr(self, 'related_tweets'):
            d['related_tweets'] = [tweet.serialize() for tweet in self.related_tweets]
            d['mean_tweet_polarity'] = self.mean_tweet_polarity
            d['median_tweet_polarity'] = self.median_tweet_polarity
        
        return d

class User:
    def __init__(self, name, num_followers, is_verified):
        self.name = name
        self.num_followers = num_followers
        self.is_verified = is_verified
    
    def serialize(self):
        d = {'name': self.name, 'num_followers': self.num_followers, 'is_verified': self.is_verified}
        return d

class Tweet:
    def __init__(self, content, user, url, created_time, favorite_count=None):
        self.content = content
        self.user = User(user['name'], user['followers_count'], user['verified'])
        self.url = url
        self.created_at = created_time
        # self.favorite_count = favorite_count

        # this should only happen if Tweets don't have urls in them
        self.set_content_sentiment(self.content)

    def set_content_sentiment(self, content):
        self.polarity, self.subjectivity = utils.get_textual_sentiment_and_objectivity(content)

    def calculate_and_set_keywords(self):
        pass

    def serialize(self):
        """
        Create dict out of object, to enable easier jsonification
        """
        d = {'content': self.content, 'user': self.user.serialize(), 'url': self.url, 'created_at': self.created_at, 'polarity': self.polarity, 'subjectivity': self.subjectivity}
        return d
    
class TwitterTrend:

    def __init__(self, name, query_term, tweet_volume):
        self.name = name
        # query_term will be helpful in fetching tweets and news for this trend
        self.query_term = query_term
        self.tweet_volume = tweet_volume
        self.is_hashtag = True if name[0]=='#' else False

    def set_related_tweets(self, tweets):
        self.related_tweets = tweets

    def set_related_news_stories(self, news_stories):
        self.related_news_stories = news_stories

    def set_aggregated_tweet_sentiment(self):
        """
        Sets aggregated polarity of related tweets
        """
        if self.related_tweets:
            tweet_polarity_list = [tweet.polarity for tweet in self.related_tweets]
            self.mean_tweet_polarity = utils.mean(tweet_polarity_list)
            self.median_tweet_polarity = utils.median(tweet_polarity_list)
        else:
            # TODO: possibly set these to an unviable value to signify non-existence
            self.mean_tweet_polarity = 0
            self.median_tweet_polarity = 0

    def set_aggregated_news_sentiment(self):
        """
        Sets both polarity and subjectivity of related news stories
        """
        if self.related_news_stories:
            news_polarity_list = [story.polarity for story in self.related_news_stories]
            self.mean_news_polarity = utils.mean(news_polarity_list)
            self.median_news_polarity = utils.median(news_polarity_list)

            news_subjectivity_list = [story.subjectivity for story in self.related_news_stories]
            self.mean_news_subjectivity = utils.mean(news_subjectivity_list)
            self.median_news_subjectivity = utils.median(news_subjectivity_list)
        else:
            # TODO: possibly set these to an unviable value to signify non-existence
            self.mean_news_polarity = 0
            self.median_news_polarity = 0
            self.mean_news_subjectivity = 0
            self.median_news_subjectivity = 0


    def serialize(self):
        """
        Create dict out of object, to enable easier jsonification
        """
        d = {'name': self.name, 'tweet_volume': self.tweet_volume, 'query_term': self.query_term, 'is_hashtag': self.is_hashtag}

        if hasattr(self, 'related_tweets'):
            d['related_tweets'] = [tweet.serialize() for tweet in self.related_tweets]
            d['mean_tweet_polarity'] = self.mean_tweet_polarity
            d['median_tweet_polarity'] = self.median_tweet_polarity

        if hasattr(self, 'related_news_stories'):
            d['related_news_stories'] = [story.serialize() for story in self.related_news_stories]
            d['mean_news_polarity'] = self.mean_news_polarity
            d['median_news_polarity'] = self.median_news_polarity
            d['mean_news_subjectivity'] = self.mean_news_subjectivity
            d['median_news_subjectivity'] = self.median_news_subjectivity

        return d
