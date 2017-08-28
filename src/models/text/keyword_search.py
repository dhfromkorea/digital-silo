import numpy as np
import re
from src.utilities.data_utils import *
from src.utilities.metrics import *


class KeywordSearch(object):
    '''[summary]
    
    [description]
    '''
    def __init__(self, keywords=['caption']):
        super(KeywordSearch, self).__init__()
        self._keywords = keywords

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, keywords=[]):
        self._keywords = keywords

    def test(self, path_X, path_y=None):
        return accuracy_score_f1(self, path_X, path_y)

    def predict(self, X, padding=False):
        '''[summary]
        
        [description]
        
        Args:
            X: [description]
            keywords: [description]
        
        Returns:
            [description]
            [type]
        '''

        pattern = r'|'.join(self.keywords)
        is_matched =  X['caption'].str.contains(pattern, flags=re.IGNORECASE)
        #TODO: change the word spray to something smarter
        #as if we spray the neighboring points around the matched point 
        if padding:    
            is_matched_padded = is_matched.copy()
            PADDING = 18 # 3 minutes (plus/minus i)
            for i, row in is_matched.iteritems():
                if row:
                    start = i - PADDING if i > PADDING else 0
                    end = i + PADDING
                    is_matched_padded[start:end] = True

            is_matched = is_matched_padded
        return is_matched