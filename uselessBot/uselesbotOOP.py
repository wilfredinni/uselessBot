import twitter
import datetime
import json
import praw
import re


class bot:

    json_file_to_open = None

    def __init__(self, subreddit_name, file_credentials, json_db):
        self.subreddit_name = subreddit_name
        self.file_credentials = file_credentials
        self.json_db = json_db
        # store the reddit and twitter credentials (try to make it one time)

    def __repr__(self):
        return "bot('{}', '{}', '{}')".format(
            self.subreddit_name, self.file_credentials, self.json_db)

    def load_credentials(self, credentials):
        self.twitter_credentials = twitter.Api(
            consumer_key=credentials['twitter']['consumer_key'],
            consumer_secret=credentials['twitter']['consumer_secret'],
            access_token_key=credentials['twitter']['access_token_key'],
            access_token_secret=credentials['twitter']['access_token_secret']
        )

        self.reddit_credentials = praw.Reddit(
            client_id=credentials['reddit']['client_id'],
            client_secret=credentials['reddit']['client_secret'],
            user_agent=credentials['reddit']['user_agent']
        )

    def load_json(self):
        with open(self.json_file_to_open, 'r') as f:
            return json.load(f)

    def write_json(self, key, value, post_db):
        post_db.update({key: value})
        with open(self.json_file_to_open, 'w') as f:
            json.dump(post_db, f)

    def post_twitter(self, msg):
        """
        Post on twitter.
        """
        self.twitter_credentials.PostUpdate(msg)

    @classmethod
    def set_json_file(cls, json_file):
        """
        Let me work with the class method instead of the instance.
        """
        cls.json_file_to_open = json_file


class search(bot):

    def __repr__(self):
        return "bot('{}', '{}', '{}')".format(
            self.subreddit_name, self.file_credentials, self.json_db)

    def search_reddit(self, saved_posts):
        """
        Search for newest 10 post on a subreddit
        """
        subreddit = self.reddit_credentials.subreddit(self.subreddit_name)

        for submission in subreddit.new(limit=10):
            if submission.title not in saved_posts.keys():
                yield submission.title, submission.url


class mentions(bot):

    def __repr__(self):
        return "bot('{}', '{}', '{}')".format(
            self.subreddit_name, self.file_credentials, self.json_db)

    def get_mentions(self, mentions_db):
        last_mention = str(self.twitter_credentials.GetMentions(count=1))
        # use regex to filter the twitter user and the post
        regex_user = re.compile(r"ScreenName=(.*?),")  # good screenName
        regex_metion = re.compile(r"Text='@UselesstBot (.*?)'")  # good mention

        # find the coincidences in the str
        filtered_user = regex_user.findall(last_mention)
        filtered_mention = regex_metion.findall(last_mention)

        return ''.join(filtered_user), ''.join(filtered_mention)

    def compare(self, text, user, mention_db):
        if text not in mention_db.keys():
            current = datetime.datetime.now()
            new_mention = {text: user}
            # overwrite post_db
            with open(self.json_file_to_open, 'w') as f:
                json.dump(new_mention, f)

            return '{} - changed by {} at: {}'.format(text, user, current)
        else:
            return False
