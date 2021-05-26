import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import linear_kernel


def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf




df = pd.read_csv('scrappedNews.csv',encoding = "ISO-8859-1")


a=df['Description']


filtered_list=[]

#Removing Stop Words

for i in range(0,len(a)):  
    stop_words = set(stopwords.words('english')) 
  
    word_tokens = word_tokenize(a[i]) 
  
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
    filtered_sentence = [] 
  
    for w in word_tokens: 
        if w.lower() not in stop_words: 
            filtered_sentence.append(w)  
    filtered_list.append(filtered_sentence)


#Unique Words 
uniqueueWordz = set(filtered_list[0])
for i in range(1,len(filtered_list)):
    uniqueueWordz= set(uniqueueWordz).union(set(filtered_list[i]))

#number of Words from uniqueWords
number_of_words=[]
for i in range(0,len(filtered_list)):
    numOfWordsA = dict.fromkeys(uniqueueWordz, 0)
    for word in filtered_list[i]:
        numOfWordsA[word] += 1
    number_of_words.append(numOfWordsA)

#Tf from Bow

tfList=[]
for i in range(0,len(filtered_list)):
    a=computeTF(number_of_words[i],filtered_list[i])
    tfList.append(a)

#idfs
idfs = computeIDF(number_of_words)

#tfidf from tf and idf
tfidfList=[]
for i in range(0,len(filtered_list)):
    tfidf = computeTFIDF(tfList[i],idfs)
    tfidfList.append(tfidf)

#similarities
tfidfList2 =[]
for i in range(0, len(tfidfList)):
    temp=[]
    for j in tfidfList[i]:
        temp.append(tfidfList[i][j])
    tfidfList2.append(temp)
#provide here vector of article whose           (here)     recommendations you want
cosine_similarities = linear_kernel(tfidfList2[150:151], tfidfList2).flatten()
cosine_similarities[170]

#Top Most Similar Article Indexes
related_docs_indices = cosine_similarities.argsort()[-2:-7:-1]


