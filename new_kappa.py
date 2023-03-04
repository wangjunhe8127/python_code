import  numpy as np
def com_kappa(center_line, max_curvature):
    # 计算每个点的曲率（使用前向差分来近似）
    dx = np.diff(center_line[:, 0])
    dy = np.diff(center_line[:, 1])
    ddx = np.diff(dx)[:-1]
    ddy = np.diff(dy)[:-1]
    epsilon = 1e-8  # 添加的小常数
    curvature = np.abs(ddx * dy[:-2] - dx[:-2] * ddy) / np.power(dx[:-2] ** 2 + dy[:-2] ** 2 + epsilon, 1.5)

    # 找到需要优化的点
    idxs = np.where(curvature > max_curvature)[0] + 1
    return idxs