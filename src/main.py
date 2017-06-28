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

def evaluate_model(y, pred, y_metadata):
    '''[summary]
        
    [description]
    
    TODO:
        should handle duplicate counts 
    Args:
        y: [description]
        pred: [description]
    '''
    GRACE_PERIOD = 600 # seconds
    pred = pred['mid'].values
    y = y['cutpoint'].values
    result = {}
    # print('predicted cutpoints dim {}'.format(pred.shape))
    # print(pred)
    # print('labelled cutpoints dim {}'.format(y.shape))
    # print(y)

    delta = np.timedelta64(GRACE_PERIOD, 's')
    is_close = np.abs(y - pred[:, np.newaxis]) <= delta

    num_correct = np.sum(np.any(is_close, axis=1))
    num_cuts = len(y)
    num_pred = len(pred)

    return num_correct, num_cuts, num_pred

def evaluate(root_path, model, root_path_cuts=None):
    '''[summary]
    
    [description]
    
    Args:
        root_path: [root path for test caption data]
        model: [trained model]
    
    Returns:
        [description]
        [type]
    '''
    caption_files = load_caption_files(root_path)
    results = []

    total_num_correct = 0    
    total_num_cuts = 0
    total_num_pred = 0

    for caption_file in caption_files:
        df, metadata = caption_file
    
        if metadata == None:
            print('corrupted caption file... do something')
    
        if root_path_cuts == None:
            if root_path.endswith('/'):
                root_path = root_path[:-1]
            root_path_cuts = root_path
        
        pattern = '{}/**/{}.cuts'.format(root_path_cuts, metadata['filename'])
        paths = glob.glob(pattern, recursive=True)
        
        if len(paths) > 1:
            print('duplicate files with matching caption filename')
    
        cut_files = load_program_cut_files(paths[0])
        y, y_metadata = next(cut_files)
        pred = model.predict(df, keywords=['caption'], merge_time_window=20)   
        num_correct, num_cuts, num_pred  = evaluate_model(y, pred, y_metadata)

        msg = 'There were {} true program cuts. The model predicted ' \
          '{} cuts and {} predicted cuts were true.'    
        print(msg.format(num_cuts, num_pred, num_correct))

        total_num_correct += num_correct    
        total_num_cuts += num_cuts
        total_num_pred += num_pred

    recall = total_num_correct / total_num_cuts
    precision = total_num_correct / total_num_pred
        
    f1_score = 2*(precision*recall)/(precision + recall)
    # return more detailed report like showing failure cases    
    return f1_score


def main():
    # currently only 0-suffixed test_caption/cuts data are in sync
    # the rest of the pairs cannot be evaluated.
    # train, predict, evaluate
    
    # train here
    model = ks.KeywordSearch()
    
    # validate to tune hyperparams here
    
    # test here
    pred_score = evaluate(root_path='test_data/', model=model)
    print(pred_score)
if __name__ == "__main__":
    main()
