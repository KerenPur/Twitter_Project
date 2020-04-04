"""
Tweeter class, contains 5 fields
"""


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, replies, retweets, hashtags, likes, text):
        self.user = user
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags
        self.likes = likes
        self.text = text

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

    def __hash__(self):
        return hash((self.text, self.user, tuple(self.hashtags)))



