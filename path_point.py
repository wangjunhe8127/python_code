import math


def draw_arc(center, radius, start_angle, end_angle, point_distance):
    # 计算圆心角和弧长
    angle_diff = end_angle - start_angle
    arc_length = angle_diff / 360 * 2 * math.pi * radius

    # 计算点数和圆心角的步长
    num_points = int(round(arc_length / point_distance))
    angle_step = angle_diff / num_points

    # 生成所有点
    points = []
    for i in range(num_points):
        angle = math.radians(start_angle + i * angle_step)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))

    return points


def draw_line(start, end, point_distance):
    # 计算线段的长度和方向
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    line_length = math.sqrt(dx ** 2 + dy ** 2)
    unit_dx = dx / line_length
    unit_dy = dy / line_length

    # 计算点数和点之间的距离
    num_points = int(round(line_length / point_distance))
    point_step = line_length / num_points

    # 生成所有点
    points = []
    for i in range(num_points + 1):
        x = start[0] + i * point_step * unit_dx
        y = start[1] + i * point_step * unit_dy
        points.append((x, y))

    return points

def concatenate_lists(*lists):
    concatenated_list = []
    for lst in lists:
        concatenated_list.extend(lst)
    return concatenated_list

points_s = draw_arc((0, 0), 4, 0, 90, 0.15)
points_lp = draw_line((4, -4), (4, 0), 0.15)
points_lb = draw_line((0, 4), (-12, 4), 0.15)
points = concatenate_lists(points_lp,points_s,points_lb)