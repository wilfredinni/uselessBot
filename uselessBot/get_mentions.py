import hue
import uselessbot
import json
import re

# styles
bg = hue.bg
blue = hue.blue
green = hue.green
yellow = hue.yellow


def main(subreddit):
    """
    Get the 5 last mentions temporary mentions
    """
    credentials = uselessbot.load_credentials('twitter')  # load credentials
    mentions_db = uselessbot.load_json('mention_db.json')  # load mentions db

    # get the last 1 mention (change count to search for more mentions)
    mentions = str(credentials.GetMentions(count=1))

    # use regex to filter the twitter user and the post
    regex_user = re.compile(r"ScreenName=(.*?),")  # good screenName
    regex_metion = re.compile(r"Text='@UselesstBot (.*?)'")  # good mention

    # find the coincidences in the str
    filtered_user = regex_user.findall(mentions)
    filtered_mention = regex_metion.findall(mentions)

    # print(mentions)

    # ---------------------- log ----------------------
    print(bg(blue('Checking for new subreddit.')))
    # ---------------------- log ----------------------

    # only check the last mention
    try:
        if filtered_mention[0] not in mentions_db.keys():
            mention = {filtered_mention[0]: filtered_user[0]}
            # overwritte post_db.json
            with open('mention_db.json', 'w') as f:
                json.dump(mention, f)
            # format the twitter user
            twitter_user = '@{}'.format(filtered_user[0])

            # post the changed subreddit
            uselessbot.new_post(filtered_mention[0], twitter_user, False)
            # search the new subreddit for new posts
            uselessbot.main(filtered_mention[0])
        else:
            # ---------------------- log ----------------------
            print(bg(blue(
                'No new subreddit, searching again for {}'.format(subreddit))))
            # ---------------------- log ----------------------

            # if no new subreddit, continue search
            uselessbot.main(subreddit)
    except Exception:
        print(uselessbot.wrong())
        uselessbot.main('learnpython')


if __name__ == '__main__':
    main('learnpython')
