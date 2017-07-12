import numpy as np
import re
from src.utilities.data_utils import *
from src.utilities.metrics import *


class Lda(object):
    '''[summary]
    
    [description]
    '''
    def __init__(self):
        super(Lda, self).__init__()

    def test(self, path_X, path_y=None):
        return accuracy_score_f1(self, path_X, path_y)

    def predict(self, X):
        return X