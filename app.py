from flask import Flask, request, jsonify,render_template
import pickle
import praw 
import urllib.parse
import json
#cleaning
import nltk 
import string 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import re
import os
app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))
#credentials to scrape
reddit = praw.Reddit(client_id='LkYS254yTjMAQA',
                     client_secret='##',
                     password='##',
                    user_agent='Build a flare detector.',
                    username='bhumika603')

def geturl(URL):
    #return home
    #extract - title, comments, body, URL from post
    ypost = reddit.submission(url=URL)
    topcomments=''
    ypost.comments.replace_more(limit=0) #we only want top comments
    for comment in ypost.comments:
        topcomments = topcomments + ' ' + comment.body
    ypost_title = ypost.title
    ypost_body = ypost.selftext
    ypost_url = ypost.url

    sub = ['jpg','png','reddit.com/comments']
    #function which cleans the URL and extracts important info 
    #stop_w = stopwords.words('english')
    def clean_url(url):
      #if it is an image or no URL which directs to another site
      if any(x in url for x in sub):
        pre = ""
        return pre
      address = url
      parsed = urllib.parse.urlsplit(address)
      pre = parsed.path.replace("-"," ")
      pre = pre.replace("/"," ")
      pre = pre.replace("_"," ")
      pre = ' '.join(word for word in pre.split() if word not in stop_w)
      return pre
    
    #clean the URL
    ypost_url = clean_url(ypost_url)
    #clean other things
    columns = [ypost_title, ypost_body,topcomments]
    def clean(column):
      #tokenize
      words = nltk.word_tokenize(column)
      new_words = []
      #remove punctuation
      for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '' :#and new_word not in stop_w:#remove stop words
            new_words.append(new_word)
      return new_words
      #lowercase text - already done in models
    
    for col in columns:
        clean(col)
    
    combined = ypost_title+topcomments+ypost_url+ypost_body #which is a string
    combined = [combined]
    return combined

@app.route('/')
def home():
    return render_template('./index.html')
@app.route('/predict', methods=['POST'])
def predict():
    home = request.form.get('home')
    #home = str(home)
    #return home
    #extract - title, comments, body, URL from post
    if (home.find('https://www.reddit.com/r/india/comments/')==-1): #check to make sure valid URL that is in Reddit India
      return 'Error! Please enter a valid URL within subreddit india'
    ypost = reddit.submission(url=home)
    topcomments=''
    ypost.comments.replace_more(limit=0) #we only want top comments
    for comment in ypost.comments:
        topcomments = topcomments + ' ' + comment.body
    ypost_title = ypost.title
    ypost_body = ypost.selftext
    ypost_url = ypost.url
    
    #clean it 
    #need a substring list  
    sub = ['jpg','png','reddit.com/comments']
    #function which cleans the URL and extracts important info 
    stop_w = stopwords.words('english')
    def clean_url(url):
      #if it is an image or no URL which directs to another site
      if any(x in url for x in sub):
        pre = ""
        return pre
      address = url
      parsed = urllib.parse.urlsplit(address)
      pre = parsed.path.replace("-"," ")
      pre = pre.replace("/"," ")
      pre = pre.replace("_"," ")
      pre = ' '.join(word for word in pre.split() if word not in stop_w)
      return pre
    #clean the URL
    ypost_url = clean_url(ypost_url)
    #clean other things
    columns = [ypost_title, ypost_body,topcomments]
    def clean(column):
      #tokenize
      words = nltk.word_tokenize(column)
      new_words = []
      #remove punctuation
      for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '': #and new_word not in stop_w:#remove stop words
            new_words.append(new_word)
      return new_words
      #lowercase text - already done in models
    for col in columns:
        clean(col)
    
    #apply model 
    combined = ypost_title+topcomments+ypost_url+ypost_body #which is a string
    combined = [combined] #turn to list
    
    prediction = model.predict(combined)
    #prediction = x[prediction[0]]
    #le = pickle.load(open('LabelEn.pkl','rb'))
    #x = list(le.inverse_transform(prediction))

    return render_template('./index.html',prediction_text = "The predicted flair is {}.".format(prediction[0]))

@app.route("/automated_testing",methods=['POST']) 
def automated_testing():
     if request.method == "POST":
        filee = request.files["upload_file"]
        urls = filee.read().decode("utf-8").split("\n")
        x = {}
        for link in urls:
            post = geturl(link)
            predicted_flair = model.predict(post)
            x[link] = predicted_flair #the link 
        return json.dumps(x)
if __name__ == "__main__":
    #app.run(debug=False)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
