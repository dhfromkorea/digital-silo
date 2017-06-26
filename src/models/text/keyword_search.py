import re
import numpy as np

class KeywordSearch(object):
    '''[summary]
    
    Todos:
        apply minimum program length
        apply minimum time window
        to merge cuts that are close to one another
    [description]
    '''
    def __init__(self):
        super(KeywordSearch, self).__init__()

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


    def predict(self, dataframe, keywords, merge_time_window=0):
        '''[summary]
        
        [description]
        
        Args:
            dataframe: [description]
            keywords: [description]
            merge_time_window: [merge time window in minutes] (default: {0})
        
        Returns:
            [description]
            [type]
        '''
        pattern = r'|'.join(keywords)
        is_matched =  dataframe['caption'].str.contains(pattern, flags=re.IGNORECASE)
        matched_lines = dataframe[is_matched]

        if merge_time_window > 0:
            matched_lines = self._merge_matches(matched_lines, merge_time_window)
        
        return dataframe.iloc[matched_lines.index]