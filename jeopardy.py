import pandas as pd
import string
import re
import numpy as np
import datetime

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)

jeopardy_data = pd.read_csv('jeopardy.csv')
jeopardy_data.rename(columns = {
        'Show Number': 'show_number', 
        ' Air Date': 'air_date', 
        ' Round': 'round', 
        ' Category': 'category', 
        ' Value': 'value',
        ' Question': 'question', 
        ' Answer': 'answer'
        }, inplace=True)
#jeopardy_data.columns = jeopardy_data.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#whitespace_punctuation = []
#for char in (string.whitespace + string.punctuation):
#    whitespace_punctuation.append(char)
#plurals = []
#for char in whitespace_punctuation:
#    plurals.append('s' + char)
#suffices = whitespace_punctuation + plurals

class Jeopardy:

    def __init__(self, jeopardy_data):
        self.jeopardy_data = jeopardy_data
        
    def format_word(self, word):
        search_terms = []

        #prefices = [' ', "'", '"']#, '(', '[', '{']
        suffices = [' ', "'", '"', '.', ',', '!', '?', 's']#, ')', ']', '}', ';', ':', '/']

        for suffix in (suffices):
            key = ' ' + word.lower() + suffix
            search_terms.append(key)

        return search_terms

    def filter_questions(self, word_list, data):
        search_data = data
        #word_list = ['King', 'England', 'kind', 'random', 'words', 'make', 'list', 'long', 'happy', 'sad', 'emotions', 'scared', 'want', 'live', 'therapy', 'Yoni', 'Eliza', 'room', 'table', 'tensor', 'anxiety', 'codecamp', 'fun', 'programming', 'movies', 'party', 'show', 'alert', 'cup', 'coffee', 'mug', 'bagels', 'cos', 'painting', 'art', 'much']
        for word in word_list:
            search_terms = self.format_word(word)
            filtered_data = search_data[search_data.apply(lambda row: any([term in row.question.lower() for term in search_terms]), axis=1)].reset_index()
            search_data = filtered_data
        #filtered_data = jeopardy_data[jeopardy_data.apply(lambda row: [jeopardy_data.question.str.contains(all(word for word in word_list))])]
        #filtered_data = jeopardy_data[jeopardy_data.apply(lambda row: all(word in row.question for word in word_list))]

        return search_data

# make time_frames work with function
    def question_time_filter(self, word_list, time_frames):
        filtered_questions = jd.filter_questions(word_list, jeopardy_data)
        #filtered_questions['air_date_dt'] = pd.to_datetime(computer_questions.air_date, format='%Y-%m-%d')
        filtered_questions['air_date_dt'] = pd.to_datetime(filtered_questions.air_date)
        #print('Type of air_dat_dt', type(computer_questions.air_date_dt))
        filtered_qs_1 = filtered_questions[(filtered_questions.air_date_dt.dt.year >= 1990) & (filtered_questions.air_date_dt.dt.year < 2000)]
        filtered_qs_2 = filtered_questions[(filtered_questions.air_date_dt.dt.year >= 2000) & (filtered_questions.air_date_dt.dt.year < 2010)]
        print('Computer in 1990s: ' + str(filtered_qs_1.shape[0]) + ' Computer in 2000s: ' + str(filtered_qs_2.shape[0]))

jd = Jeopardy(jeopardy_data)
#jd.jeopardy_data['value_float'] = jd.jeopardy_data.value.str.replace('$', '').str.replace(',', '').str.replace('None', '0').astype('float')
jd.jeopardy_data['value'] = jd.jeopardy_data.value.str.replace('$', '').str.replace(',', '').str.replace('None', '0').astype('float')
values = jd.jeopardy_data.value
#values = jd.jeopardy_data.value_float
#print(values)
#word_list = ['king', 'England']
#word_list = ['happy', 'go']
word_list = ['King']
filtered_data = jd.filter_questions(word_list, jeopardy_data)
print('mean = $' + str(round(float(filtered_data.value.mean()), 2)))
unique_answers = pd.value_counts(filtered_data.answer)
print(unique_answers)
print('Unique answers to questions with King: ' + str(filtered_data.answer.nunique()))
print('How many questions have the word King: ' + str(filtered_data.shape[0]))
filtered_questions = filtered_data.question
print(filtered_questions)
print(filtered_data.value.mean())

### Additional Questions
#print(jd.jeopardy_data.air_date.head())


category_by_round = jd.jeopardy_data.groupby(['round', 'category']).question.count().reset_index()
#category_by_round = jd.jeopardy_data.pivot(index = 'round', columns = 'category', values = 'question')
print(category_by_round)