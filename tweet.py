"""
Tweeter class, contains 5 fields
"""
import hashlib


class Tweet:
    """
    initializing new tweet
    """

    def __init__(self, user, replies, retweets, hashtags, likes, text, statuses, followers, location,user_id):
        self.user = user
        self.replies = replies
        self.retweets = retweets
        self.hashtags = hashtags
        self.likes = likes
        self.text = text
        self.statuses = statuses
        self.followers = followers
        self.location = location
        self.user_id=user_id

    def __str__(self):
        string = f"""Tweet Info:
        user: {self.user_id}
        nickname: {self.user}
        replies: {self.replies}
        Retweets: {self.retweets}
        hashtags: {self.hashtags}
        likes: {self.likes}
        text: {self.text}
        statuses: {self.statuses}
        followers: {self.followers}
        location: {self.location}
        """
        return string

    @property
    def hash(self):
        return hashlib.sha1((self.text + self.user).encode()).hexdigest()



