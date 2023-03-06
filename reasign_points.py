import numpy as np
def reasign_points(T_IDXS, origin_c=None, origin_l=None, origin_r=None, v_km=5.0/3.6, T = 5):
    origin_c = np.array(origin_c)
    origin_l = np.array(origin_l)
    origin_r = np.array(origin_r)
    center = None
    left = None
    right = None
    ##计算accumlate_s
    pre_c = origin_c[1:]
    back_c = origin_c[:-1]
    delta = back_c - pre_c
    delta_norm = np.linalg.norm(delta,axis=1)
    accumlate_s_array = np.cumsum(delta_norm)
    ##horizen内的点
    v_m = v_km/3.6
    plan_s = v_m * T
    plan_idx = accumlate_s_array <= plan_s
    plan_s_array = accumlate_s_array[plan_idx]
    origin_c = origin_c[1:][plan_idx]
    origin_l = origin_l[1:][plan_idx]
    origin_r = origin_r[1:][plan_idx]
    ##计算插值
    T_IDXS
    
    # print(len(origin_c), len(origin_r),len(origin_l))
    # return center, left, right

if __name__ == "__main__":

    reasign_points(origin_c=np.array([[1.0,2.0,30.0],[3.0,5.0,40.0],[8.0,6.0,8.0],[9.5,4.5,6.4],[9.5,4.5,6.4]]))