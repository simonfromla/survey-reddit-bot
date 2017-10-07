#!/usr/bin/python3
import json
import os
import praw

"""
Scrapes posts for comments and saves the comment ID and comment text to the
accompanying JSON file.
"""

JSON_DEFAULT_LOC = os.environ.get('JSON_LOCATION') or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data.json")


def login():
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="Chrome:com.example.surveyor-"
                                                "bot:v1 (by /u/man-scout)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def load_manager(fp=None):
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "r") as file:
        data = json.load(file)
    return data


def scrape(reddit):
    data = load_manager()
    shortlinks = [data[sub][0]["shortlink"][-6:] for sub in data]

    for sl_id in shortlinks:
        submission = reddit.submission(id=sl_id)
        try:
            write_comments_to_file(submission, sl_id, data)
            print("Comments from '{}'' saved to file".format(submission.subreddit))
        except Exception as e:
            print("Could not write to file: {}".format(e))


def write_comments_to_file(submission, sl_id, data, fp=None):
    submission.comments.replace_more(limit=0)
    cmt_data = [{comment.id: comment.body}
                for comment in submission.comments.list()]
    for i in data:
        if sl_id in data[i][0]["shortlink"]:
            data[i][1]["responses"] = cmt_data
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "w") as fp:
        json.dump(data, fp)


def main():
    reddit = login()
    scrape(reddit)


if __name__ == "__main__":
    main()
