from path_point import points
from generate_boundary import generate_boundary
from tool_plot import plot_subplots, plot_common
pointsl,pointsr = generate_boundary(points,l=1.5,r=2.5)
# plot_subplots(points=[points,points1],xb=5,yb=5,fx=6,fy=6*2)#xy用来调整坐标轴刻度，f用来调整比例和图大小
# plot_subplots(points=[points,pointsl,pointsr],xb=5,yb=5,fx=6,fy=6)#xy用来调整坐标轴刻度，f用来调整比例和图大小
plot_common(points=[points,pointsl,pointsr])