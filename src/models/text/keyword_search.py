import re

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

    def _merge_matches(self, matched_lines, deltas, min_merge_delta):
        return matched_lines

    def predict(self, dataframe, keywords, min_merge_delta=0):
        pattern = r'|'.join(keywords)
        matched_lines =  dataframe['caption'].str.contains(pattern, flags=re.IGNORECASE)
        deltas = dataframe[matched_lines]['mid'].diff()
        matched_lines_merged = self._merge_matches(matched_lines, deltas, min_merge_delta)
        return matched_lines_merged
