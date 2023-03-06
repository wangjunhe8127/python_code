import math
import numpy as np
def generate_boundary(points,l=2,r=2):
    new_points_l = []
    new_points_r = []
    new_points = []
    width_l = l
    width_r = r
    points = np.array(points)
    num = 0
    for i in range(len(points) - 1):
        x1, y1 = points[i][0],points[i][1]
        x2, y2 = points[i+1][0],points[i+1][1]
        dx, dy = x2 - x1, y2 - y1
        
        if x1 == x2 and y1 == y2:
            continue

        num += 1
        angle = math.atan2(dy, dx)

        x_delta, y_delta = -1 * width_l * math.sin(angle), width_l * math.cos(angle)
        l = [x1+x_delta, y1+y_delta]
        new_points_l.append(l)
        x_delta, y_delta = width_r * math.sin(angle), -1* width_r * math.cos(angle)
        r = [x1+x_delta, y1+y_delta]
        new_points_r.append(r)
        new_points.append(points[i])
    return new_points, new_points_l,new_points_r