from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1
from sklearn.ensemble import RandomForestClassifier
from common import root_dir
import cPickle as pickle
import numpy as np
import time
import os


def generate_classifiers():
    path = os.path.join(root_dir, "generated")
    td = np.load(os.path.join(path, "training_data", "training_data.npy"))

    # whole training data set
    rec_len = len(td[:, :][0]) - 1  # in index (starting from 0)
    x = td[:, :rec_len]
    y = td[:, rec_len]

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
    pickle.dump(os_clf, open(os.path.join(path, "classifiers", 'os_clf_{}.pkl'.format(time.strftime("%Y_%m_%d_%H:%M"))), 'wb'))
    pickle.dump(smote_clf, open(os.path.join(path, "classifiers", 'smote_clf_{}.pkl'.format(time.strftime("%Y_%m_%d_%H:%M"))), 'wb'))
    pickle.dump(bsmote_clf,  open(os.path.join(path, "classifiers", 'bsmote_clf_{}.pkl'.format(time.strftime("%Y_%m_%d_%H:%M"))), 'wb'))

if __name__ == '__main__':
    generate_classifiers()

