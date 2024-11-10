import time

from instagrapi import Client
import re
import os
from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
cl = Client()

username = input("PLease enter your username: ")
password = input("Please enter your password: ")
tick = int(input("Please enter the time between checks (in seconds): "))

cl.login(username, password)
userId = cl.user_id_from_username(username)

print("userId:" + userId)

while True:

    userMedia = cl.user_medias(userId, 5)
    mediaId = ""
    commentCount = 0
    badCommentIds = []

    for i in userMedia:
    #print(i)
        mediaId = re.search(r"id='(.*?)'", str(i))
        mediaId = mediaId.group(1)
        print("Media id: " + mediaId)
        commentCount = re.search(r"comment_count='(.*?)'", str(i))

        comments = cl.media_comments(mediaId, commentCount)

        for comment in comments:
            #print(comment)

            match = re.search(r"text='(.*?)'", str(comment))
            user = re.search(r"username='(.*?)'", str(comment))
            commentPK = re.search(r"pk='(.*?)'", str(comment))
            extracted_text = match.group(1)
            user = user.group(1)
            commentPK = int(commentPK.group(1))

            #print(match)

            result = pipe(extracted_text)

            # Directly access the label and score from the result
            label = result[0]['label']
            #print(label)

            if label == "hate":
                badCommentIds.append(commentPK)
                print("PK added to list: " + str(commentPK))

        print(badCommentIds)
        if badCommentIds:
            if cl.comment_bulk_delete(mediaId, badCommentIds):
                print("Deleted comments")
                badCommentIds.clear()

    time.sleep(tick)
