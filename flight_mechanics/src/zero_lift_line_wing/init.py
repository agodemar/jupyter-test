# set the style of the notebook
from IPython.core.display import HTML
def css_styling():
    styles = open('./style/nbstyle.css', 'r').read()
    return HTML(styles)
css_styling()

# load libraries and set plot parameters
import math
import numpy as np
import tables as pt

from sympy import *

from IPython.display import display, Math, Latex, SVG

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')
plt.rcParams['savefig.dpi'] = 75

plt.rcParams['figure.autolayout'] = False
plt.rcParams['figure.figsize'] = 10, 6
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8
plt.rcParams['legend.fontsize'] = 14

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = "serif"
plt.rcParams['font.serif'] = "cm"
# plt.rcParams['text.latex.preamble'] = "\usepackage{subdepth}, \usepackage{type1cm}"

#----------------------------------------------------------
def plot_planform(c_r, c_t, b):
    xLineWing = [0,b/2,b/2,0]
    yLineWing = [0,0.25*c_r-0.25*c_t,0.25*c_r+0.75*c_t,c_r]

    # planform
    lineWing, = plt.plot(xLineWing, yLineWing, 'k-')
    # centerline
    centerLine, = plt.plot([0,0], [-1.1*c_r,2.1*c_r], 'b')
    centerLine.set_dashes([8, 4, 2, 4]) 
    # c/4 line
    quarterChordLine, = plt.plot([0,1.05*b], [0.25*c_r,0.25*c_r], 'k--')

    plt.axis('equal')
    plt.axis([-0.1*b/2, 1.1*b/2, -0.1*c_r, 1.1*c_r])
    plt.gca().invert_yaxis()
    plt.title('Wing planform', fontsize=22)
    plt.xlabel('$y$ (m)', fontsize=22)
    plt.ylabel('$X$ (m)', fontsize=22)
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',2*c_r))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.1*b/2))

    plt.show()