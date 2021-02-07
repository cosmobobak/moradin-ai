import numpy as np

def convert_int(i):
    width = 9  # 8bit width
    return [int(x) for x in '{:0{size}b}'.format(i, size=width)]


def serialize_state(state):
    x = np.array(convert_int(state.node[0]))
    o = np.array(convert_int(state.node[1]))
    x = x.reshape((3, 3))
    o = o.reshape((3, 3))
    return np.array([x, o])
