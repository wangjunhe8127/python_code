import os,sys
sys.path.append("/data/megvii/pilot")#将当前目录的上级目录的上级目录添加到搜索路径中，也就是可以在code_bases下查找
from path_point import points
from generate_boundary import generate_boundary
from reasign_points import reasign_points
from happypilot.config.config_mpc import V_KM, T, T_IDXS
points, pointsl,pointsr = generate_boundary(points,l=1.5,r=2.0)
reasign_points(origin_c = points, origin_l = pointsl, origin_r = pointsr, v_km = V_KM, T = T, T_IDXS = T_IDXS)
# center, left, right = reasign_points(points, pointsl, pointsr, v_m)