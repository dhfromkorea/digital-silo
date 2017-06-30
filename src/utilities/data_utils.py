import pandas as pd
import numpy as np
import glob
import os
import math

def _date_parser(pattern):
    def f(date):
        try:
            parsed = pd.datetime.strptime(date, pattern)
        except Exception as e:
            # the first 4 or 8 lines (header) and the last line won't be parsed
            parsed = ''            
        return parsed    
    return f


def _caption_date_parser(col):
    return np.vectorize(_date_parser('%Y%m%d%H%M%S.%f'))(col)


def _p_boundary_date_parser(date_A, date_B):
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
    col_names = ['t_start', 't_end', 'marker', 'caption']
    df = _load_csv_file(path, sep='|', names=col_names,
                        parse_dates=['t_start', 't_end'],
                        date_parser=_caption_date_parser,
                        dtype={'t_start':str, 't_end':str})
    # cleanse column data here
    df.drop(['marker', 't_end'], axis=1, inplace=True)
    df = df.dropna()
    df = df.reset_index(drop=True)
    metadata = annotate_file(path)    
    
    return (df, metadata)


def _load_single_program_boundary_file(path):
    col_names = ['vcr_i', 'recording_date', 'vcr_i_2', 'recording_date_2',
        't_start', 't_end', 't_schedule', 'program_name']
    df = _load_csv_file(path, sep=r'\s+', names=col_names,
                       parse_dates={'t_program_boundary': ['recording_date', 't_start']},
                       date_parser=_p_boundary_date_parser)
   
    # cleanse column data here
    cols_to_drop = ['vcr_i', 'vcr_i_2', 'recording_date_2',
                   't_end', 't_schedule', 'program_name']
    df.drop(cols_to_drop, axis=1, inplace=True)
    df.dropna()
    df = df.reset_index(drop=True)
    metadata = annotate_file(path)

    return (df, metadata)

def annotate_file(path):
    base = os.path.basename(path)
    filename, ext = os.path.splitext(base)
    filename_components = filename.split('_')
    if len(filename_components) == 9:            
        metadata = {
                       'filename': filename,
                       'filetype': ext,
                       'recording_end_date': filename_components[0],
                       'vcr_index': filename_components[4]
                    }
    else:
        print('corrupted filename: {}'.format(filename))
        # corrupted file name
        metadata = None
    return metadata

def load_files(root_path, file_extension='txt3', recursive_search=False):
    if not file_extension in ['txt3', 'cuts']:
        raise Exception('UnsupportedDataType')

    if root_path.endswith(file_extension):
        if file_extension == 'txt3':
            yield _load_single_caption_file(root_path)
        else:
            # TODO: caption filwee
            yield _load_single_program_boundary_file(root_path)
    else:
        if not root_path.endswith('/'):
            root_path += '/'        
        root_path += '**/*.{}'.format(file_extension)

        filepaths = glob.iglob(root_path, recursive=recursive_search)
        if file_extension == 'txt3':        
            for path in filepaths:
                yield _load_single_caption_file(path)
        else:                
            for path in filepaths:
                yield _load_single_program_boundary_file(path)


def load_caption_files(root_path, recursive_search=False):
    '''[summary]
    
    [description]
    
    Returns:
        [description]
        [type]
    '''
    return load_files(root_path, file_extension='txt3', recursive_search=True)


def load_program_boundary_files(root_path, recursive_search=False):
    '''[summary]
    
    [description]
    
    Returns:
        [description]
        [type]
    '''
    return load_files(root_path, file_extension='cuts', recursive_search=True)


def find_y_path_from_X_filename(X_filename, y_filetype, search_root_path):    
    pattern = '{}/**/{}.{}'.format(search_root_path, X_filename, y_filetype)
    paths = glob.glob(pattern, recursive=True)
    
    if len(paths) > 1:
        print('duplicate files with matching caption filename')
    return paths[0]


def split_video_to_clips(start_time, end_time, interval):
    pass

def split_audio_to_clips(start_time, end_time, interval):
    pass

def split_caption_to_X(caption, interval=10):
    '''[summary]
    
    [description]
    
    Args:
        caption: [consists of lines]
        interval: [seconds] (default: {10})
    
    Returns:
        [description]
        [type]
    '''
    freq = '{}s'.format(interval)
    grouper = pd.Grouper(key='t_start',freq=freq)
    grouped = caption.groupby(grouper)
    def _combine_rows(X):
        # TODO: cleanse any unnecessary string in caption
        params = dict(caption=' '.join(X['caption'])) 
        return pd.Series(params)        
    
    X = grouped.apply(_combine_rows)
    X['t_start'] = X.index
    X = X[['t_start', 'caption']]
    X.reset_index(drop=True, inplace=True)
    return X


def convert_program_boundaries_to_y(program_boundaries, X, interval=10):    
    y = pd.DataFrame(X['t_start'], columns=['t_start'])
    y['is_program_boundary'] = False
        
    interval = np.timedelta64(interval, 's')
    # TODO: try a vectorized solution later on  
    for _, row in program_boundaries.iterrows():
        pb = row['t_program_boundary']
        mask = ((y['t_start']) <= pb) & (pb < (y['t_start'] + interval))
        y['is_program_boundary'] = y['is_program_boundary'] | mask
    
    return y['is_program_boundary']  