#!/usr/bin/env python3

'''
run this script at src/
python main.py

terminologies
    shot ->(A) scene ->(B) story/commercial ->(C) program ->(D) video
    below are boundaries or boundaries, or transitions
    A = shot boundaries
    B = scene boundaries
    C = story boundaries (or commercial)
    D = program boundaries

'''

import sys
sys.path.insert(0, '../')
import random
import glob
from src.models.text import keyword_search as ks
from src.utilities.data_utils import *

import datetime
#TEST_DATA_PATH = 'test_data/'
TEST_DATA_PATH = '../tmp/2006/2006-06/'


def try_keyword_search():
    # train here
    keywords = ['Type=Commercial','Type=Story']
    model = ks.KeywordSearch(keywords)
    # validate to tune hyperparams here
    
    # test here
    f1_score= model.test(TEST_DATA_PATH)

def check_story_boundaries():
    search_path = TEST_DATA_PATH +'.txt3'
    X_paths = glob.glob(search_path)
    file_path = random.choice(X_paths)
    captions = load_caption_files(file_path, keep_story_boundary=True)                
    caption, metadata = next(captions)

    is_story_boundary = caption['caption'].str.contains('type=', flags=re.IGNORECASE) 

    t_sb = caption[is_story_boundary]['t_start']

    y_path = find_y_path_from_X_filename(metadata['filename'], TEST_DATA_PATH)
    pb_files = load_program_boundary_files(y_path)                
    pb, _ = next(pb_files)

    t_pb = pb['t_program_boundary']
    
    def find_nearest_date(dates, compared_to):
        return min(dates, key=lambda x: abs(x - compared_to))

    min_deltas = []
    for pb in t_pb:
        sb = find_nearest_date(t_sb, pb)
        md = (pb - sb) if (pb > sb) else (sb - pb) 
        min_deltas.append(md)
        print(md)
    print(metadata['filename'])
    print(sum(min_deltas, datetime.timedelta())/len(min_deltas))

def main():
    try_keyword_search()
    #check_story_boundaries()

if __name__ == "__main__":
    main()
