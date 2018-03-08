import json
import time
import praw
import twitter


def search(subreddit_name):
    """
    search for new posts on a subreddit and if they are not saved,
    save them and post on twitter. If it is already saved, wait 60
    seconds and search again.
    """
    subreddit = reddit.subreddit(subreddit_name)
    db = load('posts_db.json')

    for submission in subreddit.new(limit=10):
        if submission.title not in db.keys():
            write_db(submission.title, submission.url)

    print('Nothing new. Sleeping for 60 seconds.')
    time.sleep(60)
    search(subreddit_name)


def load(file):
    """
    Load the credentials from credentials.json for twitter
    and reddit, and the posts from posts_db.json.
    """
    with open(file, 'r') as credentials:
        return json.load(credentials)


def write_db(title, url, file='posts_db.json'):
    new_post = {title: url}  # new dict
    db = load(file)  # load the db
    db.update(new_post)  # add new entry
    with open(file, 'w') as f:  # save the entry
        json.dump(db, f)

    post(title, url)


def post(title, url):
    hashtags = ' #python #reddit #bot '
    twitter_api.PostUpdate(title + hashtags + url)
    print('New post! {}'.format(title))


# load the credentials from credentials.json
credentials = load('credentials.json')

# connect with reddit
reddit = praw.Reddit(
    client_id=credentials['reddit']['client_id'],
    client_secret=credentials['reddit']['client_secret'],
    user_agent=credentials['reddit']['user_agent']
)

# connect with twitter
twitter_api = twitter.Api(
    consumer_key=credentials['twitter']['consumer_key'],
    consumer_secret=credentials['twitter']['consumer_secret'],
    access_token_key=credentials['twitter']['access_token_key'],
    access_token_secret=credentials['twitter']['access_token_secret']
)

if __name__ == '__main__':
    search('learnpython')
