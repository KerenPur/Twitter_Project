
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = u'https://twitter.com/search?q='


def get_tweets(query: str, idle: int = 1, scrolls: int = 5):
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

    html_tweet = body.find_element_by_id('react-root')
    return html_tweet.text

def create_tweet_obj():
    pass



def main():
    raw_tweets = get_tweets(query=u'corona', idle=1, scrolls=5)



if __name__ == "__main__":
    main()