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
    new_l = [l[i] for i in idx_arr]
    new_r = [r[i] for i in idx_arr]
    return new_c, new_l, new_r


def generate_ref_pose(c):
    return np.array(c)[:, 0], np.array(c)[:, 1]

def obtain_theta_from_points():
    past_theta = math.pi/2
    def step(poi2, poi1):
        nonlocal past_theta
        dx = poi2[0] - poi1[0]
        dy = poi2[1] - poi1[1]
        if abs(dx) < 1e-6 or abs(dy) < 1e-6:
            if abs(dx)<1e-6:
                if abs(dy) > 1e-6:
                    theta = math.pi/2 if dy >0 else -math.pi/2
                else:
                    theta = past_theta
            else:
                theta = 0 if dx >0 else math.pi
        else:
            theta = math.atan2(dy,dx)
        past_theta = theta
        return theta
    return step

def generate_ref_heading(c):
    obtain = obtain_theta_from_points()
    res = [(lambda i:obtain(c[i],c[i-1]) if obtain(c[i],c[i-1])>0 else 2*math.pi+obtain(c[i],c[i-1]))(i) for i in range(1, len(c), 1)] 
    res.insert(0, res[0])
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
    L = 2.8
    init_state = np.array([x_ref[0], y_ref[0], heading_ref[0], init_alpha])
    params = np.array([params_ego_v, L] * IDX_N).reshape(IDX_N,-1)
    ref = [np.array(x_ref).reshape(IDX_N,), np.array(y_ref).reshape(IDX_N,), np.array(heading_ref).reshape(IDX_N,)]
    return [init_state, params, ref, new_c]

def cut_points(points, pointsl, pointsr,idx):
    new_points = points[idx:]
    new_l = pointsl[idx:]
    new_r = pointsr[idx:]
    return new_points, new_l, new_r

def generate_mpc_input(idx=0, load_mode = 0):
    if load_mode==0:
        from path_point import points
    elif load_mode==1:
        from load_csv import load_csv
        points = np.array(load_csv()[2:4]).transpose()
    points, pointsl, pointsr = generate_boundary(points, l=1.5, r=2.0)
    points, pointsl, pointsr = cut_points(points, pointsl, pointsr, idx)
        # new_c, new_l, new_r = to_local_coordinates(center=points, left=pointsl, right=pointsr)
    res = generate_core(points, pointsl, pointsr)
    return res

if __name__ == "__main__":
    input = generate_mpc_input()
    plot_common([input[3]])
    

