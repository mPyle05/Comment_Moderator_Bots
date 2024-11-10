import praw
from praw.exceptions import RedditAPIException
import time
import logging
logging.basicConfig(level = logging.DEBUG)

message = 'boo'
reddit = praw.Reddit(
    client_id='wG7NSQTDHsXtHjhNA8_Oew',
    client_secret='YhSRTfyvrDj4vAKNgy43qYMQ5qjfdg',
    user_agent="<console:Objective-Job1591:1.0>",
    username = 'Objective-Job1591',
    password = 'MakeUC002'
)

with open("bad_words.txt", "r") as file:
    # Strip quotes and split by commas, then strip whitespace around each word
    bad_words = [word.strip().strip('"') for word in file.read().split(",")]



subreddit = reddit.subreddit("MakeUCTest2")
for submission in subreddit.hot(limit=10):
    if submission.stickied == False:
        for comment in submission.comments:
            if hasattr(comment,"body"):

                comment_lower = comment.body.lower()
                for word in bad_words:
                    word_string = str(word.lower())
                    if word in comment_lower:   
                        print(comment_lower)
                        print('--------------')
                        try:
                            comment_id = comment.id 
                            comment = reddit.comment(id=comment_id)
                            comment.mod.remove()
                        except RedditAPIException as e:

                            print(f"an error occured: {e}")
                        time.sleep(10)
                        

           

           

'''

'''






