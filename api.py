"""
This file contains get_user_info which extract user info via twitter api
"""

import json
import tweepy


def get_user_info(query, num_of_tweets=10):
    """
    This function extract user details from twitter api
    """
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"configuration config_file is missing, error: {e}")

    auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config["CONSUMER_SECRET"])
    auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = tweepy.Cursor(api.search, q=query, lang="en", tweet_mode='extended').items(num_of_tweets)
    # Store these tweets into a python list
    tweet_list = [tweet for tweet in tweets]

    # Since all the tweets are from the same user, we'll take the first tweet
    data = {'statuses': tweet_list[0].user.statuses_count, 'followers': tweet_list[0].user.followers_count,
            'location': tweet_list[0].user.location}

    return data


def main():
    data = get_user_info('Techrose11', 1)


if __name__ == "__main__":
    main()
