"""
Houses shared connections
"""

import tweepy
from tweepy import OAuthHandler

from . import settings
env_vars = settings.env_vars

class Connections:
    
    def __init__(self):
        self.twitter_api_conn = None
        self.set_twitter_api_connection()

    def set_twitter_api_connection(self, consumer_key = env_vars['TWITTER_CONSUMER_KEY'], 
                    consumer_secret = env_vars['TWITTER_CONSUMER_SECRET'], 
                    access_token = env_vars['TWITTER_ACCESS_TOKEN'], 
                    access_secret = env_vars['TWITTER_ACCESS_SECRET']):
        
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
    
        self.twitter_api_conn = tweepy.API(auth)

    def get_twitter_api_connection(self):

        # TODO: use this function to catch connection 
        # aborted/stopped errors and reconnects
        if not self.twitter_api_conn:
            self.set_twitter_api_connection()
        return self.twitter_api_conn
        
