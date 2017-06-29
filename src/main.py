#!/usr/bin/env python3

'''
run this script at src/
python main.py

terminologies
    shot ->(A) scene ->(B) story/commercial ->(C) program ->(D) video
    below are cuts or boundaries, or transitions
    A = shot cuts
    B = scene cuts
    C = story cuts (or commercial)
    D = program cut

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
    print(f1_score)

if __name__ == "__main__":
    main()
