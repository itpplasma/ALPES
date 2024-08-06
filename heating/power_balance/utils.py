
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def make_clickable_legend(loc='upper right', fig=None, ax=None):
    # we cannot use plt.gcf() and plt.gca() as default parameter, because this would open a new figure when importing utils.py
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.gca()
    legend = ax.legend(loc=loc)
    legend_lines = legend.get_lines()
    legend_texts = legend.get_texts()
    index_by_legend_line = {}
    index_by_legend_text = {}
    lines = ax.lines
    for i, legend_line in enumerate(legend_lines):
        legend_line.set_picker(True)
        legend_line.set_pickradius(10)
        index_by_legend_line[legend_line] = i
    for i, legend_text in enumerate(legend_texts):
        legend_text.set_picker(True)
        index_by_legend_text[legend_text] = i

    def on_pick(event):
        if isinstance(event.artist, matplotlib.lines.Line2D):
            legend_line = event.artist
            index = index_by_legend_line[legend_line]
        else:
            legend_text = event.artist
            index = index_by_legend_text[legend_text]
            legend_line = legend_lines[index]
        isVisible = legend_line.get_visible()

        lines[index].set_visible(not isVisible)
        legend_line.set_visible(not isVisible)

        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    ax.grid('both')

def solve_quadratic_equation(a, b, c):
    """solves the equation a * x^2 + b * x + c = 0"""
    if np.all(a == 0):
        x = -c / b

        return x, x

    else:
        discriminant = b**2 - 4 * a * c

        x1 = (-b - np.sqrt(discriminant)) / (2 * a)
        x2 = (-b + np.sqrt(discriminant)) / (2 * a)

        return x1, x2
