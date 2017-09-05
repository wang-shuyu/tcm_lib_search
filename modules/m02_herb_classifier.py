#encoding=utf-8
import pandas as pd
import sklearn
from sklearn import linear_model, preprocessing, neighbors, svm
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import feature_selection
# import pickle

class numeric_column_selector(BaseEstimator, TransformerMixin):
    def __init__(self, columns = ['pos_flag_pre', 'pos_flag_curr', 'pos_flag_next', 'label']):
        self.columns = columns

    def fit(self, x, y = None):
        return self

    def transform(self, x):
        return x.as_matrix(columns = [c for  c in list(x.columns.values) if c not in self.columns])

class pos_column_selector(BaseEstimator, TransformerMixin):
    def __init__(self, columns = ['pos_flag_pre', 'pos_flag_curr', 'pos_flag_next']):
        self.columns = columns

    def fit(self, x, y = None):
        return self

    def transform(self, x):
        return x.as_matrix(columns = self.columns)

class pos_label_encoder(preprocessing.LabelEncoder):
    def fit(self, x, y = None):
        super(pos_label_encoder, self).fit(x.flatten())
        return self

    def fit_transform(self, x, y = None):
        return super(pos_label_encoder, self).fit(x.flatten()).transform(x)

class pos_label_onehot_encoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.label_encoder = preprocessing.OneHotEncoder(sparse=False)

    def fit(self, x, y = None):
        self.label_encoder.fit(x)

    def transform(self, x):
        return self.label_encoder.transform(x)

    def fit_transform(self, x, y = None):
        return self.label_encoder.fit_transform(x)
