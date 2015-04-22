from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from common import root_dir
import numpy as np
import os


def feature_importance():
    path = os.path.join(root_dir, "generated")
    td = np.load(os.path.join(path, "training_data", "training_data.npy"))

    # ----------- Data set separation ----------- #
    # whole set
    rec_len = len(td[:, :][0]) - 1  # in index (starting from 0)
    x = td[:, :rec_len]
    y = td[:, rec_len]

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

    # Over Sampler data (Uncomment as required)
    clf_1 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_1.fit(ox, oy)
    importance = clf_1.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf_1.estimators_], axis=0)
    indices = np.argsort(importance)[::-1]

    # SMOTE data (Uncomment as required)
    # clf_2 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    # clf_2.fit(sx, sy)
    # importance = clf_2.feature_importances_
    # std = np.std([tree.feature_importances_ for tree in clf_2.estimators_], axis=0)
    # indices = np.argsort(importance)[::-1]

    # BSMOTE data (Uncomment as required)
    # clf_3 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    # clf_3.fit(bsx1, bsy1)
    # importance = clf_3.feature_importances_
    # std = np.std([tree.feature_importances_ for tree in clf_3.estimators_], axis=0)
    # indices = np.argsort(importance)[::-1]

    # Print the feature ranking
    print "Feature ranking: "
    for f in range(rec_len):
        print "%d. feature %d (%f)" % (f + 1, indices[f], importance[indices[f]])

    # Plot the feature importance of the forest
    plt.figure()
    plt.title("Feature importance")
    plt.bar(range(rec_len), importance[indices], color="r", yerr=std[indices], align="center")
    plt.xticks(range(rec_len), indices)
    plt.xlim([-1, rec_len])
    plt.show()

if __name__ == '__main__':
    feature_importance()

