---

# Instagram Hate Speech Detection and Comment Moderation

This script leverages Python libraries `instagrapi` and `transformers` to detect and moderate hate speech comments on an Instagram account. It uses a pretrained hate speech model to identify and remove harmful content from comments on recent media posts.

## Features
- Authenticates to Instagram using user credentials.
- Retrieves the latest media posts and associated comments.
- Uses a hate-speech classification model to flag inappropriate comments.
- Deletes comments identified as hate speech from the user's posts.

## Prerequisites
- Python 3.6+
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Instagrapi](https://github.com/adw0rd/instagrapi)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/instagram-hate-speech-moderation.git
   cd instagram-hate-speech-moderation
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

2. **Select an Instagram account**:
   - Enter `1` for the first account or `2` for the second account based on preference.

3. The script will:
   - Log into the specified Instagram account.
   - Retrieve the most recent 5 posts from the account.
   - Detect hate speech in comments and delete any flagged comments.

## Code Walkthrough

### Imports and Model Setup
```python
from instagrapi import Client
import re
import os
from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
```

- **`instagrapi`**: Enables Instagram API functions.
- **`pipeline`**: Loads the hate speech model.

### Instagram Client and Login
```python
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

print("userId:" + userId)
```

- **`load_settings`** and **`login`**: Authenticates the Instagram account.
- **`user_id_from_username`**: Retrieves the user ID.

### Retrieving Media and Comments
```python
userMedia = cl.user_medias(userId, 5)
mediaId = ""
badCommentIds = []
```

Retrieves the last 5 posts by `userId`.

### Hate Speech Detection and Comment Deletion
```python
for i in userMedia:
    mediaId = re.search(r"id='(.*?)'", str(i)).group(1)
    print("Media id: " + mediaId)
    comments = cl.media_comments(mediaId)

    for comment in comments:
        match = re.search(r"text='(.*?)'", str(comment))
        commentPK = int(re.search(r"pk='(.*?)'", str(comment)).group(1))

        # Classify comment text
        result = pipe(match.group(1))
        label = result[0]['label']

        if label == "hate":
            badCommentIds.append(commentPK)
            print("Flagged comment for deletion:", commentPK)

    if badCommentIds:
        if cl.comment_bulk_delete(mediaId, badCommentIds):
            print("Deleted flagged comments")
            badCommentIds.clear()
```

- Uses the **hate speech model** to classify each comment.
- Flagged comments are **deleted in bulk** for each post.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

--- 
