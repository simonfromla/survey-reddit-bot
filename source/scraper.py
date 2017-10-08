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
    """ Create a reddit instance according to praw.ini configuration.
    Call reddit.user.me() as a check.
    Return reddit instance.
    """
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="Chrome:com.example.surveyor-"
                                                "bot:v1 (by /u/man-scout)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def load_manager(fp=None):
    """ Load the accompanying JSON data which holds reddit post information.
    """
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "r") as file:
        data = json.load(file)
    return data


def scrape(reddit):
    """ For each post specified in the JSON dict, scrape the comments within
    the post and write the comments to the JSON dict to the key: "responses".
    """
    data = load_manager()
    shortlinks = [data[sub][0]["shortlink"][-6:] for sub in data]

    for sl_id in shortlinks:
        submission = reddit.submission(id=sl_id)
        try:
            write_comments_to_file(submission, sl_id, data)
            print("Comments from '{}'' "
                  "saved to file".format(submission.subreddit))
        except Exception as e:
            print("Could not write to file: {}".format(e))


def write_comments_to_file(submission, sl_id, data, fp=None):
    """ Takes a reddit submission object, shortlink ID, and JSON data.
    Retrieves the comments per submission, and for each submission within the
    JSON data, also write its comments.
    """
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
