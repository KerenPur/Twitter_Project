"""
Tweeter class, contains 5 fields
"""


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, text, replies, retweets, hashtags):
        self.user = user
        self.text = text
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags

    def __str__(self):
        string = """Tweet Info:
        user: {}
        text: {}
        replies: {}
        Retweets: {}
        hashtags: {}
        """.format(self.user, self.text, self.replies, self.retweets, self.hashtags)
        return string



