# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10jVM4Q2eMiWxoz2WMnVZDhtrELs8zTCi
"""

pip install datasets

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from datasets import load_dataset

#sadness (0), joy (1), love (2), anger (3), fear (4), surprise (5).

# Replace 'emotion' with the name of the emotion dataset you want to load
dataset_name = 'emotion'

# Load the emotion dataset
emotion_dataset = load_dataset(dataset_name)

# Access the train split of the dataset
train_dataset = emotion_dataset['train']
test_dataset = emotion_dataset['test']

import numpy as np

class NaiveBayes:
    def __init__(self, alpha):
        self.classes = None
        self.class_priors = {}
        self.feature_likelihoods = {}
        self.alpha = alpha  # Laplace smoothing parameter

    def fit(self, X, y):
        self.classes = np.unique(y)

        for c in self.classes:
            X_c = X[y == c]
            self.class_priors[c] = np.log((X_c.shape[0]) / (X.shape[0]))

            self.feature_likelihoods[c] = {}
            for feature in range(X.shape[1]):
                count_feature = X_c[:, feature].sum() + self.alpha  # Laplace smoothing
                count_total = X_c.shape[0] + X.shape[1] * self.alpha  # Laplace smoothing
                self.feature_likelihoods[c][feature] = np.log(count_feature / count_total)

    def predict(self, X):
        predictions = []

        for x in X:
            posteriors = []
            for c in self.classes:
                log_likelihood = 0
                for feature, value in enumerate(x):
                    log_likelihood += self.feature_likelihoods[c][feature] * value
                posterior = self.class_priors[c] + log_likelihood
                posteriors.append(posterior)
            predictions.append(self.classes[np.argmax(posteriors)])

        return predictions

    def evaluate_acc(self,y_true, y_pred):
      return np.mean(y_true == y_pred)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

vectorizer = CountVectorizer(stop_words=['english'], ngram_range=(1,1))

corpus = np.array(train_dataset['text'])
counts = vectorizer.fit_transform(corpus)
X_train = np.array(counts.todense())

print(X_train.shape)
y_train = np.array(train_dataset['label'])

corpus = np.array(test_dataset['text'])
counts = (vectorizer.transform(corpus))

X_test = np.array(counts.todense())
y_test = np.array(test_dataset['label'])

# Create and fit the classifier

alpha = [1, 5, 7, 9]
for i in alpha:
    classifier = NaiveBayes(alpha = i)
    classifier.fit(X_train, y_train)

    # Make predictions
    predictions = classifier.predict(X_test)

    # print("Predictions:", predictions)

    print('alpha', i)
    print('accuracy' , classifier.evaluate_acc(y_test, predictions))
    print('F1 score', f1_score(y_test, predictions, average='micro'))
    print('recall', recall_score(y_test, predictions, average='micro'))
    print('precision', precision_score(y_test, predictions, average='micro'))