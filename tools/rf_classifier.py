"""

"""
import cPickle as pickle


class RFClassifier(object):
    def __init__(self):
        self._clf = None
        pass

    def load(self, balanced_type='os'):
        if balanced_type == 'smote':
            self._clf = pickle.load(open('trained_classifiers/smote_clf.pkl', 'rb'))
        elif balanced_type == 'bsmote':
            self._clf = pickle.load(open('trained_classifiers/bsmote_clf.pkl', 'rb'))
        else:
            self._clf = pickle.load(open('trained_classifiers/os_clf.pkl', 'rb'))
        pass

    def save(self):
        pass

    def train(self, data):
        pass

    def analyse(self, record):
        # [0, 0] represents normal, [0, 1] represents DDoS
        analysis = self._clf.predict_proba(record)
        probability = analysis[0, 1]
        is_ddos = True if probability >= 0.5 else False
        return probability, is_ddos
        pass

    pass