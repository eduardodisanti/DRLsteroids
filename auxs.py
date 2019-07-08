import numpy as np

def flatten_tensor(t, size):

    _t = np.array(t).reshape(1, size)

    return _t