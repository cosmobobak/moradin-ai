import numpy as np

def convert_int(i):
    width = 9  # 8bit width
    return [int(x) for x in '{:0{size}b}'.format(i, size=width)]


def vec_state(state):
    x = np.array(convert_int(state.node[0]))
    o = np.array(convert_int(state.node[1]))
    x = x.reshape((3, 3))
    o = o.reshape((3, 3))
    return np.array([x, o])

def maxpos(l):
    p = 0
    b = l[0]
    for i, v in enumerate(l):
        if v > b:
            b, p = v, i
    return p

def devec_action(actionVec):
    return maxpos(actionVec)