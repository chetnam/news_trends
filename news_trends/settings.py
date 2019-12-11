# loads variables set in .env file
import os
from dotenv import load_dotenv
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'), verbose=True)

env_vars = {}
env_vars['NEWS_API_KEY'] = os.getenv("NEWS_API_KEY")
env_vars['TWITTER_CONSUMER_KEY'] = os.getenv("TWITTER_CONSUMER_KEY")
env_vars['TWITTER_CONSUMER_SECRET'] = os.getenv("TWITTER_CONSUMER_SECRET")
env_vars['TWITTER_ACCESS_TOKEN'] = os.getenv("TWITTER_ACCESS_TOKEN")
env_vars['TWITTER_ACCESS_SECRET'] = os.getenv("TWITTER_ACCESS_SECRET")
