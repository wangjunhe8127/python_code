import numpy as np

# 计算曲线的曲率
def curvature(x, y):
    dx_dt = np.gradient(x)
    d2x_dt2 = np.gradient(dx_dt)
    dy_dt = np.gradient(y)
    d2y_dt2 = np.gradient(dy_dt)
    k = (d2x_dt2 * dy_dt - dx_dt * d2y_dt2) / (dx_dt**2 + dy_dt**2)**1.5
    return k

# 计算笛卡尔坐标系中的点在Frenet坐标系中的位置和曲率
def cartesian_to_frenet(x, y):
    ds = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
    s = np.cumsum(ds)
    ds_dt = np.gradient(s)
    x_dt = np.gradient(x)
    y_dt = np.gradient(y)
    yaw = np.arctan2(y_dt, x_dt)
    k = curvature(x, y)
    k = np.concatenate(([k[0]], k, [k[-1]]))
    d = np.abs(yaw - np.arctan(k * ds_dt)) * np.sign(x[1:] - x[:-1])
    d = np.concatenate(([0], d, [0]))
    s = np.concatenate(([0], s, [s[-1]]))
    return d, s, k

# 测试
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([0, 1, 4, 9, 16, 25])
d, s, k = cartesian_to_frenet(x, y)
print("d: ", d)
print("s: ", s)
print("k: ", k)
