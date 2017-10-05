#! /usr/bin/python3
import config
import json
import os
import praw
import time

"""

1) Takes an input of subs from the user, title, and post-body and auto generates
posts at 10 minute intervals. Input information taken from config.py.
Take url shortlink and save it and subreddit to CSV.
(also write to CSV: the survey question)


"""

def login():
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="Chrome:com.example.surveyor-bot:v1 (by /u/man-scout)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def submit_post(reddit, title, body_file):
    print("reading body_file..")
    with open(body_file, "r") as f:
        body = f.read()
    sr = config.SUBS
    data = {}
    for index, s in enumerate(sr, 1 - len(sr)):
        body = body.replace("%%SUBREDDIT%%", s)
        # body = body.replace("%%TOPIC%%", topic
        subreddit = reddit.subreddit(s)
        print("submitting a new post to /r/{}".format(s))
        url = subreddit.submit(title, selftext=body, send_replies=True)
        print("post submitted to /r/{}".format(s))
        data["/r/" + s] = [{"shortlink": url.shortlink}, {"responses": []}]
        with open("data.json", "w") as file:
            json.dump(data, file, ensure_ascii=False)
            print("Data written to file")
        if index:
            print("sleeping 10 minutes...")
            time.sleep(600)


        # Scraper.py should be able to work in isolation, with a dynamic csv--meaning, as the csv updates with new shortlinks, scraper should work without conflict.


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
