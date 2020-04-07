"""
This file is responsible for storing values in the twitter_db
"""
from __future__ import print_function
import mysql.connector
import json

PASSW = 'xxPm6rnp'

with open('config.json', 'r') as file:
    config = json.load(file)

add_hashtags = ("INSERT INTO hashtags "
                "(hashtag)"
                "VALUES (%s)"
                "ON DUPLICATE KEY UPDATE hashtag= %s")
add_tweet = ("INSERT INTO tweets "
             "(id,user_nickname, num_replies, num_likes, num_retweets,text) "
             "VALUES (%s,%s, %s, %s, %s,%s)"
             "ON DUPLICATE KEY UPDATE num_replies= %s, num_likes=%s, num_retweets=%s")
add_tweet_hashtags = ("INSERT INTO tweets_hashtags"
                      "(hashtag_id,tweet_id)"
                      "VALUES (%s, %s)")
add_search = ("INSERT INTO searches"
              "(search_string)"
              "VALUES (%s)"
              "ON DUPLICATE KEY UPDATE search_string= %s")
add_search_tweets = ("INSERT INTO searches_tweets"
                     "(tweet_id,search_id)"
                     "VALUES (%s,%s)")
add_username = ("INSERT INTO usernames"
                "(username)"
                "VALUES (%s)"
                "ON DUPLICATE KEY UPDATE username= %s")
add_username_searches = ("INSERT INTO username_searches"
                         "(username_id,search_id)"
                         "VALUES (%s,%s)")
add_tweets_username_searches = ("INSERT INTO tweets_username_searches"
                                "(tweet_id,username_search_id)"
                                "VALUES (%s,%s)")


def test_db():
    """
    testing database by printing tweets table
    """
    cnx = mysql.connector.connect(host=config["HOST"], user=config["USER_NAME"], passwd=PASSW,
                                  database=config["DB_NAME"])
    # creating database_cursor to perform SQL operation
    db_cursor = cnx.cursor()
    db_cursor.execute("SELECT * FROM tweets")
    result = db_cursor.fetchall()
    for row in result:
        print(row)


def store_tweets_dict(tweets_dict, search, user):
    """
    storing values in databse
    """
    cnx = mysql.connector.connect(host=config["HOST"], user=config["USER_NAME"], passwd=PASSW,
                                  database=config["DB_NAME"])
    cursor = cnx.cursor(buffered=True)
    cursor.execute(add_username, [user, user])
    cursor.execute("SELECT id FROM usernames WHERE username= %s", [user])
    username_id = cursor.fetchall()[0][0]
    cursor.execute(add_search, [search, search])
    cursor.execute("SELECT id FROM searches WHERE search_string= %s", [search])
    search_id = cursor.fetchall()[0][0]
    cursor.execute(add_username_searches, [username_id, search_id])
    username_search_ind = cursor.lastrowid
    for tweet in tweets_dict:
        tweet_txt = tweets_dict[tweet].text[:100] + (tweets_dict[tweet].text[100:] and '..')
        cursor.execute(add_tweet, [tweets_dict[tweet].hash, tweets_dict[tweet].user, tweets_dict[tweet].replies,
                                   tweets_dict[tweet].likes, tweets_dict[tweet].retweets, tweet_txt,
                                   tweets_dict[tweet].replies, tweets_dict[tweet].likes, tweets_dict[tweet].retweets])
        cursor.execute("SELECT id FROM tweets WHERE id= %s", [tweets_dict[tweet].hash])
        tweet_id = cursor.fetchall()[0][0]
        cursor.execute(add_search_tweets, [tweet_id, search_id])
        cursor.execute(add_tweets_username_searches, [tweet_id, username_search_ind])
        for hashtag in tweets_dict[tweet].hashtags:
            cursor.execute(add_hashtags, [hashtag, hashtag])
            cnx.commit()
            cursor.execute("SELECT id FROM hashtags WHERE hashtag= %s", [hashtag])
            hashtag_ind = cursor.fetchall()[0][0]
            cursor.execute(add_tweet_hashtags, [hashtag_ind, tweet_id])
            print("Hashtag {} from {} added successfully.".format(hashtag, tweets_dict[tweet].user))

    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()


def drop_database():
    """
    deleting database
    """
    conn = mysql.connector.connect(host=config["HOST"], user=config["USER_NAME"], passwd=PASSW)
    cursor = conn.cursor()
    sql = "DROP DATABASE " + config["DB_NAME"]
    cursor.execute(sql)
