
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras
import pickle

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

tokenizer_f = open("model_files/tokenizer.pickle", "rb")
tokenizer = pickle.load(tokenizer_f)
tokenizer_f.close()

model = load_model('model_files/ItalianSentCls.h5')

def sentiment(text):
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

    return sentiment, confidence

