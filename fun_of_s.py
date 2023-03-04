import numpy as np
def get_s_xy(points):
    if len(points)==1:
        return np.array([points[0],points[1],1])
    pre = points[1:]
    back = points[:-1]
    delta = back-pre
    
    