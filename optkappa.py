import numpy as np
from new_kappa import com_kappa
from scipy.optimize import minimize_scalar
from scipy.interpolate import UnivariateSpline

def optimize_center_line(centerline, left_bound, right_bound, max_curvature=0.01, max_offset=1.0):
    # 计算每个点的曲率（使用前向差分来近似）
    idxs = com_kappa(centerline,max_curvature)
    if len(idxs) == 0:
        return centerline

    left_bound = interpolate_bound(left_bound, centerline)
    right_bound = interpolate_bound(right_bound, centerline)

    # 在边界上插值，以确保优化后的中心线不会超出边界
    left_interp = UnivariateSpline(centerline[:, 0], left_bound[:, 1])
    right_interp = UnivariateSpline(centerline[:, 0], right_bound[:, 1])

    def optimize_point(idx):
        x = centerline[idx, 0]
        # 求取在x点的优化函数值
        center = np.array([x, centerline[idx, 1]])
        f = lambda y: np.sum((center - np.array([x, y])) ** 2) + 1e7 * is_out_of_bounds(center, left_interp, right_interp)
        # 最小化函数
        res = minimize_scalar(f, bounds=(left_interp(idx), right_interp(idx)), method='bounded')
        return res.x
    # 对每个需要平滑的点进行优化
    for i in idxs:
        centerline[i, 1] = optimize_point(i)
    # 平滑斜率
    # # centerline = smooth_slope(centerline)
    return centerline

def is_out_of_bounds(center, left_interp, right_interp):
    # 判断中心线是否超出边界
    left_bound = left_interp(center[0])
    right_bound = right_interp(center[0])
    return (center[1] < left_bound) or (center[1] > right_bound)


def interpolate_bound(bound, centerline):
    # 计算中心线上每个点的 x 坐标
    center_x = centerline[:, 0]

    # 将边界点的 x 坐标插值到中心线上
    bound_x = np.linspace(bound[0, 0], bound[-1, 0], len(bound))
    bound_y = np.interp(center_x, bound_x, bound[:, 1])

    # 将插值后的边界点作为新的边界返回
    new_bound = np.column_stack((center_x, bound_y))
    return new_bound