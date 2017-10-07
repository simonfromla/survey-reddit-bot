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
    post_title = config.TITLE
    sub_list = config.SUBS
    print("Reading body file...")
    body = load_post_body()

    for index, sub in enumerate(sub_list, 1 - len(sub_list)):
        body = body.replace("%%SUBREDDIT%%", sub)
        # body = body.replace("%%TOPIC%%", topic)
        subreddit = reddit.subreddit(sub)
        print("Submitting a new post to /r/{}".format(sub))
        submission = subreddit.submit(post_title,
                                      selftext=body, send_replies=True)
        print("Post submitted to /r/{}".format(sub))
        try:
            write_to_file(submission, sub)
        except Exception as e:
            print("Could not write to file: {}".format(e))

        if index:
            print("Sleeping 10 minutes before posting...")
            time.sleep(600)


def write_to_file(submission, sub, fp=None):
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "r") as file:
        data = json.load(file)
    data["/r/" + sub] = [{"shortlink": submission.shortlink},
                         {"responses": []}]
    with open(fp, "w") as file:
        json.dump(data, file, ensure_ascii=False)
        print("Data written to file")


def main():
    reddit = login()
    submit_post(reddit)


if __name__ == "__main__":
    main()
