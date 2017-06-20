#!/usr/bin/env python3

'''
TODO
1. load data (caption, video, audio)
2. split the data into training and test
3. load model and train on the trainig data
4. test the model against the test data
5. report the training/testing error
'''

import pandas as pd

DATA_PATH = '../data/2006/2006-06/2006-06-13/example.txt3'
headers = ['start', 'end', 'marker', 'caption']
df = pd.read_csv(DATA_PATH, sep='|', header=None, names=headers)

is_boundary = (df['marker'] == 'SEG_00')
is_story = df['caption'].str.contains('story', case=False)
is_commercial = df['caption'].str.contains('commercial', case=False)
contains_caption_keyword = df['caption'].str.contains('caption', case=False)

story_boundaries = df.loc[is_boundary & is_story]
commercial_boundaries = df.loc[is_boundary & is_commercial]

print(contains_caption_keyword.dropna(axis=0, how='all'))
predicted_boundaries = df.loc[contains_caption_keyword]
# print(predicted_boundaries)