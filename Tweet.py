"""
Tweeter class, contains 6-8 fields
"""


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, name, nickname, time, content, num_retweets, num_love, video_len=None, video_views=None):
        self.name = name
        self.nickname = nickname
        self.time = time
        self.content = content
        self.num_retweets = num_retweets
        self.num_love = num_love
        self.video_len = video_len
        self.video_views = video_views
