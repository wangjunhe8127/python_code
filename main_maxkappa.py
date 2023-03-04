import numpy as np
from get_maxkappa import calculate_curvature
import matplotlib.pyplot as plt
from path_point import points
max_kappa, max_idx = calculate_curvature(points)

print(f"Maximum curvature: {max_kappa:.2f}")
print(f"Maximum curvature point: {points[max_idx]} (index: {max_idx})")

# Plot the original points and the interpolated curve
plt.plot(np.array(points)[:,0], np.array(points)[:,1], '-', label='interpolated')

# Add annotations for the maximum curvature point
plt.annotate(f"Max curvature = {max_kappa:.2f}",
             xy=points[max_idx],
             xytext=(points[max_idx][0]+0.2, points[max_idx][1]+0.2),
             arrowprops=dict(facecolor='red', arrowstyle='->'))
plt.plot(points[max_idx][0], points[max_idx][1], 'ro')

# Display the plot
plt.legend()
plt.show()
