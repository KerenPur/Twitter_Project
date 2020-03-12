import csv
import re
import requests
from bs4 import BeautifulSoup
from tweet import Tweet

URL = 'https://twitter.com/UpdateCovid'


def get_tweets():
    """
    This function extract tweets from the given url and return the html content as text
    :return:
    """
    response = ""
    try:
        response = requests.get(URL)
    except requests.ConnectionError as e:
        print("Url failure, {}".format(e))
        exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')
    tweets = soup.findAll('li', {"class": 'js-stream-item'})

    return tweets


def get_hashtag(tweet_text):
    """
    This function gets all the hashtags for a text in tweet
    :param tweet_text: tweet text
    :return: list of hashtags
    """
    hashtags = []
    tweet_text_str = str(tweet_text)
    pattern = re.compile(r'\#([a-zA-Z\.\_\-0-9]+)')
    matches = pattern.finditer(tweet_text_str)
    for match in matches:
        print(match.group(1))
        hashtags.append(match.group(1))
    return hashtags


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

            tweet_obj = Tweet(user=tweet_user, text=tweet_text, replies=replies, retweets=retweets,
                              hashtags=get_hashtag(tweet_text))
            tweets_dict[tweet_user] = tweet_obj
        else:
            continue

    return tweets_dict


def save_to_csv(filepath, tweets_dict):
    """
    This function saves the tweets dict to csv file
    :param tweets_dict: tweets dictionary
    :return: None
    """
    try:
        with open(filepath, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            header = ['User', 'Content', 'Replies', 'Retweets', 'Hashtags' '\n']
            wr.writerow(header)
            for key in tweets_dict:
                wr.writerow(
                    [tweets_dict[key].user, tweets_dict[key].text, tweets_dict[key].replies, tweets_dict[key].retweets,
                     tweets_dict[key].hashtags, '\n'])
    except FileExistsError:
        print('File Already exists')
        exit(1)


def main():
    soup_tweets = get_tweets()
    tweets_dict = create_tweets_obj(tweets=soup_tweets)

    for tweet in tweets_dict:
        print(tweets_dict[tweet])

    save_to_csv('tweet.csv', tweets_dict)


if __name__ == "__main__":
    main()
