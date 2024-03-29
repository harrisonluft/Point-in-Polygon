from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None):
        if kind == "outside":
            plt.plot(x, y, "ro", label='Outside')
        elif kind == "boundary":
            plt.plot(x, y, "bo", label='Boundary')
        elif kind == "inside":
            plt.plot(x, y, "go", label='Inside')
        else:
            plt.plot(x, y, "ko", label='Unclassified')

    def add_line(self, x1, x2, y1, y2):
        plt.plot([x1, x2], [y1, y2], "yo-", alpha = 0.25, label = "Rays", markersize=0)

    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc = 'lower right')
        plt.xlabel("X values")
        plt.ylabel("Y values")
        plt.title("Point-in-Polygon Results")
        plt.show()

    def save(self, path):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='lower right')
        plt.xlabel("X values")
        plt.ylabel("Y values")
        plt.title("Point-in-Polygon Results")
        plt.savefig(path)