"""
This file contains get_user_info which extract user info via twitter api
"""

import json
import tweepy


def get_user_info(user_id, api):
    """
    This function extract user details from twitter api
    """

    user = api.get_user(user_id)

    data = {'statuses': user.statuses_count, 'followers': user.followers_count,
            'location': user.location}

    return data


def connect_to_api():
    """
    This function establish the connection to twitter api and returns an api object
    """
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"configuration config_file is missing, error: {e}")

    auth = tweepy.OAuthHandler(config['CONSUMER_KEY'], config["CONSUMER_SECRET"])
    auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def main():
    data = get_user_info('Techrose11', 1)


if __name__ == "__main__":
    main()
