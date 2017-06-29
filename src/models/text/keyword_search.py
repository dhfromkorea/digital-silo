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

    def test(self, root_path_captions, root_path_cuts=None):
        return accuracy_score_f1(self, root_path_captions, root_path_cuts)

    def predict(self, X):
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
        return is_matched.reset_index(drop=True)