# About the Project

The **Hate Speech Detection Bot** was developed by our team to tackle **online harassment** and **discrimination** on social media platforms, particularly Instagram and Reddit. By leveraging the power of AI, this bot automatically detects and removes hate speech from Instagram comments, and subReddits,  creating a safer and more inclusive space for users. This project inludes a Comment-moderating bot for both **Reddit** and **Instagram**, expanding our efforts to combat harmful content across multiple platforms.

## Inspiration

The inspiration behind this project came from the increasing prevalence of **hate speech** and **cyberbullying** on social media platforms. As platforms like Instagram have grown, it has become more challenging for moderators to effectively manage harmful content.  

Our goal was to create a tool that could **empower users** and **community moderators** to protect their online spaces from abusive content without the need for constant manual oversight. The vision was to use technology to fight back against hate speech and **discrimination**, promoting safer interactions online.

## What it does

[The Instagram Hate Speech Detection Bot:](./README_InstagramBot.md)
- **Logs into Instagram** and retrieves a user’s most recent posts and associated comments.
- **Scans the comments** using a pre-trained natural language processing (NLP) model to detect **hate speech**.
- **Deletes harmful comments** flagged by the AI model to ensure the post remains respectful and inclusive.
- Works **automatically**, saving moderators and users time while keeping their online spaces free of harmful content.

By automating the detection and removal of hate speech, the bot helps users maintain control over their online environments and promotes a healthier, more positive community.

## How we built it

This project was built by our team using the following technologies:
- **Python** as the main programming language.
- **instagrapi** library to interact with Instagram’s API, retrieve posts and comments, and delete comments.
- **Hugging Face’s transformers** for natural language processing, specifically the **facebook/roberta-hate-speech-dynabench-r4-target** model, which classifies text as either **safe** or **hate speech**.
  
### Development Process:
1. **Login and Authentication**: We used the instagrapi library to authenticate the bot using Instagram credentials and retrieve the necessary data (user media and comments).
2. **Content Scanning**: After fetching recent comments, we passed the text to the pre-trained AI model to classify the comments into categories such as "safe" or "hate".
3. **Comment Deletion**: If the AI flagged a comment as hate speech, the bot would automatically remove it using the API, ensuring a swift response to harmful content.
4. **Automation**: The bot runs in an infinite loop, periodically checking for new comments and cleaning them up without human intervention.

## Challenges we ran into

Building and deploying the bot came with several challenges:
- **API Restrictions**: Instagram’s API has limitations on data access and comment removal, which required us to work within these boundaries while still achieving the bot's goals.
- **Scalability**: With high volumes of posts and comments on Instagram, we had to design a solution that could handle large amounts of data without slowing down or missing harmful content.
- **False Positives and Model Tuning**: We encountered issues with the model occasionally flagging non-hateful content as harmful. Fine-tuning the model to improve its accuracy in detecting hate speech without mistakenly flagging innocent comments was an ongoing process.
- **Real-Time Moderation**: Ensuring that the bot operated quickly and effectively, especially as new comments were posted, was a challenge that required optimizing the bot’s performance.

## Accomplishments that we're proud of

- **Real-Time Hate Speech Moderation**: We are proud of developing a bot that can effectively detect and remove hate speech in real time, preventing harmful comments from being seen by other users.
- **Cross-Platform Moderation**: The ability to extend our Reddit bot’s concept to Instagram was a key achievement, allowing us to apply the solution to different social media platforms.
- **AI Integration**: Successfully integrating a pre-trained **RoBERTa model** for hate speech detection and fine-tuning it to work for Instagram comments was a major accomplishment.
- **Collaboration and Teamwork**: The bot was developed through close collaboration among team members with various areas of expertise, from data science and machine learning to software development and user interface design.

## What we learned

- **Scalability is Key**: Developing solutions that can scale effectively to handle large amounts of data is essential, especially when dealing with social media platforms that generate millions of posts and comments daily.
- **Ethical AI Implementation**: We learned a great deal about how AI can be used for **social good**, and the importance of continually refining models to ensure they do not inadvertently censor content or misinterpret context.
- **User-Centered Design**: We understood the importance of designing technology that is **accessible and beneficial** for users—creating tools that directly address real-world problems, like online harassment, in a way that is intuitive and helpful.

## What's Next

Moving forward, our team plans to:
- **Expand to Other Platforms**: We aim to adapt the bot for additional social media platforms, such as **Twitter** and **Facebook**, to help tackle hate speech and discrimination in more online communities.
- **Model Improvement**: We will continue to improve the AI model, addressing any limitations or biases and ensuring it can accurately detect harmful content across diverse languages and contexts.
- **Enhanced Features**: We are exploring adding more customizable features, such as personalized filtering for specific types of hate speech or integrating sentiment analysis to detect subtle forms of discrimination.

Ultimately, we hope to continue evolving the bot into a more robust, scalable tool that can make a meaningful impact on combating online hate speech and fostering **inclusive, respectful communities**.
