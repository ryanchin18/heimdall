from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1
from sklearn.ensemble import RandomForestClassifier
import cPickle as pickle
import numpy as np


def generate_classifiers():
    td = np.load("/home/grainier/GitProjects/orion-ids/scripts/training_sets/training_data.npy")

    # whole training data set
    x = td[:, :11]
    y = td[:, 11]

    # ----------- Fix Class Imbalance ----------- #
    OS = OverSampler(random_state=1)
    ox, oy = OS.fit_transform(x, y)

    smote = SMOTE(random_state=1)
    sx, sy = smote.fit_transform(x, y)

    bsmote = bSMOTE1(random_state=1)
    bsx1, bsy1 = bsmote.fit_transform(x, y)

    # ----------- Generate Classifiers ----------- #
    os_clf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    os_clf.fit(ox, oy)

    smote_clf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    smote_clf.fit(sx, sy)

    bsmote_clf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    bsmote_clf.fit(bsx1, bsy1)

    # ----------- Dump Classifiers ----------- #
    pickle.dump(os_clf, open('os_clf.pkl', 'wb'))
    pickle.dump(smote_clf, open('smote_clf.pkl', 'wb'))
    pickle.dump(bsmote_clf,  open('bsmote_clf.pkl', 'wb'))

if __name__ == '__main__':
    generate_classifiers()

