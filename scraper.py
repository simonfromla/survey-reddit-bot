import json
import praw


"""
2) open the json and read each url shortlink.
request the shortlink page
if response, scrape comment text, comment id, author
write to csv according to the url shortlink/subreddit
CHECKING for updates.
if new comment, add it. if same comment id but edited answer, add edit to csv.

[description]
"""
def deserialize():
    with open("data.json", "r") as f:
        data = json.load(f)
        print(data["postpreview"][0]["shortlink"])


def scrape():
    with open("data.json", "r") as f:
        data = json.load(f)
        # print(data["postpreview"][0]["shortlink"])

        submission = reddit.submission(url=data["postpreview"][0]["shortlink"])
        print(submission)


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
    scrape()


if __name__ == "__main__":
    main()
