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

from models.text import keyword_search as ks

def main():
    # train here
    keywords = ['caption', 'story', 'commercial']
    model = ks.KeywordSearch(keywords)
    # validate to tune hyperparams here
    
    # test here
    f1_score= model.test('test_data/')

if __name__ == "__main__":
    main()
