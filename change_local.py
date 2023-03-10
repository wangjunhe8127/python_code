import numpy as np
from tool_plot import plot_common 
def to_local_coordinates(center, left, right):
    origin = center[0]
    x_axis = (center[1] - center[0]) / np.linalg.norm(center[1] - center[0]) #初始方向
    y_axis = np.array([x_axis[1], -x_axis[0]])
    rotation_matrix = np.vstack((x_axis, y_axis)).T
    center_local = np.dot(rotation_matrix, (center - origin).T).T
    left_local = np.dot(rotation_matrix, (left - origin).T).T
    right_local = np.dot(rotation_matrix, (right - origin).T).T
    return center_local,left_local,right_local