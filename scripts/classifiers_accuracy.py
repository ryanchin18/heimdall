from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1
from sklearn.ensemble import RandomForestClassifier
from common import root_dir
import numpy as np
import os
TRAINING_SIZE = 500


def classifiers_accuracy():
    path = os.path.join(root_dir, "generated")
    td = np.load(os.path.join(path, "training_data", "training_data.npy"))

    # ----------- Data set separation ----------- #
    # whole set
    rec_len = len(td[:, :][0]) - 1  # in index (starting from 0)
    data_x = td[:, :rec_len]
    data_y = td[:, rec_len]

    # training set
    x = data_x[:-TRAINING_SIZE]
    y = data_y[:-TRAINING_SIZE]

    # testing set
    t_x = data_x[-TRAINING_SIZE:]
    t_y = data_y[-TRAINING_SIZE:]

    # ----------- Fix Class Imbalance ----------- #
    OS = OverSampler(random_state=1)
    ox, oy = OS.fit_transform(x, y)

    smote = SMOTE(random_state=1)
    sx, sy = smote.fit_transform(x, y)

    bsmote1 = bSMOTE1(random_state=1)
    bsx1, bsy1 = bsmote1.fit_transform(x, y)

    # ----------- Train and Predict  ----------- #
    # predict() will just say whether it's a attack,
    # but predict_proba() will say the probability (this is important)

    # Over Sampler data
    clf_1 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_1.fit(ox, oy)
    p_1 = clf_1.predict_proba(t_x)
    # print("p_1 : ", p_1)

    # SMOTE data
    clf_2 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_2.fit(sx, sy)
    p_2 = clf_2.predict_proba(t_x)
    # print("p_2: ", p_2)

    # BSMOTE data
    clf_3 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_3.fit(bsx1, bsy1)
    p_3 = clf_3.predict_proba(t_x)
    # print("p_3 : ", p_3)

    print "{0} \t{1} \t\t{2} \t{3}".format("actual", "os", "smote", "bsmote")
    for i in range(0, TRAINING_SIZE):
        a = t_y[i]
        o = p_1[i][1]
        s = p_2[i][1]
        b = p_3[i][1]
        if a != 0. or o != 0. or s != 0. or b != 0.:
            print "{0} \t{1} \t{2} \t{3}".format(a, o, s, b)
        pass

if __name__ == '__main__':
    classifiers_accuracy()

