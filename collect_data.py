
import requests
from bs4 import BeautifulSoup
from tweet import Tweet

URL = u'https://twitter.com/UpdateCovid'


def get_tweets(idle: int = 1, scrolls: int = 5):
    """
    This function extract tweets from the given url and return the html content as text
    :param url: url path (should be twitter
    :param query: string to search hash tags on twitter
    :param idle: sleep time before collecting browser data
    :param scrolls: number of scrolls we wish to simulate
    :return:
    """

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.findAll('li', {"class": 'js-stream-item'})

    return tweets


def create_tweets_obj(tweets):
    """
    This function creates tweets dictionary out of tweets
    :param tweets: soup object of tweets
    :return: tweets dictionary
    """
    tweets_dict = {}
    for tweet in tweets:
        if tweet.find('p', {"class": 'tweet-text'}):
            tweet_user = tweet.find('span', {"class": 'username'}).text.strip()
            tweet_text = tweet.find('p', {"class": 'tweet-text'}).text.encode('utf8').strip()
            replies = tweet.find('span', {"class": "ProfileTweet-actionCount"}).text.strip()
            retweets = tweet.find('span', {"class": "ProfileTweet-action--retweet"}).text.strip()

            tweet_obj = Tweet(user=tweet_user, text=tweet_text, replies=replies, retweets=retweets)
            tweets_dict[tweet_user] = tweet_obj
        else:
            continue

    return tweets_dict


def main():
    soup_tweets = get_tweets(1,1)
    tweets_dict = create_tweets_obj(tweets=soup_tweets)



if __name__ == "__main__":
    main()
