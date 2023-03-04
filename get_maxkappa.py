def calculate_curvature(points):
    curvature = []
    max_kappa = 0
    max_idx = 0
    for i in range(1, len(points) - 1):
        x0, y0 = points[i-1]
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        dx1, dy1 = x1 - x0, y1 - y0
        dx2, dy2 = x2 - x1, y2 - y1
        cross_product = dx1 * dy2 - dy1 * dx2
        numerator = 2 * abs(cross_product)
        denominator = (dx1**2 + dy1**2)**1.5 + (dx2**2 + dy2**2)**1.5
        if denominator == 0:
            pass
        else:
            if numerator / denominator > max_kappa:
                max_kappa = numerator / denominator
                max_idx = i
    return max_kappa, max_idx
