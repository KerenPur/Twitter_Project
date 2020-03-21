import csv
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tweet import Tweet

URL ='http://twitter.com/search?q='


def get_tweets(query: str, idle: int = 3, scrolls: int = 5):
    """
    This function extract tweets from the given url and return the html content as text
    :param url: url path (should be twitter
    :param query: string to search hash tags on twitter
    :param idle: sleep time before collecting browser data
    :param scrolls: number of scrolls we wish to simulate
    :return:
    """
    browser = webdriver.Chrome()
    browser.get(URL + query)
    time.sleep(idle)
    body = browser.find_element_by_tag_name('body')
    for _ in range(scrolls):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    tweets = soup.find_all("div", attrs={"data-testid": "tweet"})

    return tweets


def create_tweets_obj(tweets):
    """
    This function creates tweets dictionary out of tweets
    :param tweets: soup object of tweets
    :return: tweets dictionary
    """
    tweets_dict = {}
    replies_regex = re.compile("([0-9]+) [(replies)(reply)]")
    retweets_regex = re.compile(".* ([0-9]+) [(Retweets)(Retweet)]")
    likes_regex = re.compile(".* ([0-9]+) [(likes)(like)]")
    hashtag_regex = re.compile("/hashtag/([^\s]+)\?src=hashtag_click")
    username_regex = re.compile("/([^\s/]+)/?")
    print("Found {} tweets".format(len(tweets)))
    for idx, tweet in enumerate(tweets):
        labels = [item for item in tweet.find_all("div", {"role": "group"}) if "aria-label" in item.attrs]
        replies = 0
        retweets = 0
        likes = 0
        if len(labels) == 1:
            label = labels[0]["aria-label"]
            if replies_regex.match(label):
                replies = int(replies_regex.match(label).group(1))

            if retweets_regex.match(label):
                retweets = int(retweets_regex.match(label).group(1))

            if likes_regex.match(label):
                likes = int(likes_regex.match(label).group(1))

        hashtags = [hashtag_regex.match(item["href"]).group(1)
                    for item in tweet.find_all("a") if "href" in item.attrs and hashtag_regex.match(item["href"])]
        tweet_user = [item['href']
                      for item in tweet.find_all("a", {"aria-haspopup": 'false', "role": "link"})
                      if "href" in item.attrs][0]
        tweet_user = username_regex.match(tweet_user).group(1)
        tweet_obj = Tweet(user=tweet_user, replies=replies, retweets=retweets, hashtags=hashtags, likes=likes)
        tweets_dict[tweet_user] = tweet_obj

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
    soup_tweets = get_tweets("corona")
    tweets_dict = create_tweets_obj(tweets=soup_tweets)

    for tweet in tweets_dict:
        print(tweets_dict[tweet])

    save_to_csv('tweet.csv', tweets_dict)


if __name__ == "__main__":
    main()
