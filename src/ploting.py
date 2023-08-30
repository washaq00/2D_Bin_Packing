import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from data_structures.bin_2d import Bin2D
from typing import List

PACKAGE_FACE = "c"
PACKAGE_EDGE = "k"
BIN_EDGE = "k"


def add_bin2d_to_plot(ax: plt.Axes, bin: Bin2D):
    ax.add_patch(Rectangle((0, 0), bin.width, bin.height, edgecolor=BIN_EDGE))
    ax.set_xlim(0, bin.width)
    ax.set_ylim(0, bin.height)

    for package in bin.packages:
        r = Rectangle(package.location(), package.width, package.height, edgecolor=PACKAGE_EDGE, facecolor=PACKAGE_FACE)
        ax.add_patch(r)
        rx, ry = r.get_xy()
        cx = rx + r.get_width() / 2.0
        cy = ry + r.get_height() / 2.0
        ax.annotate(package.id, (cx, cy), color='black', weight='bold', fontsize=10, ha='center', va='center')


def plot_bins2d(bins: List[Bin2D], block=False):
    bin_num = len(bins)
    fig, ax = plt.subplots(1, bin_num)
    for i in range(bin_num):
        add_bin2d_to_plot(ax[i], bins[i])

    plt.show(block=block)
