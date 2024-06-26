# -*- coding: utf-8 -*-
"""AI project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1g_7KuQyVuw_otkDKz4EeXmY2o1yZGvaP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/spam.csv", encoding="latin-1")

df = df.dropna(how="any", axis=1)
df.columns = ['label', 'message']

df.head()

n_unique_data=df['message'].nunique()
display("중복된 데이터의 개수: {}".format(len(df)-n_unique_data))
df.drop_duplicates(subset='message',inplace=True)

n_unique_data_after_drop = df['message'].nunique()
display("중복된 데이터 삭제 후 중복된 데이터의 개수: {}".format(n_unique_data - n_unique_data_after_drop))

print('결측값 여부 :',df.isnull().values.any())

from matplotlib import pyplot as plt
import seaborn as sns
df.groupby('label').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

display(df['label'].value_counts())

print(f'ham 비율 = {round(df["label"].value_counts()[0]/len(df) * 100,3)}%')
print(f'spam 비율 = {round(df["label"].value_counts()[1]/len(df) * 100,3)}%')

df['label_num'] = df.label.map({'ham':0, 'spam':1})
df.head()

df['message_len'] = df['message'].apply(lambda x: len(x.split(' ')))
df.head()

df[df.label=='spam'].describe()

df[df.label=='ham'].describe()

plt.figure(figsize=(10, 7))

df[df.label=='ham'].message_len.plot(bins=30, kind='hist', color='blue',
                                       label='Ham', alpha=0.8)
df[df.label=='spam'].message_len.plot(kind='hist', color='black',
                                       label='Spam', alpha=0.8)
plt.legend()
plt.xlabel("Message Length")

import re
import string

def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

df['message_clean'] = df['message'].apply(clean_text)
df.head()

import nltk
nltk.download('stopwords')

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from keras.layers import (LSTM,
                          Embedding,
                          BatchNormalization,
                          Dense,
                          TimeDistributed,
                          Dropout,
                          Bidirectional,
                          Flatten,
                          GlobalMaxPool1D)

stop_words = stopwords.words('english')
more_stopwords = ['u', 'im', 'c','r']
stop_words = stop_words + more_stopwords

def remove_stopwords(text):
    text = ' '.join(word for word in text.split(' ') if word not in stop_words)
    return text

df['message_clean'] = df['message_clean'].apply(remove_stopwords)
df

import nltk
from nltk.stem import PorterStemmer

# 포터 스태머 초기화
stemmer = PorterStemmer()

def stem_text(text):
    text = ' '.join(stemmer.stem(word) for word in text.split(' '))
    return text

# 데이터프레임의 'message_clean' 열에 어간 추출 함수 적용
df['message_clean'] = df['message_clean'].apply(stem_text)

# 결과 확인
df

stop_words = stopwords.words('english')
more_stopwords = ['v', 'b','iû÷m','å£']
stop_words = stop_words + more_stopwords

def remove_stopwords(text):
    text = ' '.join(word for word in text.split(' ') if word not in stop_words)
    return text

df['message_clean'] = df['message_clean'].apply(remove_stopwords)
df

# Commented out IPython magic to ensure Python compatibility.
import re
import string
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from collections import Counter

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from tqdm import tqdm
import os
import nltk
import spacy
import random
from spacy.util import compounding
from spacy.util import minibatch

from collections import defaultdict
from collections import Counter

import keras
from keras.models import Sequential
from keras.initializers import Constant
from keras.layers import (LSTM,
                          Embedding,
                          BatchNormalization,
                          Dense,
                          TimeDistributed,
                          Dropout,
                          Bidirectional,
                          Flatten,
                          GlobalMaxPool1D)
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    accuracy_score
)

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 워드클라우드 생성
wc = WordCloud(
    background_color='black',  # 배경색상을 흰색으로 설정
    max_words=200  # 최대 단어 수를 200개로 제한
)

# 텍스트 데이터를 이용하여 워드클라우드 생성
# 여기에는 적절한 텍스트 데이터를 입력하세요
wc.generate(' '.join(text for text in df.loc[df['label'] == 'ham', 'message_clean']))

# 워드클라우드를 그림으로 표시
plt.figure(figsize=(10, 5))
plt.title('Top words for HAM messages', fontdict={'size': 15, 'verticalalignment': 'bottom'})
plt.imshow(wc)
plt.axis("off")  # 축을 표시하지 않음
plt.show()

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 워드클라우드 생성
wc = WordCloud(
    background_color='black',  # 배경색상을 흰색으로 설정
    max_words=200  # 최대 단어 수를 200개로 제한
)

# 텍스트 데이터를 이용하여 워드클라우드 생성
# 여기에는 적절한 텍스트 데이터를 입력하세요
wc.generate(' '.join(text for text in df.loc[df['label'] == 'spam', 'message_clean']))

# 워드클라우드를 그림으로 표시
plt.figure(figsize=(10, 5))
plt.title('Top words for SPAM messages', fontdict={'size': 15, 'verticalalignment': 'bottom'})
plt.imshow(wc)
plt.axis("off")  # 축을 표시하지 않음
plt.show()

df['message_clean_len'] = df['message_clean'].apply(lambda x: len(x.split(' ')))
df

df.describe()

max_length_text_row = df[df['message_clean_len'] == df['message_clean_len'].max()]['message_clean'].iloc[0]

print("Max length text:", max_length_text_row)

max_length_index = df['message_clean_len'].idxmax()

# 가장 긴 텍스트를 포함한 행 삭제하기
df = df.drop(max_length_index)

df.describe()

words = df[df.label=='ham'].message_clean.apply(lambda x: [word.lower() for word in x.split()])
spam_words = Counter()

for msg in words:
    spam_words.update(msg)

print(spam_words.most_common(50))

X_data=df['message']
y_data=df['label']

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_data) # X_data의 각 행에 토큰화를 수행
sequences = tokenizer.texts_to_sequences(X_data) # 단어를 숫자값, 인덱스로 변환하여 저장
print(sequences[-3:-1])

word_to_index = tokenizer.word_index
print(word_to_index)

x = df['message_clean']
y = df['label_num']

print(len(x), len(y))

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
print(len(x_train), len(y_train))
print(len(x_test), len(y_test))

from sklearn.feature_extraction.text import CountVectorizer

# instantiate the vectorizer
vect = CountVectorizer()
vect.fit(x_train)

x_train_dtm = vect.transform(x_train)
x_test_dtm = vect.transform(x_test)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()
tfidf_transformer.fit(x_train_dtm)
tfidf_transformer.transform(x_train_dtm)

tfidf_transformed = tfidf_transformer.transform(x_train_dtm)
print(tfidf_transformed)

import plotly.figure_factory as ff

x_axes = ['Ham', 'Spam']
y_axes =  ['Spam', 'Ham']

def conf_matrix(z, x=x_axes, y=y_axes):

    z = np.flip(z, 0)

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')

    # add title
    fig.update_layout(title_text='<b>Confusion matrix</b>',
                      xaxis = dict(title='Predicted value'),
                      yaxis = dict(title='Real value')
                     )

    # add colorbar
    fig['data'][0]['showscale'] = True

    return fig

from sklearn.naive_bayes import MultinomialNB
nb = MultinomialNB()

# Train the model
nb.fit(x_train_dtm, y_train)

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

classifiers = [MultinomialNB(),
               RandomForestClassifier(),
               KNeighborsClassifier(),
               SVC()]
for cls in classifiers:
    cls.fit(x_train_dtm, y_train)

# Dictionary of pipelines and model types for ease of reference
pipe_dict = {0: "NaiveBayes", 1: "RandomForest", 2: "KNeighbours",3: "SVC"}
# Cossvalidation
for i, model in enumerate(classifiers):
    cv_score = cross_val_score(model, x_train_dtm,y_train,scoring="accuracy", cv=10)
    print("%s: %f " % (pipe_dict[i], cv_score.mean()))

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

# Instantiate the decision tree classifier
dt_classifier = DecisionTreeClassifier()

# Train the model
dt_classifier.fit(x_train_dtm, y_train)

# Make class predictions for X_test_dtm
y_pred_class = dt_classifier.predict(x_test_dtm)

# Calculate accuracy of class predictions
print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# Print the confusion matrix
print("=======Confusion Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

from sklearn import metrics

def classification_metrics(y_true, y_pred):
    # 혼동 행렬 계산
    cm = metrics.confusion_matrix(y_true, y_pred)

    # 정확도 계산
    accuracy = metrics.accuracy_score(y_true, y_pred)

    # 정밀도 계산
    precision = metrics.precision_score(y_true, y_pred)

    # 재현율 계산
    recall = metrics.recall_score(y_true, y_pred)

    # F1 점수 계산
    f1_score = metrics.f1_score(y_true, y_pred)

    return {
        'Confusion Matrix': cm,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1_score
    }

# 분류 지표 계산
classification_results = classification_metrics(y_test, y_pred_class)
print(classification_results)

from sklearn.linear_model import LogisticRegression

# Instantiate the logistic regression classifier
lr_classifier = LogisticRegression()

# Train the model
lr_classifier.fit(x_train_dtm, y_train)

# Make class predictions for X_test_dtm
y_pred_class = lr_classifier.predict(x_test_dtm)

# Calculate accuracy of class predictions
print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# Print the confusion matrix
print("=======Confusion Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

def plot_confusion_matrix(y_true, y_pred):
    cm = metrics.confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.title('Confusion Matrix')
    plt.show()

# 테스트 세트에 대한 혼동 행렬 시각화
plot_confusion_matrix(y_test, y_pred_class)

from sklearn.metrics import roc_curve, auc

# Calculate the false positive rate (FPR) and true positive rate (TPR)
fpr, tpr, thresholds = roc_curve(y_test, lr_classifier.predict_proba(x_test_dtm)[:,1])

# Calculate the Area Under the Curve (AUC)
roc_auc = auc(fpr, tpr)

# Plot the ROC curve
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()

from sklearn.metrics import precision_recall_curve

# Calculate precision and recall
precision, recall, _ = precision_recall_curve(y_test, lr_classifier.predict_proba(x_test_dtm)[:,1])

# Plot the Precision-Recall curve
plt.figure()
plt.step(recall, precision, color='b', alpha=0.2, where='post')
plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.ylim([0.0, 1.05])
plt.xlim([0.0, 1.0])
plt.title('Precision-Recall curve')
plt.show()

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, auc

# ROC 곡선 계산
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

# Precision-Recall 곡선 계산
precision, recall, _ = precision_recall_curve(y_test, y_pred_prob)

# ROC 곡선 그리기
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

# Precision-Recall 곡선 그리기
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='blue', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()



from sklearn import metrics

def classification_metrics(y_true, y_pred):
    # 혼동 행렬 계산
    cm = metrics.confusion_matrix(y_true, y_pred)

    # 정확도 계산
    accuracy = metrics.accuracy_score(y_true, y_pred)

    # 정밀도 계산
    precision = metrics.precision_score(y_true, y_pred)

    # 재현율 계산
    recall = metrics.recall_score(y_true, y_pred)

    # F1 점수 계산
    f1_score = metrics.f1_score(y_true, y_pred)

    return {
        'Confusion Matrix': cm,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1_score
    }

# 분류 지표 계산
classification_results = classification_metrics(y_test, y_pred_class)
print(classification_results)

from sklearn.ensemble import RandomForestClassifier

# Instantiate the random forest classifier
rf_classifier = RandomForestClassifier()

# Train the model
rf_classifier.fit(x_train_dtm, y_train)

# Make class predictions for X_test_dtm
y_pred_class = rf_classifier.predict(x_test_dtm)

# Calculate accuracy of class predictions
print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# Print the confusion matrix
print("=======Confusion Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

def plot_confusion_matrix(y_true, y_pred):
    cm = metrics.confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.title('Confusion Matrix')
    plt.show()

# 테스트 세트에 대한 혼동 행렬 시각화
plot_confusion_matrix(y_test, y_pred_class)

from sklearn.svm import SVC

# Instantiate the support vector machine classifier
svm_classifier = SVC()

# Train the model
svm_classifier.fit(x_train_dtm, y_train)

# Make class predictions for X_test_dtm
y_pred_class = svm_classifier.predict(x_test_dtm)

# Calculate accuracy of class predictions
print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# Print the confusion matrix
print("=======Confusion Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

def plot_confusion_matrix(y_true, y_pred):
    cm = metrics.confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.title('Confusion Matrix')
    plt.show()

# 테스트 세트에 대한 혼동 행렬 시각화
plot_confusion_matrix(y_test, y_pred_class)

from sklearn.neighbors import KNeighborsClassifier

# Instantiate the KNN classifier
knn_classifier = KNeighborsClassifier()

# Train the model
knn_classifier.fit(x_train_dtm, y_train)

# Make class predictions for X_test_dtm
y_pred_class = knn_classifier.predict(x_test_dtm)

# Calculate accuracy of class predictions
print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# Print the confusion matrix
print("=======Confusion Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

def plot_confusion_matrix(y_true, y_pred):
    cm = metrics.confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.title('Confusion Matrix')
    plt.show()

# 테스트 세트에 대한 혼동 행렬 시각화
plot_confusion_matrix(y_test, y_pred_class)

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, auc

# ROC 곡선 계산
fpr, tpr, _ = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

# Precision-Recall 곡선 계산
precision, recall, _ = precision_recall_curve(y_test, y_pred_prob)

# ROC 곡선 그리기
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

# Precision-Recall 곡선 그리기
plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='blue', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()

from sklearn import metrics

# 실제값과 예측값을 이용하여 혼동 행렬 계산
cm = metrics.confusion_matrix(y_test, y_pred_class)

# 혼동 행렬 출력
print(cm)

# Commented out IPython magic to ensure Python compatibility.
# import an instantiate a logistic regression model
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression(solver='liblinear')

# train the model using X_train_dtm
# %time logreg.fit(x_train_dtm, y_train)

y_pred_class = logreg.predict(x_test_dtm)

# calculate predicted probabilities for X_test_dtm (well calibrated)
y_pred_prob = logreg.predict_proba(x_test_dtm)[:, 1]
y_pred_prob

print("=======Accuracy Score===========")
print(metrics.accuracy_score(y_test, y_pred_class))

# print the confusion matrix
print("=======Confision Matrix===========")
print(metrics.confusion_matrix(y_test, y_pred_class))

# calculate AUC
print("=======ROC AUC Score===========")
print(metrics.roc_auc_score(y_test, y_pred_prob))