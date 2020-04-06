"""
This file is responsible for creating the twitter_db
"""
from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
import json

PASSW = 'xxPm6rnp'

TABLES = {}

TABLES['tweets'] = ('''
CREATE TABLE tweets(
    id VARCHAR(255) PRIMARY KEY, 
    user_nickname VARCHAR(255) NOT NULL,
    num_replies INT,
    num_likes INT,
    num_retweets INT,
    text VARCHAR(255)
)''')

TABLES['hashtags'] = ("""
CREATE TABLE hashtags(
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    hashtag VARCHAR(255) UNIQUE NOT NULL
)""")

TABLES['tweets_hashtags'] = ("""
CREATE TABLE tweets_hashtags(
    id INTEGER PRIMARY KEY AUTO_INCREMENT, 
    hashtag_id INTEGER, 
    tweet_id VARCHAR(255),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags (id),
    FOREIGN KEY (tweet_id) REFERENCES tweets (id)
)""")

TABLES['usernames'] = ("""
CREATE TABLE usernames (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL
)""")

TABLES['searches'] = ("""
CREATE TABLE searches(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  search_string VARCHAR(255)
)""")

TABLES['username_searches'] = ("""
CREATE TABLE username_searches(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username_id INTEGER,
  search_id INTEGER,
  FOREIGN KEY (search_id) REFERENCES searches (id),
  FOREIGN KEY (username_id) REFERENCES usernames (id)
)""")

TABLES['tweets_username_searches'] = ("""
CREATE TABLE tweets_username_searches(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  tweet_id VARCHAR(255),
  username_search_id INTEGER,
  FOREIGN KEY (username_search_id) REFERENCES username_searches (id),
  FOREIGN KEY (tweet_id) REFERENCES tweets (id)
)""")

TABLES['searches_tweets'] = ("""
CREATE TABLE searches_tweets(
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  tweet_id VARCHAR(255),
  search_id INTEGER,
  FOREIGN KEY (search_id) REFERENCES searches (id),
  FOREIGN KEY (tweet_id) REFERENCES tweets (id)
)""")

QUERIES = {'add_tweet_index': '''CREATE UNIQUE INDEX idx_tweets_id ON tweets (id)''',
           'add_username_index ': '''CREATE UNIQUE INDEX idx_username ON usernames (username)''',
           'add_hashtags_index': '''CREATE UNIQUE INDEX idx_hashtags_id ON hashtags (hashtag)''',
           'add_searches_index': '''CREATE UNIQUE INDEX idx_searches_id ON searches (search_string)'''}


def create_connection(host_name, user_name, user_password):
    """
    creating connection to the database
    returning connector object
    """
    mydb = None
    try:
        mydb = mysql.connector.connect(host=host_name, user=user_name, passwd=user_password)
    except mysql.connector.Error as e:
        print("The error '{e}' occurred")
    return mydb


def create_database(cursor, db_name):
    """
    creating database
    """
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error:
        return


def execute_query(cursor, query):
    """
    executing query
    """
    try:
        cursor.execute(query)
        cursor.commit()
    except mysql.connector.Error:
        return


def main():
    """
    Establishes connection to mySQL, creates database
    """
    with open('config.json', 'r') as file:
        config = json.load(file)

    cnx = create_connection(config["HOST"], config["USER_NAME"], PASSW)
    cursor = cnx.cursor()
    # creating database
    try:
        cursor.execute("USE {}".format(config["DB_NAME"]))
    except mysql.connector.Error as err:
        if errorcode.ER_BAD_DB_ERROR == err.errno:
            create_database(cursor, config["DB_NAME"])
            cnx.database = config["DB_NAME"]

    # creating tables
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            cursor.execute(table_description)
        except mysql.connector.Error:
            continue

    # adding indexes for quick querying
    for query_name in QUERIES:
        query = QUERIES[query_name]
        try:
            cursor.execute(query)
        except mysql.connector.Error:
            continue

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
