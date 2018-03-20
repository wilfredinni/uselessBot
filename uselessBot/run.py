from uselesbotOOP import bot, mentions, search
import time
import hue

# styles
bg = hue.bg
blue = hue.blue
green = hue.green
yellow = hue.yellow


def run(subreddit):
    # create the instance
    useless_search = search(subreddit, 'credentials.json', 'posts_db.json')

    # set and load the json file that stores the credentials
    bot.set_json_file(useless_search.file_credentials)
    credentials = useless_search.load_json()
    useless_search.load_credentials(credentials)

    # set and load the json file that stores posts_db
    bot.set_json_file(useless_search.json_db)
    saved_posts = useless_search.load_json()

    # search 10 lasts posts on reddit
    new_posts = useless_search.search_reddit(saved_posts)
    for post in new_posts:
        # dump the new posts in posts_db
        useless_search.write_json(post[0], post[1], saved_posts)
        # post on twitter
        useless_search.post_twitter('{} {}'.format(post[0], post[1]))
        # -----------------------------------------------------------
        print(bg(green('New Post! {} - {}'.format(post[0], post[1]))))
        # -----------------------------------------------------------

    # --------------------------------------------
    print(bg(blue('Nothing new. Sleeping for 60 seconds.')))
    # --------------------------------------------
    time.sleep(15)
    change_subreddit(subreddit)


def change_subreddit(subreddit):
    # -----------------------------------
    print(bg(blue('Checking for new subreddit.')))
    # -----------------------------------
    get_mentions = mentions(subreddit, 'credentials.json', 'mention_db.json')

    # set and load the json file that stores the credentials
    bot.set_json_file(get_mentions.file_credentials)
    credentials = get_mentions.load_json()
    get_mentions.load_credentials(credentials)

    # get the last mention
    last_mention = get_mentions.get_mentions(get_mentions.json_db)
    # load the last mention file
    bot.set_json_file(get_mentions.json_db)
    mentions_json = get_mentions.load_json()

    # compare with db and post
    mention_post = get_mentions.compare(
        last_mention[1], last_mention[0], mentions_json)

    # if there is a new post
    if mention_post:
        get_mentions.post_twitter(mention_post)
        # ------------------------------------------------
        print(bg(yellow('@{} changed the subreddit to #{}'.format(
            last_mention[0], last_mention[1]))))
        # ------------------------------------------------
        run(last_mention[1])
    else:
        # ------------------------------------------------------------------
        print(bg(blue(
            'No new subreddit, searching again for {}'.format(subreddit))))
        # ------------------------------------------------------------------
        run(subreddit)


if __name__ == '__main__':
    run('learnpython')
