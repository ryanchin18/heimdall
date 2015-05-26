"""

"""
from common import root_dir
import cPickle as pickle
import os


class RFClassifier(object):
    def __init__(self):
        self.path = os.path.join(root_dir, "generated", "classifiers")
        self._clf = None
        pass

    def load(self, balanced_type='os'):
        if balanced_type == 'smote':
            self._clf = pickle.load(open(os.path.join(self.path, 'smote_clf.pkl'), 'rb'))
        elif balanced_type == 'bsmote':
            self._clf = pickle.load(open(os.path.join(self.path, 'bsmote_clf.pkl'), 'rb'))
        else:
            self._clf = pickle.load(open(os.path.join(self.path, 'os_clf.pkl'), 'rb'))
        pass

    def save(self):
        # TODO
        pass

    def train(self, data):
        # TODO
        pass

    def analyse(self, record):
        # [0, 0] represents normal, [0, 1] represents DDoS
        analysis = self._clf.predict_proba(record)
        probability = analysis[0, 1]
        is_ddos = True if probability >= 0.5 else False
        return probability * 100.0, is_ddos
        pass

    pass