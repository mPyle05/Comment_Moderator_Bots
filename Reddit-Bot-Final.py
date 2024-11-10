---

# Reddit Hate Speech Detection Bot

This script uses the `praw` and `transformers` libraries to detect and moderate hate speech in Reddit comments. It leverages a pretrained hate speech model to automatically flag and remove offensive comments from posts in a specific subreddit.

## Features
- Authenticates with user-provided Reddit credentials.
- Checks recent posts in a specified subreddit.
- Uses a hate-speech classification model to flag inappropriate comments.
- Removes flagged comments to maintain a respectful discussion.

## Prerequisites
- **Python 3.6+**
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/latest/)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository-url.git
   cd your-project-folder
   ```

2. **Install required Python packages**:
   ```bash
   pip install praw transformers
   ```

## Usage

1. **Run the script**:
   ```bash
   python main.py
   ```

2. **When prompted, enter**:
   - Your **Reddit client_id**.
   - Your **Reddit secret key**.
   - Your **Reddit account username**.
   - Your **Reddit account password**.
   - The **name of the subreddit** you want to moderate.

3. **Bot Behavior**:
   - Logs in to your Reddit account.
   - Retrieves the latest posts from the specified subreddit.
   - Scans the comments for hate speech using the model.
   - Removes any comments identified as hate speech.
   - Pauses briefly to avoid rate-limiting.

## Code Walkthrough

### Imports and Model Setup

```python
import praw
from praw.exceptions import RedditAPIException
import time
import os
from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
pipe = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")
```

- **`praw`**: Interfaces with Reddit's API.
- **`pipeline`**: Loads the hate speech detection model from Hugging Face.

### Authentication and Subreddit Setup

```python
reddit = praw.Reddit(
    client_id='Enter client_id',
    client_secret='Enter secret key',
    user_agent="<console:Objective-Job1591:1.0>",
    username='Enter account username',
    password='Enter account password'
)

subreddit = reddit.subreddit("Enter the name of the subreddit you want to moderate")
```

- **Reddit credentials** are used for authentication.
- **Subreddit name** is provided to specify which subreddit the bot should monitor.

### Comment Retrieval and Hate Speech Detection

```python
for submission in subreddit.hot(limit=10):
    if submission.stickied == False:
        for comment in submission.comments:
            if hasattr(comment, "body"):
                comment_lower = comment.body.lower()
                result = pipe(comment_lower)
                label = result[0]['label']
                if label == 'hate':
                    print(comment_lower)
                    print('--------------')
```

- Retrieves the top 10 posts in the specified subreddit.
- Checks if the comment is stickied and retrieves the comment's text.
- **Hate speech detection** is performed on the comment.

### Flagging and Removing Comments

```python
                    try:
                        comment_id = comment.id 
                        comment = reddit.comment(id=comment_id)
                        comment.mod.remove()
                    except RedditAPIException as e:
                        print(f"an error occured: {e}")
                    time.sleep(10)
```

- Flagged comments are **removed** using Reddit's moderation features.
- Handles any exceptions with the **RedditAPIException**.
- **Sleep interval** of 10 seconds between actions to avoid rate-limiting.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---
