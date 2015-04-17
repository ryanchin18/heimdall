from __future__ import division
from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt

s = {
  "lines.linewidth": 2.0,
  "examples.download": True,
  "patch.linewidth": 0.5,
  "legend.fancybox": True,
  "axes.color_cycle": [
    "#30a2da",
    "#fc4f30",
    "#e5ae38",
    "#6d904f",
    "#8b8b8b"
  ],
  "axes.facecolor": "#f0f0f0",
  "axes.labelsize": "large",
  "axes.axisbelow": True,
  "axes.grid": True,
  "patch.edgecolor": "#f0f0f0",
  "axes.titlesize": "x-large",
  "svg.embed_char_paths": "path",
  "examples.directory": "",
  "figure.facecolor": "#f0f0f0",
  "grid.linestyle": "-",
  "grid.linewidth": 1.0,
  "grid.color": "#cbcbcb",
  "axes.edgecolor":"#f0f0f0",
  "xtick.major.size": 0,
  "xtick.minor.size": 0,
  "ytick.major.size": 0,
  "ytick.minor.size": 0,
  "axes.linewidth": 3.0,
  "font.size":14.0,
  "lines.linewidth": 4,
  "lines.solid_capstyle": "butt",
  "savefig.edgecolor": "#f0f0f0",
  "savefig.facecolor": "#f0f0f0",
  "figure.subplot.left"    : 0.08,
  "figure.subplot.right"   : 0.95,
  "figure.subplot.bottom"  : 0.07
}

def vizualization():

    import numpy as np
    td = np.load("/home/grainier/GitProjects/orion-ids/tools/training_sets/training_data.npy")

    # x = td[:, :11]
    # y = td[:, 11]

    # whole set
    data_x = td[:, :11]
    data_y = td[:, 11]

    # training set
    x = data_x[:-500]
    y = data_y[:-500]

    # testing set
    t_x = data_x[-500:]
    t_y = data_y[-500:]

    print(t_y)


    from tools.unbalanced_dataset import OverSampler, SMOTE, bSMOTE1


    # -------------------------------- // -------------------------------- #
    # Datasets
    OS = OverSampler(random_state=1)
    ox, oy = OS.fit_transform(x, y)

    smote = SMOTE(random_state=1)
    sx, sy = smote.fit_transform(x, y)

    bsmote1 = bSMOTE1(random_state=1)
    bsx1, bsy1 = bsmote1.fit_transform(x, y)

    # -------------------------------- // -------------------------------- #
    # Random Forest Classifiers
    from sklearn.ensemble import RandomForestClassifier

    # predict will just say whether it's a attack, but predict_proba will say the probability (this is important)

    # oversampler data
    clf_1 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_1.fit(ox, oy)
    p_1 = clf_1.predict_proba(t_x)
    print("p_1 : ", p_1)

    # smote data
    clf_2 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_2.fit(sx, sy)
    p_2 = clf_2.predict_proba(t_x)
    print("p_2: ", p_2)

    # bsmote 1 data
    clf_3 = RandomForestClassifier(n_estimators=100, n_jobs=2)
    clf_3.fit(bsx1, bsy1)
    p_3 = clf_3.predict_proba(t_x)
    print("p_3 : ", p_3)

    # importance
    importances = clf_1.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf_1.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(10):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importance of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(11), importances[indices], color="r", yerr=std[indices], align="center")
    plt.xticks(range(11), indices)
    plt.xlim([-1, 11])
    plt.show()

    # -------------------------------- // -------------------------------- #
    # PCA
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)

    x = pca.fit_transform(x)
    ox = pca.transform(ox)
    sx = pca.transform(sx)
    bsx1 = pca.transform(bsx1)

    # -------------------------------- // -------------------------------- #
    # Visualization
    matplotlib.rcParams.update(s)
    # f, ax = plt.subplots(2, 3, figsize=(16, 9))
    # f.suptitle("Over-sampling with SMOTE: comparison", fontsize=16)
    #
    # for e, c in zip(set(y), ['purple', 'g']):
    #     ax[0, 0].scatter(x[y==e, 0], x[y==e, 1], color = c, alpha = 0.5)
    # ax[0, 0].set_title('Original', fontsize=12)
    #
    # for e, c in zip(set(y), ['purple', 'g']):
    #     ax[0, 1].scatter(x[y==e, 0], x[y==e, 1], color = c, alpha = 0.5)
    # ax[0, 1].scatter(ox[-new:, 0], ox[-new:, 1], color = 'y', alpha = 0.3)
    # ax[0, 1].set_title('Random Over-sampling', fontsize=12)
    #
    #
    # for e, c in zip(set(y), ['purple', 'g']):
    #     ax[0, 2].scatter(x[y==e, 0], x[y==e, 1], color = c, alpha = 0.5)
    # ax[0, 2].scatter(sx[-new:, 0], sx[-new:, 1], color = 'y', alpha = 0.3)
    # ax[0, 2].set_title('SMOTE', fontsize=12)
    #
    #
    # for e, c in zip(set(y), ['purple', 'g']):
    #     ax[1, 0].scatter(x[y==e, 0], x[y==e, 1], color = c, alpha = 0.5)
    # ax[1, 0].scatter(bsx1[-new:, 0], bsx1[-new:, 1], color = 'y', alpha = 0.3)
    # ax[1, 0].set_title('Borderline-SMOTE type 1', fontsize=12)
    #
    # for e, c in zip(set(y), ['purple', 'g']):
    #     ax[1, 1].scatter(x[y==e, 0], x[y==e, 1], color = c, alpha = 0.5)
    # ax[1, 1].scatter(bsx2[-new:, 0], bsx2[-new:, 1], color = 'y', alpha = 0.3)
    # ax[1, 1].set_title('Borderline-SMOTE type 2', fontsize=12)
    #
    # # Hide ticks
    # plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)
    # plt.setp([a.get_yticklabels() for a in ax[:, 1]], visible=False)
    # plt.setp([a.get_yticklabels() for a in ax[:, 2]], visible=False)
    #
    # plt.show()

if __name__ == '__main__':

    vizualization()

