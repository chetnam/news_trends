**Summary**
This project contains a Flask API that exposes news and twitter data to enable simple analysis and visualization of parallel or diverging trends/topics in news and social media.

This API exposes three endpoints:
* /trends: Returns top trends on Twitter. Options to (through query parameters) add related tweets and news stories.
* /topNews: Returns top news from NewsAPI. Options to (through query parameters) add related tweets and add any parameters NewsAPI's top headlines endpoint accepts. Includes sentiment measures on the content of the news stories and the content of the tweets (if tweets included).
* /tweets: Returns tweets related to a specific search query (through query parameter 'q'). Options to choose number of tweets returned. Includes sentiment measures on the content of the tweets.

***

**Other Details**

* To get the raw data, this project uses [NewsAPI](https://newsapi.org/), [Twitter's API](https://developer.twitter.com/en/docs), and [tweepy](https://www.tweepy.org/).
* To add sentiment, this project uses [textblob](https://textblob.readthedocs.io/en/dev/).
* The API currently throws a 500 for any exception, including when the client-entered search query returns no results. This will be changed at some point in the future.
* To set this up locally, a NewsAPI api key and credentials for Twitter's API are needed and should be included in a '.env' file (see [python-dotenv](https://pypi.org/project/python-dotenv/) for more details).
* In this project, 'requirements.txt' is analogous to a 'package-lock.json' file in an npm project. 'requirements-to-freeze.txt' is analogous to a 'package.json' file. Packages that you use explicitly should be added to 'requirements-to-freeze.txt' and all packages your project uses (such as dependencies of the packages you add explicitly) should be in 'requirements.txt'. 'pip install -r requirements-to-freeze.txt' and 'pip freeze > requirements.txt' serve almost the same purpose as 'npm i' would in an npm project. Make sure to be working in a clean virtualenv to exclude unnecessary packages. Idea boorowed from [here](https://www.kennethreitz.org/essays/a-better-pip-workflow).

