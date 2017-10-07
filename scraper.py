#!/usr/bin/python3
import json
import praw


"""
if new comment, add it. if same comment id but edited answer, add edit to csv.
"""

def login():
    print("Authenticating")
    reddit = praw.Reddit("surveyor", user_agent="Chrome:com.example.surveyor-bot:v1 (by /u/man-scout)")
    print("Authenticated as {}".format(reddit.user.me()))
    return reddit


def deserialize():
    with open("data.json", "r") as f:
        data = json.load(f)
        print(data["postpreview"][0]["shortlink"])


def scrape(reddit):
    with open("data.json", "r") as f:
        data = json.load(f)

        shortlinks = [data[link][0]["shortlink"][-6:] for link in data]

        for sl_id in shortlinks:
            submission = reddit.submission(id=sl_id)
            submission.comments.replace_more(limit=0)

            cmt_data = [{comment.id: comment.body} for comment in submission.comments.list()]

            for i in data:
                if sl_id in data[i][0]["shortlink"]:
                    data[i][1]["responses"] = cmt_data


    with open("data.json", "w") as fp:
        json.dump(data, fp)

    print(data)


# def scrape_response():
#     print("Obtaining {} comments".format(config.number_of_comments))
#     for comment in reddit.subreddit('test').comments(limit=config.number_of_comments):
#         if "test" in comment.body:
#             print("'Test' found in comment: {}".format(comment.id))
#             comment.reply(AUTO_REPLY_MESSAGE)
#             print("Replied to comment: {}".format(comment.id))

#             print("Sleeping for 10 seconds")
#             time.sleep(10)


def main():
    reddit = login()

    scrape(reddit)

if __name__ == "__main__":
    main()
