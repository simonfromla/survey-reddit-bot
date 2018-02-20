# survey-reddit-bot

Automate post creation for a specified list of sub-reddits.
SRB will post for you just outside reddit's ten minute rate-limit while you do other things.
Then scrape responses to the posts and save them to a JSON dictionary for later viewing.

### Usage
1) Install the requirements
2) Head over to [reddit preferences](https://www.reddit.com/prefs/apps/) scroll all the way to the bottom, register/create a new application.
3) Edit __configs/config.py__ with the title of your posts, as well as the list of sub-reddits to post to.
4) Edit __configs/post-body.txt__ with the body of your post.
5) Edit __source/praw.ini__ with the details of your new app.
6) In __source/surveyor.py__, change `appname` in the `login()` function to match your app's name.
7) Run __source/surveyor.py__ to generate the posts to the list of sub-reddits.

__source/scraper.py__ can be run anytime after a post has been created to scrape the post for its responses. Consider running this file with crontab for automated scraping.


##### File overview
- __configs/config.py__ holds the post's title information, as well as the list of sub-reddits to post to.
- __configs/post-body.txt__ should be edited with your post's body text. Markdown format accepted. Variables marked by double parentheses, "%%TOPIC%%", can be edited and manipulated as you see fit in surveyor.py.
- __data.json__ is a JSON file initialized with an empty dictionary, `{}` to hold the scraped information. This is where the post information as well as comments to the post will be saved.
- __source/praw.ini__ holds reddit app related information.
- __source/surveyor.py__ is a script that auto-posts according to the specified configurations.
- __source/scraper.py__ is a script that looks for the posts posted using __surveyor.py__, scrapes the responses within the posts and saves them to __data.json__.

