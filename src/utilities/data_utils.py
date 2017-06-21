CAPTION_FILEPATH = '../data/2006/2006-06/2006-06-13/example.txt3'
CUT_FILEPATH = '../data/2006/2006-06/2006-06-13/example.cuts'

import pandas as pd
import numpy as np


def load_caption_data():
    def date_parser(x):
        '''[summary]
        
        [description]
        
        Args:
            x: [description]
        
        Returns:
            [description]
            [type]
        '''
        try:
            f = lambda x: pd.datetime.strptime(x, '%Y%m%d%H%M%S.%f')
            a = np.vectorize(f)(x[:-1])
            # the last line gets to be a problem. this is a workaround to bypass it.
            return np.append(a, "")
        except Exception as e:
            print(e)
            print('If the error is about END, you can ignore this')

    col_names = ['start', 'end', 'marker', 'caption']
    df = pd.read_csv(CAPTION_FILEPATH, sep='|', header=None, names=col_names,
                     parse_dates=['start', 'end'], date_parser=date_parser,
                     dtype={'start':str, 'end':str})

    is_end, _, filename, _ = df.iloc[df.shape[0] - 1]
    df = df[:-1]
    df['mid'] = df['start'] + 0.5 * (df['end'] - df['start'])
    return (df, is_end, filename)

def load_cutfiles():
    '''[summary]
    
    [description]
    
    Returns:
        [description]
        [type]
    '''
    col_names = ['vcr', 'recording_date', 'vcr_2', 'recording_date_2',
        'start', 'end', 'schedule', 'program']
    def date_parser(a, b):
        c = '{} {}'.format(a, b)
        f = lambda x: pd.datetime.strptime(x, '%m/%d/%y %H:%M:%S')
        return f(c)

    #date_parse = lambda x: pd.datetime.strptime(x, '%Y:%m:%d %H:%M:%S')
    df = pd.read_csv(CUT_FILEPATH, sep='\t', header=None, names=col_names,
                     parse_dates={'cutpoint': ['recording_date', 'start']}, date_parser=date_parser
                     )
    #leave the first and the last timestamp as they tend to be noisy
    #they may not be the trust program boundaries so it hinders the training.
    #TODO: a counter argument is that they are roughly right, since we suffer from
    #shortage of labelled boundaries so it may be more useful to keep them?
    df = df[['cutpoint', 'vcr', 'program']][1:]
    return df
