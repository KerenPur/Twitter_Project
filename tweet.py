"""
Tweeter class, contains 5 fields
"""


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, replies, retweets, hashtags, likes):
        self.user = user
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags
        self.likes = likes

    def __str__(self):
        string = """Tweet Info:
        user: {}
        replies: {}
        Retweets: {}
        hashtags: {}
        likes: {}
        """.format(self.user, self.replies, self.retweets, self.hashtags, self.likes)
        return string



