import os
basedir = os.path.abspath(os.path.dirname(__file__))

from . import settings

class Config(object):
    # set defaults to true for testing
    DEBUG = True
    TESTING = True
    
    ENV_VARS = settings.env_vars

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    pass