import numpy as np
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

from src.utilities.data_utils import *
from src.utilities.metrics import *


class Lda(object):
    '''[summary]
    
    [description]
    '''
    def __init__(self, num_features=1000, num_topics=50):
        super(Lda, self).__init__()
        self.num_features = num_features
        self.num_topics = num_topics
        self.model = LatentDirichletAllocation(n_topics=num_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0)
        self.tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=num_features, stop_words='english')
        self.feature_names = tf_vectorizer.get_feature_names()
    

    def train(self, path_X):        
        caption_files = load_caption_files(path_X)
        # TODO: consider partial fit if this takes too much time
        X_datasets = []
        for caption_file in caption_files:
            caption, metadata = caption_file
            X = split_caption_to_X(caption)            
            X_datasets.append(X)

        self.X = pd.concat(X_datasets)['caption'].tolist()
        
        tf = self.tf_vectorizer.fit_transform(self.X)
        lda = LatentDirichletAllocation(n_topics=self.num_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0)
        lda = lda.fit(tf)


    def test(self, path_X, path_y=None):
        return accuracy_score_f1(self, path_X, path_y)

    def predict(self, X):
        return X

    def display_topics(self, num_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic {}".format(topic_idx))
            print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))


class NMF(object):
    """docstring for NMF"""
    def __init__(self, arg):
        super(NMF, self).__init__()
        self.arg = arg
        