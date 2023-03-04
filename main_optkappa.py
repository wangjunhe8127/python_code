import numpy as np
from scipy.optimize import minimize
from path_point import points
from generate_boundary import generate_boundary
from tool_plot import plot_subplots,plot_common
from  optkappa import optimize_center_line
from change_local import to_local_coordinates
# from xy2frent import cartesian_to_frenet
#左右边界
pointsl,pointsr = generate_boundary(points,l=1.5,r=2.5)
left_boundary=pointsl
right_boundary=pointsr
#修改为numpy格式
center_line = np.array([list(t) for t in points])
left_boundary = np.array(left_boundary)
right_boundary = np.array(right_boundary)
# 计算局部坐标系下的坐标
center_line, left_boundary, right_boundary = to_local_coordinates(center_line,left_boundary,right_boundary)

# #生成优化的点
new_points = optimize_center_line(center_line,left_boundary,right_boundary,max_curvature=0.2,max_offset=0.2)
# #画图
all_points =  [center_line,left_boundary, right_boundary,new_points]

# all_points = [center_line,left_boundary, right_boundary]
plot_common(points=all_points)