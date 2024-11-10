---

# Instagram Hate Speech Detection Bot

This script uses the `instagrapi` and `transformers` libraries to detect and moderate hate speech in Instagram comments periodically. It leverages a pretrained hate speech model to automatically flag and delete offensive comments from recent media posts at a user-defined time interval.

## Features
- Authenticates with user-provided Instagram credentials.
- Periodically checks for new comments on recent posts.
- Uses a hate-speech classification model to flag inappropriate comments.
- Deletes flagged comments to maintain a respectful comment section.

## Prerequisites
- **Python 3.6+**
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Instagrapi](https://github.com/adw0rd/instagrapi)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mPyle05/Hate-Speech-Detection-Bots.git
   cd instagram-hate-speech-bot
   ```

2. **Install required Python packages**:
   ```bash
   pip install instagrapi transformers
   ```

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **When prompted, enter**:
   - Your Instagram **username**.
   - Your Instagram **password**.
   - **Time interval** (in seconds) for checking comments on recent posts.
   - The number of posts to check

3. **Bot Behavior**:
   - Logs in to your Instagram account.
   - Retrieves the last specified number media posts and scans their comments.
   - Uses the hate speech model to flag and delete any identified hate speech comments.
   - Continues to check and moderate comments based on the provided time interval.

## Code Walkthrough

### Imports and Model Setup

```python
import time
from instagrapi import Client
import re
import os
from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
cl = Client()
```

- **`instagrapi`**: Interfaces with Instagram's API.
- **`pipeline`**: Loads the hate speech detection model from Hugging Face.

### Authentication and Interval Setup

```python
username = input("Please enter your username: ")
password = input("Please enter your password: ")
tick = int(input("Please enter the time between checks (in seconds): "))
numofPosts = int(input("How many posts to check?"))

cl.login(username, password)
userId = cl.user_id_from_username(username)

print("userId:" + userId)
```

- **User credentials** are collected and used for login.
- **Time interval** is specified by the user to set the delay between each scan.
- **Number of Posts** are specified by the user

### Comment Retrieval and Hate Speech Detection

```python
while True:
    userMedia = cl.user_medias(userId, numOfPosts)
    badCommentIds = []

    for i in userMedia:
        mediaId = re.search(r"id='(.*?)'", str(i)).group(1)
        print("Media id: " + mediaId)
        commentCount = re.search(r"comment_count='(.*?)'", str(i))

        comments = cl.media_comments(mediaId, commentCount)
```

- The last **numOfPosts** media posts are retrieved.
- **Comment detection** runs on each post to find hate speech comments.

### Flagging and Deleting Comments

```python
        for comment in comments:
            match = re.search(r"text='(.*?)'", str(comment))
            user = re.search(r"username='(.*?)'", str(comment))
            commentPK = re.search(r"pk='(.*?)'", str(comment))
            extracted_text = match.group(1)
            user = user.group(1)
            commentPK = int(commentPK.group(1))

            result = pipe(extracted_text)
            label = result[0]['label']

            if label == "hate":
                badCommentIds.append(commentPK)
                print("PK added to list: " + str(commentPK))

        if badCommentIds:
            if cl.comment_bulk_delete(mediaId, badCommentIds):
                print("Deleted comments")
                badCommentIds.clear()

    time.sleep(tick)
```

- Each comment is classified, and any hate speech is flagged.
- **Deletes flagged comments** in bulk for each media post.
- Pauses based on the user-defined interval.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---
