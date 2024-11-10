from instagrapi import Client
import re

with open("bad_words.txt", "r") as file:
    # Strip quotes and split by commas, then strip whitespace around each word
    bad_words = [word.strip().strip('"') for word in file.read().split(",")]

ipBan = int(input("1 for old, 2 for new: "))
cl = Client()

if ipBan == 1:
    cl.load_settings('dump.json')
    cl.login("elijahwhitesell25@gmail.com", "BallBall98!")
    userId = cl.user_id_from_username("ewhi.tesell")
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

        print(match)
        for word in bad_words:
            if word.lower() in extracted_text.lower():
                print(user + f" is bad. Found disliked word: '{word}'")
                print("PK: " + str(commentPK))
                badCommentIds.append(commentPK)

    print(badCommentIds)
    if cl.comment_bulk_delete(mediaId, badCommentIds):
        print("Deleted comments")
        badCommentIds.clear()
