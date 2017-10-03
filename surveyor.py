import config
import praw
import time

AUTO_REPLY_MESSAGE = ("A reply to your 'test'.")

"""Takes an input of subs from the user, title, and post-body and auto generates
posts at 8 minute intervals. Input information taken from config.py.
[description]

check for a positive number of responses and scrape the site for comments.
Save comment ID
"""

def login():
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="asdf")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def run(reddit):
    print("Obtaining {} comments".format(config.number_of_comments))
    for comment in reddit.subreddit('test').comments(limit=config.number_of_comments):
        if "test" in comment.body:
            print("'Test' found in comment: {}".format(comment.id))
            comment.reply(AUTO_REPLY_MESSAGE)
            print("Replied to comment: {}".format(comment.id))

            print("Sleeping for 10 seconds")
            time.sleep(10)


def main():
    reddit = login()
    while True:
        run(reddit)


if __name__ == "__main__":
    main()
