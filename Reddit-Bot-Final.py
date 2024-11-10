import praw
from praw.exceptions import RedditAPIException
import time
import os
from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

reddit = praw.Reddit(
    client_id='Enter client_id',
    client_secret='Enter secret key',
    user_agent="<console:Objective-Job1591:1.0>",
    username = 'Enter account username',
    password = 'Enter account password'
)


subreddit = reddit.subreddit("Enter the name of the subreddit you want to moderate")
for submission in subreddit.hot(limit=10):
    if submission.stickied == False:
        for comment in submission.comments:
            if hasattr(comment,"body"):

                comment_lower = comment.body.lower()
                result = pipe(comment_lower)
                label = result[0]['label']
                if label == 'hate':
                    print(comment_lower)
                    print('--------------')
                    try:
                        comment_id = comment.id 
                        comment = reddit.comment(id=comment_id)
                        comment.mod.remove()
                    except RedditAPIException as e:

                        print(f"an error occured: {e}")
                    time.sleep(10)
           
