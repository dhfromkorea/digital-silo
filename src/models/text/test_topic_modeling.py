import unittest
import numpy as np
import random
import glob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# from src.models.text.lda import *
from src.utilities.data_utils import *


class TestLda(unittest.TestCase):    
    def setUp(self):
        search_path = 'test_data/'
        caption_files = load_caption_files(search_path)
        X_datasets = []
        for caption_file in caption_files:
            caption, metadata = caption_file
            X = split_caption_to_X(caption)            
            X_datasets.append(X)
        self.documents = pd.concat(X_datasets)['caption'].tolist()
        self.num_features = 1000
        self.num_topics = 20

    def test_train_lda(self):
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=self.num_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(self.documents)
        tf_feature_names = tf_vectorizer.get_feature_names()
        lda = LatentDirichletAllocation(n_topics=self.num_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0)
        lda = lda.fit(tf)
        
        def display_topics(model, feature_names, no_top_words):
            for topic_idx, topic in enumerate(model.components_):
                print("Topic {}".format(topic_idx))
                print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

        no_top_words = 10
        display_topics(lda, tf_feature_names, no_top_words)         
        # checkout https://stackoverflow.com/questions/31107945/how-to-perform-prediction-with-lda-linear-discriminant-in-scikit-learn
    
    def test_predict_lda(self):
        pass
    
class TestNMF(object):
    """docstring for TestNMF"""
    def __init__(self, arg):
        super(TestNMF, self).__init__()
        self.arg = arg

if __name__ == '__main__':
    # TODO: is this the right thing todo ?
    unittest.main()
