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

shot < scene < segment (story, commercial) < program

'''


import pandas as pd
import numpy as np
import re
CAPTION_FILE_PATH = '../data/2006/2006-06/2006-06-13/example.txt3'
CUT_FILE_PATH = '../data/2006/2006-06/2006-06-13/example.cuts'

def load_caption_data(path):
    def date_parser(x):
        try:
            f = lambda x: pd.datetime.strptime(x, '%Y%m%d%H%M%S.%f')
            a = np.vectorize(f)(x[:-1])
            # the last line gets to be a problem. this is a workaround to bypass it.
            return np.append(a, "")
        except Exception as e:
            print(e)
            print('If the error is about END, you can ignore this')

    col_names = ['start', 'end', 'marker', 'caption']
    df = pd.read_csv(path, sep='|', header=None, names=col_names,
                     parse_dates=['start', 'end'], date_parser=date_parser,
                     dtype={'start':str, 'end':str})

    is_end, _, filename, _ = df.iloc[df.shape[0] - 1]
    df = df[:-1]
    df['mid'] = df['start'] + 0.5 * (df['end'] - df['start'])
    return (df, is_end, filename)

def load_cut_files(path):
    col_names = ['vcr', 'recording_date', 'vcr_2', 'recording_date_2',
        'start', 'end', 'schedule', 'program']
    def date_parser(a, b):
        c = np.core.defchararray.add(a, b)        
        f = lambda x: pd.datetime.strptime(x, '%m/%d/%y%H:%M:%S')
        return np.vectorize(f)(c)

    #date_parse = lambda x: pd.datetime.strptime(x, '%Y:%m:%d %H:%M:%S')
    df = pd.read_csv(path, sep='\t', header=None, names=col_names,
                     parse_dates={'cut_time': ['recording_date', 'start']}, date_parser=date_parser
                     )
    #leave the first and the last timestamp as they tend to be noisy
    #they may not be the trust program boundaries so it hinders the training.
    #TODO: a counter argument is that they are roughly right, since we suffer from
    #shortage of labelled boundaries so it may be more useful to keep them?
    df = df[['cut_time', 'vcr', 'program']][1:]
    return df

def cc_keyword(df, *args):
    pattern = r'|'.join(args)
    return df['caption'].str.contains(pattern, flags=re.IGNORECASE)

def evaluate(pred, y):
    '''[summary]
    
    decision time window (grace period) of 3 seconds before and after the predicted timestamp

    Inputs:
        pred {[Dataframe]} -- [description]
        y {[Dataframe]} -- [description]

    Returns:
        accuracy:
    '''
    GRACE_PERIOD = 3.0 # seconds
    # df['lower_bound'] = 
    # df['upper_bound'] = 
    pass

def main():
    df, is_end, filename = load_caption_data(CAPTION_FILE_PATH)
    df2 = load_cut_files(CUT_FILE_PATH)
    
    # print(df.head())
    # print("SLDKJFLKSJFD LJ LKSDJFLSDJLFKJSDLFJSLKJL")
    print(df2.head())
    
    is_segment = df['marker'].str.contains('seg', case=False)
    is_story = df['caption'].str.contains('story', case=False)
    is_commercial = df['caption'].str.contains('commercial', case=False)
    contains_caption_keyword = cc_keyword(df, 'caption', 'good morning')

    story_boundaries = df.loc[is_segment & is_story]
    commercial_boundaries = df.loc[is_segment & is_commercial]
    predicted_boundaries = df.loc[contains_caption_keyword]

if __name__ == "__main__":
    main()

