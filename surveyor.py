import config
import os
import praw
import time

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


def submit_post(reddit, title, body_file):
    print("reading body_file..")
    with open(body_file, "r") as f:
        body = f.read()
    sr = config.SUBS
    for s in sr:
        body = body.replace("%%SUBREDDIT%%", s)
        # body = body.replace("%%TOPIC%%", topic
        subreddit = reddit.subreddit(s)
        print("submitting post...")
        subreddit.submit(title, selftext=body, send_replies=True)
        print("post submitted")
        # sleep for ten minutes
        # scrape for comments


def scrape_response():
    pass

def run(reddit):
    body_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), "post-body.txt")
    submit_post(reddit, config.TITLE, body_location)



    # print("Obtaining {} comments".format(config.number_of_comments))
    # for comment in reddit.subreddit('test').comments(limit=config.number_of_comments):
    #     if "test" in comment.body:
    #         print("'Test' found in comment: {}".format(comment.id))
    #         comment.reply(AUTO_REPLY_MESSAGE)
    #         print("Replied to comment: {}".format(comment.id))

    #         print("Sleeping for 10 seconds")
    #         time.sleep(10)


def main():
    reddit = login()

    run(reddit)

if __name__ == "__main__":
    main()
