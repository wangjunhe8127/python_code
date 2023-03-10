import numpy as np
import math
import matplotlib.pyplot as plt

def plot_subplots(points, xb, yb, fx,fy):
    num_subplots = len(points)
    num_rows = math.ceil(math.sqrt(num_subplots))
    num_cols = math.ceil(num_subplots/num_rows)
    fig, axes = plt.subplots(num_rows, num_cols)
    for i in range(num_subplots):
        point = np.array(points[i])
        if num_subplots >2:
            row = i // num_cols
            col = i % num_cols
            axes[row, col].plot(point[:,0],point[:,1])
            axes[row, col].set_title(f"Subplot {i + 1}")
            axes[row, col].axis('equal')
        else:
            axes[i].plot(point[:,0],point[:,1])
            axes[i].set_title(f"Subplot {i + 1}")
            axes[i].axis('equal')
        # axes[i].set_xlim([-xb,xb])
        # axes[i].set_ylim([-yb, yb])

    # 设置横轴和纵轴的刻度范围和间隔
    xticklocs = np.linspace(-xb, xb, 10)
    xticklabels = ['{:2.1f}'.format(loc) for loc in xticklocs]
    yticklocs = np.linspace(-yb, yb, 10)
    yticklabels = ['{:2.1f}'.format(loc) for loc in yticklocs]

    # 为每个子图设置刻度范围和间隔
    for ax in axes.flatten():
        ax.set_xticks(xticklocs)
        ax.set_xticklabels(xticklabels)
        ax.set_yticks(yticklocs)
        ax.set_yticklabels(yticklabels)

    # 设置画布大小并调整子图之间的距离
    fig.set_size_inches(fx, fy)
    fig.tight_layout()

    # 显示图表
    plt.show()


def plot_common(idx = 0,mode = "show"):
    inter_idx = idx
    def step(points,one_point=[]):
        nonlocal inter_idx
        num_subplots = len(points)
        fig, ax = plt.subplots()
        for i in range(num_subplots):
            point = np.array(points[i])
            ax.plot(point[:,0],point[:,1])
        if len(one_point) != 0:
            for i in one_point:
                ax.scatter(i[0],i[1])
        ax.axis('equal')
        if mode == "show":
            plt.show()
        else:
            plt.savefig(f'/data/megvii/pilot/picture/{inter_idx}.jpg')
            inter_idx +=1
        return 
    return step
    # xticklocs = np.linspace(-xb, xb, 10)
    # yticklocs = np.linspace(-yb, yb, 10)