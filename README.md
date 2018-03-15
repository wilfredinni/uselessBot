# uselessBot

A useless robot, full of bugs, that goes where you want.

## How it works

just tweet `@UselessBot` with a `subreddit`. The bot will post the last 10 entries on twitter and start searching for new ones every 2 minutes until someone changes the subreddit... so useless =(

    @UselessBot gifs

You can see it working at [@UselesstBot](https://twitter.com/UselesstBot) and running thanks to [pythonanywhere.com](https://www.pythonanywhere.com).

## Usage

- Fill the credential.json with your API keys for Reddit and Twitter.
- Open or Import retwibot.py and use `search('subreddit')`:

    ```python
    search('learnpython')
    ```
Console Output:

![alt text](https://serving.photos.photobox.com/550350036c86424aafe74c1e015965d236fb2948d1f94658ff7595c55c4022ca6359ce0b.jpg)


## TODO

- Change all the `print()` for logs.
- Review the code.
- Unittest.
