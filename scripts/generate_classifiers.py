from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1
from sklearn.ensemble import RandomForestClassifier
from common import root_dir
import cPickle as pickle
import numpy as np
import os


def generate_classifiers():
    path = os.path.join(root_dir, "generated")
    td = np.load(os.path.join(path, "training_data", "training_data.npy"))

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
    pickle.dump(os_clf, open(os.path.join(path, "classifiers", 'os_clf.pkl'), 'wb'))
    pickle.dump(smote_clf, open(os.path.join(path, "classifiers", 'smote_clf.pkl'), 'wb'))
    pickle.dump(bsmote_clf,  open(os.path.join(path, "classifiers", 'bsmote_clf.pkl'), 'wb'))

if __name__ == '__main__':
    generate_classifiers()

