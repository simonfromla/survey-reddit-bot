#!/usr/bin/python3
import json
import os
import praw
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from copy import deepcopy
from configs import config

"""
Auto-generate posts to a given list of sub-reddits at ten minute intervals.

Configure the post's title, and choose the subreddits in 'config.py', and edit
the post's body information with markdown inside 'post-body.txt'.
"""

JSON_DEFAULT_LOC = os.environ.get('JSON_LOCATION') or os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "survey_response.json")


def login():
    """ Create a reddit instance according to praw.ini configuration.
    Call reddit.user.me() as a check.
    Return reddit instance.
    """
    print("Authenticating")
    reddit = praw.Reddit("appname", user_agent="Chrome:com.example.bot-"
                                                "name:v1 (by /u/)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def load_post_body():
    """ Load the accompanying post-body.txt to be used as the post's body text.
    Return the markdown formatted text.
    """
    with open("../configs/post-body.txt") as file:
        body = file.read()
    return body


def edit_post_body(post_body, sub):
    """ If any additional edits to the post's body is made here, it must
    work in conjunction with the `for` loop in the `submit_post` function.
    """
    post_body.replace("%%SUBREDDIT%%", sub)
    # post_body.replace("%%TOPIC%%", topic)
    return post_body


def update_response(old_response, submission, sub):
    """ Takes a submission object and the name of the sub-reddit and creates an
    entry into the JSON dictionary of {"subreddit": [{"submission shortlink"},
                                                     {"responses":[]}].
    "responses" is initialized to hold comments, used by scraper.py.
    """
    new_response = deepcopy(old_response)
    new_response["/r/" + sub] = [{"shortlink": submission.shortlink},
                                 {"responses": []}]
    return new_response


def load_survey_responses(fp=None):
    """ Load the current survey response file as a JSON object.
    """
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "r") as file:
        survey_results = json.load(file)
    return survey_results


def prepare_survey_update(submission, sub):
    survey_response = load_survey_responses()
    update = update_response(survey_response, submission, sub)
    return update


def write_to_file(update, fp=None):
    if fp is None:
        fp = JSON_DEFAULT_LOC
    with open(fp, "w") as file:
        json.dump(update, file, ensure_ascii=False)
        print("Post submission data written to file")


def submit_post(reddit, fp=None):
    """ Retrieve the post's title, the list of sub-reddits to post to, and
    the body text of the post.
    Using the reddit instance, submit the post to each of the designated
    sub-reddits.
    Write the newly created submission object to a JSON dictionary.
    Sleeps after each submission but the last.
    """
    post_title = config.TITLE
    sub_list = config.SUBS
    print("Reading body file...")
    try:
        body = load_post_body()
    except OSError as e:
        print("Could not read file: {}".format(e))

    for index, sub in enumerate(sub_list, 1 - len(sub_list)):
        body = edit_post_body(body, sub)
        subreddit = reddit.subreddit(sub)

        print("Submitting a new post to /r/{}".format(sub))
        submission = subreddit.submit(post_title,
                                      selftext=body, send_replies=True)
        print("Post submitted to /r/{}".format(sub))

        update = prepare_survey_update(submission, sub)

        try:
            write_to_file(update)
        except OSError as e:
            print("Could not write to file: {}".format(e))

        if index:
            print("Sleeping 600s before next post...")
            time.sleep(600)


def main():
    reddit = login()
    submit_post(reddit)


if __name__ == "__main__":
    main()
