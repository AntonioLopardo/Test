'''
sent_mod importing the keras model performs the sentiment analysis on every tweet
'''
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras
import pickle

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

tokenizer_f = open("model_files/tokenizer.pickle", "rb")
tokenizer = pickle.load(tokenizer_f)
tokenizer_f.close()

tokenizer.oov_token = None

model = load_model('model_files/ItalianSentCls.h5')

def sentiment(text,lang):
    '''
    for an Italian tweet sentiment computes the sentiment of the text 
    given returning 1 if it's more confident the text given is positive and 0 
    otherwise, alongside the sentiment it returns a confidence score
    from 0.5 to 1.0
    While for an english tweet it computes the sentiment using textblob returning
    a sentiment of 3 for neutral tweets, to be discarded, 1 if it's more confident 
    the text given is positive and 0 otherwise, alongside the sentiment it returns 
    a confidence score from 0.0 to 1.0
    '''
    if lang is 'it' :
        text = [text]
        text = tokenizer.texts_to_sequences(text)
        #print(text)
        text = pad_sequences(text, maxlen = 30)
        #print(text)
        results = model.predict(text)

        if results[0][0] > results[0][1]:
            sentiment = 0
            confidence = results[0][0]
        else:
            sentiment = 1
            confidence = results[0][1]
    
    elif lang is 'en':
        textb = TextBlob(text)
        sentiment = 3
        confidence = 0.0
        
        if textb.sentiment.polarity < 0:
            sentiment = 0
            confidence = -(textb.sentiment.polarity)
            
        if textb.sentiment.polarity > 0:
            sentiment = 1
            confidence = (textb.sentiment.polarity)

    return sentiment, confidence


