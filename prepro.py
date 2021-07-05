import os
from os.path import isfile, join
import re
import string
import nltk
import json
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
import sys

nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer('spanish')


def removeChars(txt): # eliminamos las punctuaciones
    delete = ("\"", "\'", "º", "&")
    for char in delete:
        txt = txt.replace(char, "")
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', txt)



def cleanText(txt):
    rootList=[]

    cleanData   = removeChars(txt)
    tok         = TweetTokenizer(preserve_case = False, strip_handles = True, reduce_len = True)
    tokens      = tok.tokenize(cleanData)
    cleanTokens = nltk.word_tokenize(cleanData)

    stoplist = stopwords.words("spanish")
    
    newArr = []
    #recorremos los tokens y removemos todos los stopwords
    for token in tokens:
        if token not in stoplist:
                newArr.append(token)

    #guardamos en una nueva lista la raiz de los tokens limpios
    for token in newArr:
        rootList.append(stemmer.stem(token))
            
    return rootList