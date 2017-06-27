import pandas as pd
import numpy as np
import glob

CAPTION_DB_PATH = '../data/2006/2006-06/2006-06-13/2006-06-13_0000_US_00000141_V11_MB12_VHS13_H2_JK.txt3'
CUT_DB_PATH = '../data/2006/2006-06/2006-06-13/2006-06-13_0000_US_00000141_V11_MB12_VHS13_H2_JK.cuts'


def _date_parser(pattern):
    def f(date):
        parsed = ''
        try:
            parsed = pd.datetime.strptime(date, pattern)
        except Exception as e:
            # strip off the first 4/8 lines (header) the last line (footer)
            # print(e)
            pass
        return parsed    
    return f


def _caption_date_parser(col):
    return np.vectorize(_date_parser('%Y%m%d%H%M%S.%f'))(col)


def _cut_date_parser(date_A, date_B):
    date = '{} {}'.format(date_A, date_B)
    return _date_parser('%m/%d/%y %H:%M:%S')(date)


def _load_csv_file(path, sep, names, parse_dates, date_parser, dtype=None):
    try:
        df = pd.read_csv(path, sep=sep, header=None, names=names,
                         parse_dates=parse_dates, date_parser=date_parser,
                         dtype=dtype)
        return df
    except Exception as e:
        print(e)
        pass

def _load_single_caption_file(path):
    col_names = ['start', 'end', 'marker', 'caption']
    df = _load_csv_file(path, sep='|', names=col_names,
                     parse_dates=['start', 'end'], date_parser=_caption_date_parser,
                     dtype={'start':str, 'end':str})
    df = df.dropna()
    df = df.reset_index(drop=True)
    df = df[:-1]
    df['mid'] = df['start'] + 0.5 * (df['end'] - df['start'])
    metadata = {
                   'filename': '',
                   'date': '',
                   'vcr_index':''
                }
    
    return (df, metadata)


def load_caption_files(root_path, recursive_search=False):
    '''[summary]
    
    [description]
    
    Returns:
        [description]
        [type]
    '''
    if root_path.endswith('.txt3'):
        #single file=        
        yield _load_single_caption_file(root_path)
    else:
        if root_path.endswith('/'):
            root_path += '**/*.txt3'
        else:
            root_path += '/**/*.txt3'
        filepaths = glob.iglob(root_path, recursive=recursive_search)
        
        for path in filepaths:
            yield _load_single_caption_file(path)
    

def load_program_cut_files(path):
    '''[summary]
    
    [description]
    
    Returns:
        [description]
        [type]
    '''
    col_names = ['vcr', 'recording_date', 'vcr_2', 'recording_date_2',
        'start', 'end', 'schedule', 'program']
    #date_parse = lambda x: pd.datetime.strptime(x, '%Y:%m:%d %H:%M:%S')

    df = _load_csv_file(path, sep='\t', names=col_names,
                       parse_dates={'cutpoint': ['recording_date', 'start']},
                       date_parser=_cut_date_parser)
    df.dropna()

    #leave the first and the last timestamp as they tend to be noisy
    #they may not be the trust program boundaries so it hinders the training.
    #TODO: a counter argument is that they are roughly right, since we suffer from
    #shortage of labelled boundaries so it may be more useful to keep them?
    df = df[['cutpoint', 'vcr', 'program']][1:]
    df = df.reset_index(drop=True)
    return df
