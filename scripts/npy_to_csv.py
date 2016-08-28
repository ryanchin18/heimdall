import time

import numpy as np
import os
from common import root_dir


def npy_to_csv():
    path = os.path.join(root_dir, "generated")
    td = np.load(os.path.join(path, "training_data", "training_data.npy"))
    np.savetxt(
        os.path.join(path, "training_data", "training_data_from_npy_{0}.csv".format(time.strftime("%Y_%m_%d_%H:%M"))),
        td, delimiter=",")


if __name__ == '__main__':
    npy_to_csv()
