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
shot < scene < segment (story, commercial) <(cutpoint) program
'''
import pandas as pd
import numpy as np
import re

from models.text import keyword_search as ks


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
        c = '{} {}'.format(a, b)
        f = lambda x: pd.datetime.strptime(x, '%m/%d/%y %H:%M:%S')
        return f(c)

    #date_parse = lambda x: pd.datetime.strptime(x, '%Y:%m:%d %H:%M:%S')
    df = pd.read_csv(path, sep='\t', header=None, names=col_names,
                     parse_dates={'cutpoint': ['recording_date', 'start']}, date_parser=date_parser
                     )
    #leave the first and the last timestamp as they tend to be noisy
    #they may not be the trust program boundaries so it hinders the training.
    #TODO: a counter argument is that they are roughly right, since we suffer from
    #shortage of labelled boundaries so it may be more useful to keep them?
    df = df[['cutpoint', 'vcr', 'program']][1:]
    return df

def cc_keyword(df, *args):
    pattern = r'|'.join(args)
    return df['caption'].str.contains(pattern, flags=re.IGNORECASE)

def evaluate_model(y, pred):
    '''[summary]
    
    decision time window (grace period) of 3 seconds before and after the predicted timestamp

    Inputs:
        pred {[Dataframe]} -- [1 X N array of predicted cutpoints]
        y {[Dataframe]} -- [1 X M array of true cutpoints]

    Returns:
        accuracy:
    '''
    GRACE_PERIOD = 5 # seconds

    pred = pred['mid'].values
    y = y['cutpoint'].values

    # print('predicted cutpoints dim {}'.format(pred.shape))
    # print(pred)
    # print('labelled cutpoints dim {}'.format(y.shape))
    # print(y)

    delta = np.timedelta64(GRACE_PERIOD, 's')
    is_close = np.abs(y - pred[:,np.newaxis]) <= delta
    print(np.any(is_close, axis=1))
    
    # print(pred + delta)
    # print("GSDJKFKDSJLF KJSDLK FJLSDJFLKSJ")

    pass

def main():
    df, _, _ = load_caption_data(CAPTION_FILE_PATH)
    y = load_cut_files(CUT_FILE_PATH)

    # print(df.head())
    # print("SLDKJFLKSJFD LJ LKSDJFLSDJLFKJSDLFJSLKJL")
    # print(df2['cutpoint'].head())
    
    # is_segment = df['marker'].str.contains('seg', case=False)
    # is_story = df['caption'].str.contains('story', case=False)
    # is_commercial = df['caption'].str.contains('commercial', case=False)
    # story_boundaries = df.loc[is_segment & is_story]
    # commercial_boundaries = df.loc[is_segment & is_commercial]

    model = ks.KeywordSearch()

    predicted_indices = model.predict(df, 'caption')
    pred = df.loc[predicted_indices]

    evaluate_model(y, pred)

if __name__ == "__main__":
    main()

