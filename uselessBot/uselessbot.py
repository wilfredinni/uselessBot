import hue
import json
import time
import praw
import twitter
import datetime
import get_mentions

# style
bg = hue.bg
blue = hue.blue
green = hue.green
yellow = hue.yellow
red = hue.red


def search(subreddit_name):
    """
    search for new posts on a subreddit and if they are not saved,
    save them and post on twitter. If it is already saved, wait 60
    seconds then search again.
    """
    # load the credentials for reddit and twitter
    reddit = load_credentials('reddit')
    subreddit = reddit.subreddit(subreddit_name)
    saved_posts = load_json('posts_db.json')  # load the posts bd

    # search for the last 10 submissions in reddit
    try:
        for submission in subreddit.new(limit=10):
            # check if the title is in the bd and write it
            if submission.title not in saved_posts.keys():
                write_db(submission.title, submission.url)
        # ---------------------- log ----------------------
        print(bg(blue('Nothing new. Sleeping for 60 seconds.')))
        # ---------------------- log ----------------------
    except Exception:
        print(wrong())
        search('learnpython')

    # Execute when there are no new posts:
    time.sleep(60)  # sleep for 1 minute
    get_mentions.main(subreddit_name)


def load_json(file):
    """
    Load .json files
    """
    with open(file, 'r') as f:
        return json.load(f)


def write_db(key, value, file='posts_db.json', post=True):
    """
    wtrite the info in .json files
    """
    db = load_json(file)  # load the db
    db.update({key: value})  # add new entry
    with open(file, 'w') as f:  # save the entry
        json.dump(db, f)

    # if post=True, post it on twitter
    if post:
        new_post(key, value)


def new_post(title, url, post=True):
    """
    post on twitter
    """
    twitter = load_credentials('twitter')  # load twitter credetials

    if post:
        try:
            twitter.PostUpdate(title + ' ' + url)  # post it
        except Exception:
            print(wrong())
            search('learnpython')

        # ---------------------- log ----------------------
        print(bg(green('New post! {}'.format(title))))
        # ---------------------- log ----------------------

    else:
        time = datetime.datetime.now()
        # post the updated subreddit
        try:
            # url = user - title = subreddit
            twitter.PostUpdate(
                '{} - changed by {} at: {}'.format(title, url, time))
            # '{}: {} changed the subreddit to #{}'.format(time, url, title))
        except Exception:
            print(wrong())
            search('learnpython')

        # ---------------------- log ----------------------
        print(bg(yellow('{} changed the subreddit to #{}'.format(url, title))))
        # ---------------------- log ----------------------


def load_credentials(credential):
    """
    function that loads the keys for twitter or reddit
    """
    secret_keys = load_json('credentials.json')

    if credential == 'reddit':
        return praw.Reddit(
            client_id=secret_keys['reddit']['client_id'],
            client_secret=secret_keys['reddit']['client_secret'],
            user_agent=secret_keys['reddit']['user_agent']
        )
    else:
        return twitter.Api(
            consumer_key=secret_keys['twitter']['consumer_key'],
            consumer_secret=secret_keys['twitter']['consumer_secret'],
            access_token_key=secret_keys['twitter']['access_token_key'],
            access_token_secret=secret_keys['twitter']['access_token_secret']
        )


def wrong():
    return bg(red('Something went wrong. Returning to learnpython'))


if __name__ == '__main__':
    search('learnpython')
