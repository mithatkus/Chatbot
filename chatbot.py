# -*- coding: utf-8 -*-
"""Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K8hmYmTtSo_7gwF8bW0GQUwhkanZ1IOK
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 2.x

import json
import numpy as np
import nltk
import numpy
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random

stemmer = LancasterStemmer()

from google.colab import files
uploaded = files.upload()

with open ('intents.json') as file:
    data = json.load(file)

#preprocessing

words = []
labels = []
docs_x = []
docs_y = []

import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent['tag'])

    if intent['tag'] not in labels:
        labels.append(intent['tag'])

stemmer = LancasterStemmer()

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for x in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

model = Sequential()
model.add(Dense(units=8, activation='relu', input_shape=(len(training[0]),)))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=len(output[0]), activation='softmax'))

optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(training, output, epochs=1000, batch_size=8)

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        bag = bag_of_words(inp, words)
        results = model.predict(np.array([bag]))[0]
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))

chat()