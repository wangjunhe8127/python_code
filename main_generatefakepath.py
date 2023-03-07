from reasign_points import reasign_points
from change_local import to_local_coordinates
from generate_boundary import generate_boundary
import os
import sys
import numpy as np
import bisect
import math
# 将当前目录的上级目录的上级目录添加到搜索路径中，也就是可以在code_bases下查找
sys.path.append("/data/megvii/pilot")
from happypilot.config.config_mpc import V_KM, T_IDXS,IDX_N
from tool_plot import plot_common

def generate_accumlate(origin_c, origin_l, origin_r):
    origin_c = np.array(origin_c)
    origin_l = np.array(origin_l)
    origin_r = np.array(origin_r)
    # 计算accumlate_s
    pre_c = origin_c[1:]
    back_c = origin_c[:-1]
    delta = back_c - pre_c
    delta_norm = np.linalg.norm(delta, axis=1)
    accumlate_s_array = np.cumsum(delta_norm).tolist()
    accumlate_s_array.insert(0, 0)
    return accumlate_s_array

# 按照设定的T_array找到对应accumlate_s的c，l，r


def get_infer(accumlate_s, c, l, r, v, t_array):
    c = np.array([c[i].tolist() for i in range(len(c))])
    x1 = v * np.array(t_array)
    x2 = np.array(accumlate_s)
    idx_arr = [bisect.bisect(x2, point) for point in x1]
    new_c = [c[i].tolist() for i in idx_arr]
    new_l = [l[i].tolist() for i in idx_arr]
    new_r = [r[i].tolist() for i in idx_arr]
    return new_c, new_l, new_r


def generate_ref_pose(c):
    return np.array(c)[:, 0], np.array(c)[:, 1]

def generate_ref_heading(c):
    res = [math.atan2((c[i][1] - c[i-1][1]), (c[i][0]-c[i-1][0]))
           for i in range(1, len(c), 1)]
    res.insert(0, 0)
    return res

# 首先计算每个点的x，y，heading
# 然后得到根据时间差值的每个点的新的x，y，heading
# 时间差值为通过不同的t*v得到每个mpc点对应的距离，然后取最近的point点作为参考点


def generate_core(points, pointsl, pointsr):
    acc = generate_accumlate(points, pointsl, pointsr)
    new_c, _, _ = get_infer(acc, points, pointsl,
                            pointsr, v=V_KM, t_array=T_IDXS)
    x_ref, y_ref = generate_ref_pose(new_c)
    heading_ref = generate_ref_heading(new_c)
    init_alpha = 0.0
    params_ego_v = 8.0/3.6
    L = 3.5
    init_state = np.array([x_ref[0], y_ref[0], heading_ref[0], init_alpha])
    params = np.array([params_ego_v, L] * IDX_N).reshape(IDX_N,-1)
    ref = [np.array(y_ref).reshape(IDX_N,), np.array(heading_ref).reshape(IDX_N,)]
    return [init_state, params, ref, new_c]

def generate_mpc_input():
    from path_point import points
    points, pointsl, pointsr = generate_boundary(points, l=1.5, r=2.0)
    new_c, new_l, new_r = to_local_coordinates(center=points, left=pointsl, right=pointsr)
    res = generate_core(new_c, new_l, new_r)
    return res

if __name__ == "__main__":
    input = generate_mpc_input()
    plot_common([input[3]])
    

