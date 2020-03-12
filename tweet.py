"""
Tweeter class, contains 4 fields
"""


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, text, replies, retweets):
        self.user = user
        self.text = text
        self.replies = replies
        self.retweets = retweets

    def print_tweet(self):
        string = """
        Tweet Info:\n
        user: {}\n
        text: {}\n
        replies: {}\n
        Retweets: {}\n
        """.format(self.user, self.text, self.replies, self.retweets)
        return string

    def __str__(self):
        string = """
        Tweet Info:\n
        user: {}\n
        text: {}\n
        replies: {}\n
        Retweets: {}\n
        """.format(self.user, self.text, self.replies, self.retweets)
        return string

    def __repr__(self):
        string = """
        Tweet Info:
        user: {}
        text: {}
        replies: {}
        Retweets: {}
        """.format(self.user, self.text, self.replies, self.retweets)
        return string

