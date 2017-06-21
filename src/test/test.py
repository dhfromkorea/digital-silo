import sys, os.path
sys.path.append(os.path.abspath('../'))

import unittest

from models.text.keyword_search import KeywordSearch
from utilities.data_utils import *

class KeywordSearchModelTest(unittest.TestCase):
    def setUp(self):
        self.dataframe = ''

    def test_find_row_indices_that_contain_keywords(self):
        
        self.assertEqual('df', '')


class DataUtilTest(unittest.TestCase):
    def setUp(self):
        self.dataframe = ''

    def test_load_single_caption_data(self):    
        self.assertEqual('df', '')

    def test_load_multiple_caption_data(self):    
        self.assertEqual('df', '')

    def test_load_single_cut_data(self):    
        self.assertEqual('df', '')

    def test_load_multiple_cut_data(self):    
        self.assertEqual('df', '')

if __name__ == '__main__':
    unittest.main()
