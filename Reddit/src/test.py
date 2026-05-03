import praw
reddit = praw.Reddit(client_id="xxxxxxxxxxxxxxxxxxxxxxx", 
                                     client_secret="xxxxxxxxxxxxxxxxxxxxxxx",
                                     user_agent="xxxxxxxxxxxxxxxxxxxxxx",
                                     username="xxxxxxxxxxxxxxxxxxx",
                                     password="xxxxxxxxxxxxxxxxx"
                                     )

for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)
