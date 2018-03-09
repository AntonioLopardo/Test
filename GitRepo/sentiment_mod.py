
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import keras
import pickle

from keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, Dropout
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import re

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

tokenizer_f = open("tokenizer.pickle", "rb")
tokenizer = pickle.load(tokenizer_f)
tokenizer_f.close()

#embed_dim = 128 #128
#lstm_out = 32 #196
#lstm_out2 = int(196/2)

#model = Sequential()
#model.add(Embedding(50000, embed_dim,input_length = 30))
#model.add(Dropout(0.2, noise_shape=None, seed=None))
#model.add(LSTM(lstm_out, dropout=0.5, recurrent_dropout=0.2))
#model.add(LSTM(lstm_out2, dropout=0.2, recurrent_dropout=0.2))
#model.add(Dense(2,activation='softmax'))
#model.compile(loss = 'categorical_crossentropy', optimizer='adam',metrics = ['accuracy'])
#print(model.summary())

model = load_model('ItalianSentCls.h5')

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

