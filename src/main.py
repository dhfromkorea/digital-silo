#!/usr/bin/env python3

'''
TODO
1. load data (caption, video, audio)
2. split the data into training and test
3. load model and train on the trainig data
4. test the model against the test data
5. report the training/testing error
6. visualize basic stats

terminologies
    shot ->(A) scene ->(B) story/commercial ->(C) program ->(D) video
    below are cuts or boundaries, or transitions
    A = shot cuts
    B = scene cuts
    C = story cuts (or commercial)
    D = program cuts
'''

from models.text import keyword_search as ks
from utilities.data_utils import *

import numpy as np
import re

def evaluate_model(y, pred):
    '''[summary]
        
    [description]
    
    TODO:
        should handle duplicate counts 
    Args:
        y: [description]
        pred: [description]
    '''
    GRACE_PERIOD = 1 # seconds

    pred = pred['mid'].values
    y = y['cutpoint'].values

    # print('predicted cutpoints dim {}'.format(pred.shape))
    # print(pred)
    # print('labelled cutpoints dim {}'.format(y.shape))
    # print(y)

    delta = np.timedelta64(GRACE_PERIOD, 's')

    is_close = np.abs(y - pred[:, np.newaxis]) <= delta
    num_correct = np.sum(np.any(is_close, axis=1))
    num_cuts = len(y)

    pred_accuracy = num_correct / num_cuts    
    print('The model got {} out of {} correct\naccuracy: {}'.format(num_correct, num_cuts, pred_accuracy))    


def main():
    df, _, _ = load_caption_data()
    y = load_program_cut_data()

    model = ks.KeywordSearch()
    predicted_indices = model.predict(df, 'caption')
    pred = df.loc[predicted_indices]

    evaluate_model(y, pred)

if __name__ == "__main__":
    main()
