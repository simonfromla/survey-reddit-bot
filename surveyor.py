#! /usr/bin/python3
import config
import json
import os
import praw
import time

"""
Auto-generate posts to a given list of sub-reddits at ten minute intervals.

Configure the post's title, and choose the subreddits in 'config.py', and edit
the post's body information with markdown inside 'post-body.txt'.
"""

JSON_DEFAULT_LOC = os.environ.get('JSON_LOCATION') or os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "data.json")


def login():
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="Chrome:com.example.surveyor-"
                                                "bot:v1 (by /u/man-scout)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def load_post_body():
    with open("post-body.txt") as file:
        body = file.read()
    return body


def submit_post(reddit, fp=None):
    title = config.TITLE
    sr = config.SUBS
    print("Reading body file...")
    body = load_post_body()

    data = {}
    for index, s in enumerate(sr, 1 - len(sr)):
        body = body.replace("%%SUBREDDIT%%", s)
        # body = body.replace("%%TOPIC%%", topic)
        subreddit = reddit.subreddit(s)
        print("submitting a new post to /r/{}".format(s))
        submission = subreddit.submit(title, selftext=body, send_replies=True)
        print("post submitted to /r/{}".format(s))

        # data["/r/" + s] = [{"shortlink": submission.shortlink},
        #                    {"responses": []}]


        if fp is None:
            fp = JSON_DEFAULT_LOC
        with open(fp, "r") as file:
            data = json.load(file)
        data["/r/" + s] = [{"shortlink": submission.shortlink},
                           {"responses": []}]
        with open(fp, "w") as file:
            json.dump(data, file, ensure_ascii=False)
            print("Data written to file")



        # try:
        #     write_to_file(data)
        #     print("Data written to file")
        # except Exception as e:
        #     print("Could not write to file: {}".format(e))
        if index:
            print("Sleeping 10 minutes before posting...")
            time.sleep(600)


def write_to_file(data, fp=None):
    if fp is None:
        fp = JSON_DEFAULT_LOC

    with open(fp, "r") as file:
        json.load(data)
    with open(fp, "w") as file:
        json.dump(data, file, ensure_ascii=False)


def main():
    reddit = login()
    submit_post(reddit)


if __name__ == "__main__":
    main()
