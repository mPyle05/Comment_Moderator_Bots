---
# Reddit Hate Speech Detection Bot

This script uses the `praw` and `transformers` libraries to detect and moderate hate speech in Reddit comments within a specified subreddit. It leverages a pretrained hate speech model to automatically flag and delete offensive comments from recent posts in the subreddit at a user-defined time interval.

## Features
- Authenticates with Reddit using user credentials and API keys.
- Periodically checks recent posts in a specified subreddit.
- Uses a hate-speech classification model to flag inappropriate comments.
- Deletes flagged comments to maintain a respectful subreddit.

## Prerequisites
- **Python 3.6+**
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/latest/)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/reddit-hate-speech-bot.git
   cd reddit-hate-speech-bot
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
   - Your **Reddit client_id**, **client_secret**, **user_agent**, **username**, and **password**.
   - The **subreddit name** you want to moderate.
   - **Time interval** (in seconds) for checking comments on recent posts.

3. **Bot Behavior**:
   - Logs in to your Reddit account.
   - Retrieves the top 10 recent submissions from the specified subreddit.
   - Scans the comments of these posts for hate speech.
   - Uses the hate speech model to flag and delete any identified hate speech comments.
   - Continues to check and moderate comments based on the provided time interval.

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
    username = 'Enter account username',
    password = 'Enter account password'
)

subreddit = reddit.subreddit("Enter the name of the subreddit you want to moderate")
```

- **Reddit credentials** (client ID, secret key, username, and password) are used for authentication.
- **Subreddit** is specified to monitor the comments.

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

- The last 10 **hot posts** from the specified subreddit are retrieved.
- **Comment detection** runs on each post's comments to find hate speech.

### Flagging and Deleting Comments

```python
                try:
                    comment_id = comment.id
                    comment = reddit.comment(id=comment_id)
                    comment.mod.remove()
                except RedditAPIException as e:
                    print(f"an error occurred: {e}")
                time.sleep(10)
```

- Each comment is classified, and any hate speech is flagged.
- **Deletes flagged comments** in the subreddit.
- Pauses for 10 seconds between actions to avoid rate limits.

## License
This project is licensed under the MIT License. See `LICENSE` for details.
---
