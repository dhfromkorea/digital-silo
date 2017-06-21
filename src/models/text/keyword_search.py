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

    def predict(self, dataframe, *args):
        '''[summary]
        
        [description]
        
        Args:
            dataframe: [description]
            *args: [description]
        
        Returns:
            [description]
            [type]
        '''
        pattern = r'|'.join(args)
        indices =  dataframe['caption'].str.contains(pattern, flags=re.IGNORECASE)
        return indices
