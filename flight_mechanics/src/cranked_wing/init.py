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

from scipy.interpolate import interp1d, interp2d, Rbf

import h5py

from sympy import *

from IPython.display import display, Math, Latex, SVG

from cycler import cycler

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')
plt.rcParams['savefig.dpi'] = 96

plt.rcParams['figure.autolayout'] = False
plt.rcParams['figure.figsize'] = 10, 12
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

plt.rc('axes', 
       prop_cycle=(
           cycler('color', ['black', 'darkblue', 'red', 'green', 'blue', 'brown', 'orange', 'darkgreen'])
           + cycler('linestyle',["-", "--", "-.", ":", ".", "h", "H","-."])
           + cycler('dashes',[[10000,1], [10,5], [10,5,2,5], [3,3], [20,5,5,5], [30,5], [10,10], [2,5,5,3]])
           )
    )

#----------------------------------------------------------
def plot_planform(c_r, c_k, c_t, b_k, b, Lambda_le_1, Lambda_le_2, *args, **kwargs):

    fig = plt.subplots(figsize=(9, 11))
    
    # optional arguments
    c_mac = kwargs.get('mac', None)
    X_le_mac = kwargs.get('X_le_mac', None)
    Y_mac = kwargs.get('Y_mac', None)
    X_ac = kwargs.get('X_ac', None)
    
    xLineWing = [0, b_k/2, b/2, b/2, b_k/2, 0]
    dy_k = (b_k/2)*math.tan(Lambda_le_1)
    dy = dy_k + (b/2 - b_k/2)*math.tan(Lambda_le_2)
    yLineWing = [
        0, 
        dy_k, 
        dy,
        dy + c_t, 
        dy_k + c_k, 
        c_r]
        
    # planform
    lineWing, = plt.plot(xLineWing, yLineWing, 'k-')

    plt.scatter(xLineWing, yLineWing, marker='o', s=40)    
    
    # centerline
    centerLine, = plt.plot([0,0], [-1.1*c_r,2.1*c_r], 'b')
    centerLine.set_dashes([8, 4, 2, 4]) 
    # c/4 line
    pC4r = [0, 0.25*c_r]
    pC4k = [b_k/2, dy_k + 0.25*c_k]
    pC4t = [b/2, dy + 0.25*c_t]
    quarterChordLine, = plt.plot([pC4r[0],pC4k[0],pC4t[0]], [pC4r[1],pC4k[1],pC4t[1]], 'k--')
    plt.scatter([pC4r[0],pC4k[0],pC4t[0]], [pC4r[1],pC4k[1],pC4t[1]], marker='o', s=40)

    if ('mac' in kwargs) and ('X_le_mac' in kwargs) and ('Y_mac' in kwargs):
        c_mac = kwargs['mac']
        X_le_mac = kwargs['X_le_mac']
        Y_mac = kwargs['Y_mac']
        #print(mac)
        #print(X_le_mac)
        #print(Y_mac)
        lineMAC, = plt.plot([Y_mac, Y_mac], [X_le_mac, X_le_mac + c_mac], color="red", linewidth=2.5, linestyle="-")
        lineMAC.set_dashes([1000,1]) # HUUUUGE
        lineLEMAC, = plt.plot([0,b/2], [X_le_mac,X_le_mac], color="orange", linewidth=1.5, linestyle="-")
        lineLEMAC.set_dashes([10,2])
        lineTEMAC, = plt.plot([0,b/2], [X_le_mac + c_mac, X_le_mac + c_mac], color="orange", linewidth=1.5, linestyle="-")
        lineTEMAC.set_dashes([10,2])
        plt.scatter(Y_mac, X_le_mac, marker='o', s=40)
        ax = plt.gca()  # gca stands for 'get current axis'
        ax.annotate(
            r'$(Y_{\bar{c}},X_{\mathrm{le},\bar{c}}) = '
                +r'( {0:.3}'.format(Y_mac) + r'\,\mathrm{m}'+r',\,{0:.3}'.format(X_le_mac) + r'\,\mathrm{m} )$',
                         xy=(Y_mac, X_le_mac), xycoords='data',
                         xytext=(20, 30), textcoords='offset points', fontsize=12,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) # 
        
    if 'X_ac' in kwargs:
        X_ac = kwargs['X_ac']
        #print(X_ac)
        plt.scatter(0, X_ac, marker='o', s=40)
        lineAC, = plt.plot([0,b/2], [X_ac,X_ac], color="brown", linewidth=3.5, linestyle="-")
        lineAC.set_dashes([10,2.5,3,2.5])
        ax = plt.gca()  # gca stands for 'get current axis'
        ax.annotate(r'$X_{\mathrm{ac,W}} = '+r'{0:.3}'.format(X_ac)+r'\,\mathrm{m} $',
                         xy=(b/2, X_ac), xycoords='data',
                         xytext=(20, 30), textcoords='offset points', fontsize=12,
                         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) # 

    plt.axis('equal')
    
    #    xmajorLocator = MultipleLocator(2.0)
    #    xmajorFormatter = FormatStrFormatter('%.1f')
    #    xminorLocator = MultipleLocator(4)
    #    ax = plt.gca()  # gca stands for 'get current axis'
    #    ax.xaxis.set_major_locator(xmajorLocator)
    #    ax.xaxis.set_major_formatter(xmajorFormatter)
    #    # for the minor ticks, use no labels; default NullFormatter
    #    ax.xaxis.set_minor_locator(xminorLocator)
    
    plt.axis([-0.02*b/2, 1.1*b/2, -0.05*c_r, 1.1*(dy + c_t)])
    plt.gca().invert_yaxis()
    plt.title('Wing planform', fontsize=16)
    plt.xlabel('$y$ (m)', fontsize=16)
    plt.ylabel('$X$ (m)', fontsize=16)
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',c_r + 1.15*(dy_k + dy)))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.1*b/2))

    plt.show()

