# -*- coding: utf-8 -*-
"""ML Models & Evaluation 2.0

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hyRyV4s-ysi2cJiWZ6mU5tcOgfVLdZcT
"""

#importing necessary packages 

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix as cm
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn import svm
#evaluation of model
from sklearn.model_selection import cross_val_score
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import classification_report

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# categorical labels 
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing
import pickle

from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded['finalcleanedflaredata.csv']))
df.head()

#categorical labels to numeric values 
le = LabelEncoder()
df['Flair'] = le.fit_transform(df['Flair'])
list(le.classes_)

output = open('LabelEn.pkl','wb')
pickle.dump(le,output)
output.close()
from google.colab import files
files.download('LabelEn.pkl')

"""1. LOGISTIC REGRESSION"""

def logreg(X,Y):
  X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=0)
  logreg = Pipeline([('vect', CountVectorizer(stop_words='english')),
                ('tfidf', TfidfTransformer()),
            ('clf', LogisticRegression(penalty='l2')),
            ])
  ans = logreg.fit(X_train, y_train)
  y_pred = logreg.predict(X_test)
  print('Test accuracy is :'+ str(accuracy_score(y_test, y_pred)))
  #plot a confusion matrix to check FP,FN,TP,TN  - EVALUATING MODEL
  disp = plot_confusion_matrix(ans, X_test, y_test,
                                 display_labels=le.inverse_transform(df["Flair"].unique()),
                                 cmap=plt.cm.Blues)
  #print the classification report - F1 score, recall, precision
  print(classification_report(y_test, y_pred))
  #testdata = LabelEncoder().fit_transform(y_pred[0:15])
  #print(y_test[0:15])
  print(list(le.inverse_transform(y_pred[0:1])))
  print(list(le.inverse_transform(y_test[0:1])))

#using Title as feature only
logreg(df['Title'],df['Flair'])

#using Title + Commments - just comments gives 46%
df["T+C"] = df["Title"]+df["Comments"]
logreg(df["T+C"],df['Flair'])   #almost negligible improvement

#title + comments + cleaned URL
logreg(df["T+C"]+df['CleanedURL'],df['Flair'])

#title + comments + cleaned URL + body
logreg(df["Title"]+df["Comments"]+df['CleanedURL']+df["Body"],df['Flair'])

"""UNDERSTANDING OUR CONFUSION MATRIX:
- diagonal represents no of correctly classified points
- as we increase the no of features, we can see that the darkness of the blue increases in the diagonal which shows that more test data is being classified correctly
- goal is to minimise (in theory: diagonals should be all 0 so that means no mis-classification)
- we can see that significant mis-classification occurs in Policy/Economy and Business/Finance (8) which is understandable as there is correlation between the two topics

CLASSIFICATION REPORT:
- class 0 (Ask INdia) and 6 (Business/Finance) have lowest precision
- this means TP/(TP+FP) is the lowest. (Correctly Classified divided by Correctly Classified + Wrongly Classified as Belonging to group)
- this shows that these 2 groups are the ones that cause the confusion
"""

# find accuracy using cross-validation (check for overfitting)
def logisticreg(X,Y):
  X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=0)
  
  vectorizer = CountVectorizer(stop_words='english')
  
  Xtrain_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)
  
  tfidf = TfidfTransformer()
  
  Xtrain_vectors = tfidf.fit_transform(Xtrain_vectors)
  test_vectors = tfidf.transform(test_vectors)

  feature = vectorizer.fit_transform(X)
  label = Y
  
  #clf = LogisticRegression(C=1, penalty='l1', solver='liblinear')
  clf = LogisticRegression(C=1, penalty='l2',max_iter=700)
  clf.fit(Xtrain_vectors,y_train)

  accuracies = cross_val_score(clf,feature, label, scoring='accuracy', cv=5) 
  print(accuracies)
  print("Max accuracy on 10 fold is "+str(accuracies.max()))
  print("Min accuracy on 10 fold is "+str(accuracies.min()))
  print("Mean accuracy on 10 fold is "+str(accuracies.mean()))

#using Title as feature only
logisticreg(df['Title'],df['Flair'])

#Title + Comments cross validation
logisticreg(df["T+C"],df['Flair'])   #We can see that the mean accuracy has improved

#title + comments + cleaned URL
logisticreg(df["T+C"]+df['CleanedURL'],df['Flair'])  #Test accuracy is 70% and cross valid mean accuracy is 75% (with L1 regularization)
#applying L2 applies a harsher loss and less overfitting

#title + comments + cleaned URL + body
logisticreg(df["T+C"]+df['CleanedURL']+df["Body"],df['Flair'])   #mean is 86% while test accuracy was 77% - overfitting - fixed by using L2 instead of L1

"""Conclusion: Title + Comments + Cleaned URL + body work best//
Now Evaluation of model
"""

# find accuracy using cross-validation (check for overfitting)
def naivebayes(X,Y):
  X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=0)
  
  vectorizer = CountVectorizer(stop_words='english')
  
  Xtrain_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)
  
  tfidf = TfidfTransformer()
  
  Xtrain_vectors = tfidf.fit_transform(Xtrain_vectors)
  test_vectors = tfidf.transform(test_vectors)

  feature = vectorizer.fit_transform(X)
  label = Y
  
  #clf = LogisticRegression(C=1, penalty='l1', solver='liblinear')
  clf = MultinomialNB()
  clf.fit(Xtrain_vectors,y_train)

  accuracies = cross_val_score(clf,feature, label, scoring='accuracy', cv=10) 
  print(accuracies)
  print("Max accuracy on 10 fold is "+str(accuracies.max()))
  print("Min accuracy on 10 fold is "+str(accuracies.min()))
  print("Mean accuracy on 10 fold is "+str(accuracies.mean()))

#using Title as feature only
naivebayes(df["T+C"]+df['CleanedURL']+df["Body"],df['Flair'])

# find accuracy using cross-validation (check for overfitting)
def SVM(X,Y):
  X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=0)
  
  vectorizer = CountVectorizer(stop_words='english')
  
  Xtrain_vectors = vectorizer.fit_transform(X_train)
  test_vectors = vectorizer.transform(X_test)
  
  tfidf = TfidfTransformer()
  
  Xtrain_vectors = tfidf.fit_transform(Xtrain_vectors)
  test_vectors = tfidf.transform(test_vectors)

  feature = vectorizer.fit_transform(X)
  label = Y
  
  #clf = LogisticRegression(C=1, penalty='l1', solver='liblinear')
  clf = svm.SVC()
  clf.fit(Xtrain_vectors,y_train)

  accuracies = cross_val_score(clf,feature, label, scoring='accuracy', cv=10) 
  print(accuracies)
  print("Max accuracy on 10 fold is "+str(accuracies.max()))
  print("Min accuracy on 10 fold is "+str(accuracies.min()))
  print("Mean accuracy on 10 fold is "+str(accuracies.mean()))

#using Title as feature only
SVM(df["Title"]+df["Comments"]+df["Body"]+df['CleanedURL'],df['Flair'])

print(le.classes_)

x = list(le.inverse_transform(df["Flair"]))

print(x)

#save the cleaned data to a CSV file 
from google.colab import files
df.to_csv('finalmodeldata2.csv') 
files.download('finalmodeldata2.csv')

print(le.classes__)
