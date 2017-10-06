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

    # shortlinks = []
    shortlinks = [data[link][0]["shortlink"][-6:] for link in data]
    # print(shortlinks)

    # submission = reddit.submission(url=data["postpreview"][0]["shortlink"])
    for sl_id in shortlinks:
        submission = reddit.submission(id=sl_id)
        submission.comments.replace_more(limit=0)

        cmt_data = [{comment.id: comment.body} for comment in submission.comments.list()]
        # print(cmtd)
        # for r in data:
        #     if sl_id in data[r][0]["shortlink"]:
        #         data[r][0]["responses"] = cmtd
        for i in data:
            if sl_id in data[i][0]["shortlink"]:
                data[i][1]["responses"] = cmt_data

        # for key, value in data.items():
        #     for x in value:
        #         if sl_id in x['shortlink']:
        #             if not "responses":
        #                 x["responses"]= cmt_data
        #             else:
        #         # in case you overwrite the response with empty data
        #                 x['responses'] += cmt_data


    # print(data[r][0]["responses"] for r in data)
    print(data)
    # print(data)
    # for comment in submission.comments.list():
    #     print(comment.id, comment.body)
        # data["postpreview"][1]["responses"][comment.id] = comment.body

    # for comment in submission.comments.list():
    #     for i, d in data["postpreview"][1]["responses"][i]:
    #         d[comment.id] = comment.body
    # print(data)



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
