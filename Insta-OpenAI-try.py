from instagrapi import Client
import re
import os
from openai import OpenAI
client = OpenAI(
     api_key=os.environ.get("OPENAI_API_KEY")
)



ipBan = int(input("1 for old, 2 for new: "))
cl = Client()

if ipBan == 1:
    #cl.load_settings('dump.json')
    cl.login("elijahwhitesell25@gmail.com", "BallBall98!")
    userId = cl.user_id_from_username("ewhi.tesell")
    #cl.dump_settings('dump.json')
else:
    cl.load_settings('dump2.json')
    cl.login("elijahwhitesel26@gmail.com", "BallBall98!")
    userId = cl.user_id_from_username("ewhi.t.esell")
    #cl.dump_settings('dump2.json')

print("userId:" + userId)

userMedia = cl.user_medias(userId, 5)

mediaId = ""
commentCount = 0
badCommentIds = []

for i in userMedia:
    print(i)
    mediaId = re.search(r"id='(.*?)'", str(i))
    mediaId = mediaId.group(1)
    print(" From USER profile" + mediaId)
    commentCount = re.search(r"comment_count='(.*?)'", str(i))

    comments = cl.media_comments(mediaId, commentCount)

    for comment in comments:
        print(comment)

        match = re.search(r"text='(.*?)'", str(comment))
        user = re.search(r"username='(.*?)'", str(comment))
        commentPK = re.search(r"pk='(.*?)'", str(comment))
        extracted_text = match.group(1)
        user = user.group(1)
        commentPK = int(commentPK.group(1))


        def detect_hate_speech(text):

            response = client.moderations.create(
                input=text
            )

            return response["results"][0]["flagged"]

        if __name__ == "__ai_try2__":
            text_to_check = extracted_text
            is_hate_speech = detect_hate_speech(text_to_check)

            if is_hate_speech:
                print("The text contains hate speech.")
                badCommentIds.append(commentPK)
            else:
                print("The text does not contain hate speech.")




    print(badCommentIds)
    if badCommentIds:
        if cl.comment_bulk_delete(mediaId, badCommentIds):
            print("Deleted comments")
            badCommentIds.clear()
        




'''       
moderation = client.moderations.create(input=extracted_text)

        if moderation:
            print('This contains hate speech')
            badCommentIds.append(commentPK)

        else:
            print("The text does not contain hate speech.")
'''