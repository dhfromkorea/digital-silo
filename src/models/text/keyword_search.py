#!/usr/bin/env python3

import re

class KeywordSearch(object):
    """docstring for KeywordSearch"""
    def __init__(self):
        super(KeywordSearch, self).__init__()

    def predict(self, dataframe, *args):
        pattern = r'|'.join(args)
        indices =  dataframe['caption'].str.contains(pattern, flags=re.IGNORECASE)
        return indices
