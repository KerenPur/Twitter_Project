"""
Tweeter class, contains 5 fields
"""
import hashlib


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, replies, retweets, hashtags, likes, text, statuses, followers, location):
        self.user = user
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags
        self.likes = likes
        self.text = text
        self.statuses = statuses
        self.followers = followers
        self.location = location

    def __str__(self):
        string = """Tweet Info:
        user: {}
        replies: {}
        Retweets: {}
        hashtags: {}
        likes: {}
        text: {}
        """.format(self.user, self.replies, self.retweets, self.hashtags, self.likes, self.text)
        return string

    @property
    def hash(self):
        return hashlib.sha1((self.text + self.user).encode()).hexdigest()



