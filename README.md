# Reddit Flair Detector
Prediction of the official flairs of the given Reddit post from the India subreddit. (https://www.reddit.com/r/india/)
# WEBSITE
Runs on: https://reddit-flair-detector-bhumika.herokuapp.com/
# Part I - Reddit Data Collection 
I have used PRAW (Python Reddit API Wrapper) to scrape data.
Initially, I decided that I would scrape by hot, new and top posts. I soon realised that the distribution of posts was very unequal, with very little data being collected from flairs such as food (was only able to collect 10) and mostly from political and non-political flairs.

I then tried to scrape a max of 1000 posts per flair, but only managed to get approximately 200-250 posts from each flair. This ensured that my distribution of posts was similar so that all categories of flairs were being trained in the model. On deciding what data to collect, I first explored the posts (score was irrelevant) and decided to collect:

1. Title
2. Body 
3. Top comments (in PRAW it is a commentforest, so did not collect any of the sub comments for any comment)
4. URL
5. ID 
6. Flair (label)

# Part II - Exploratory Data Analysis (EDA)
1. I checked to make sure that all posts collected were unique, by their ID and deleted if any duplicates.
2. Checking for NULL values 
    - Realised that 40% of data collected had nothing in the Body
    - Noted that in the future I might not use 'body' as a feature, might worsen the results due to inconsistency 
3. Started with one feature: 'Title' 
    - Decided to make a vocabulary set from it to check the top 30 words. 
    - Realised that the top words were mostly part of Stop Words or punctuation 
    - This justified my reasoning and I then decided I would remove stop words and punctuation as it would have adverse effect on my model
    - Re-checked the top words
3. For the Title, Body, and Top Comments:
    - Removed stopwords
    - Removed punctuation
    - Considered lemmatization (but model was performing worse later on)
    - Lowercase (done already in Tokenizer)
4. Cleaning the URL 
    - First tried finding substrings like 'reddit.com/comments/' which would tell me URL was just the permalink or '.jpg' etc for image
    - Realised it wouldn't work -> used urllib.parse instead
    - The important information could be extracted from the path, so did that and applied cleaning techinques as before
    
  
  
  

