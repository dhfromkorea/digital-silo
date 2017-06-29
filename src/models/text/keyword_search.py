import numpy as np
import re
from src.utilities.data_utils import *
from src.utilities.metrics import *


class KeywordSearch(object):
    '''[summary]
    
    [description]
    '''
    def __init__(self, keywords=['caption'], merge_time_window=0):
        super(KeywordSearch, self).__init__()
        self._merge_time_window = merge_time_window
        self._keywords = keywords

    def _merge_matches(self, matched_lines, merge_time_window):
        # TODO: this is costly. we should improve this later
        min_delta = np.timedelta64(merge_time_window, 'm')
        # the original row index does not 
        merged = matched_lines.copy()

        for i, row in matched_lines.iterrows():
            cur_match_time = row['mid']

            if i == matched_lines.index[0]:
                last_match_time = cur_match_time                 
            elif (cur_match_time - last_match_time) <= min_delta:
                merged = merged.drop(i)
            else:
                last_match_time = cur_match_time            
        return merged

    @property
    def merge_time_window(self):
        return self._merge_time_window

    @merge_time_window.setter
    def merge_time_window(self, num_minutes):
        self._merge_time_window = num_minutes

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
            merge_time_window: [merge time window in minutes] (default: {0})
        
        Returns:
            [description]
            [type]
        '''
        pattern = r'|'.join(self.keywords)
        is_matched =  X['caption'].str.contains(pattern, flags=re.IGNORECASE)
        matched_lines = X[is_matched]

        # if self.merge_time_window > 0:
        #     matched_lines = self._merge_matches(matched_lines, self.merge_time_window)
        # return X.iloc[matched_lines.index]
        return matched_lines