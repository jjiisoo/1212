# -*- coding: utf-8 -*-
"""AIPP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rJiW9UGGW5VDVtNPOucZAZBAqPxU2x0P
"""

import re
import string
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')

# 전처리 함수 정의
def clean_text(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

stop_words = stopwords.words('english')
more_stopwords = ['u', 'im', 'c', 'r', 'v', 'b', 'iû÷m', 'å£']
stop_words = stop_words + more_stopwords

def remove_stopwords(text):
    text = ' '.join(word for word in text.split(' ') if word not in stop_words)
    return text

stemmer = PorterStemmer()

def stem_text(text):
    text = ' '.join(stemmer.stem(word) for word in text.split(' '))
    return text

def preprocess_text(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    text = stem_text(text)
    return text

# CountVectorizer 및 TfidfTransformer 불러오기
with open('count_vectorizer.pkl', 'rb') as cv_file:
    loaded_vect = pickle.load(cv_file)



# 모델 불러오기
with open('logistic_regression_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

def classify_text(text):
    # 텍스트 전처리
    processed_text = preprocess_text(text)

    # 벡터화 및 TF-IDF 변환
    text_counts = loaded_vect.transform([processed_text])


    # 모델에 전달하여 분류
    predicted_label = model.predict(text_counts)
    return predicted_label[0]

if __name__ == "__main__":
    while True:
        user_text = input("Enter the text to classify (or type 'exit' to quit): ")
        if user_text.lower() == 'exit':
            print("Exiting the program...")
            break
        result = classify_text(user_text)
        print("The text is classified as:", "spam" if result == 1 else "ham")