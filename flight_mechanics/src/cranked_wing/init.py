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

    fig = plt.subplots(figsize=(9, 9))
    
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
    centerLine, = plt.plot([0,0], [-0.2*c_r,2.1*c_r], 'b')
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
    ax.spines['bottom'].set_position(('outward',10)) # outward by 10 points
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.07*b/2))

    plt.show()

#----------------------------------------------------------
def plot_wing_functions(c_r, c_k, c_t, 
                    eps_k, eps_t, alpha0l_r, alpha0l_k, alpha0l_t,
                    b_k, b, Lambda_le_1, Lambda_le_2, 
                    f_chords, f_Xle, f_twist, f_alpha0l,
                    *args, **kwargs):
    """
    
    See: http://www.scipy-lectures.org/intro/matplotlib/matplotlib.html
    
    """

    # optional arguments
    f_S_integral_indefinite = kwargs.get('f_S_integral_indefinite', None)
    f_alpha0L_integral_indefinite = kwargs.get('f_alpha0L_integral_indefinite', None)


    # define vectors
    n_points = 20
    vY0 = np.linspace(0, b/2, n_points, endpoint=True)
    vY1 = np.concatenate([vY0,[b_k/2]])
    vY = np.sort(np.unique(vY1))
    vChord = []
    vXle = []
    vTwist = []
    vAlpha0l = []
    for y in vY:
        vChord.append(f_chords(c_r, c_k, c_t, b_k, b, Lambda_le_1, Lambda_le_2, y))
        vXle.append(f_Xle(b_k, b, Lambda_le_1, Lambda_le_2, y))
        vTwist.append(f_twist(eps_k, eps_t, b_k, b, y))
        vAlpha0l.append(f_alpha0l(alpha0l_r, alpha0l_k, alpha0l_t, b_k, b, y))
        
    vChord = np.asarray(vChord)
    vTwist = np.asarray(vTwist)
    vXle = np.asarray(vXle)
    vAlpha0l = np.asarray(vAlpha0l)
    
    # Create a figure of size WxH inches, DPI dots per inch
    fig = plt.figure(figsize=(11, 12), dpi=300)
    
    # Create a new subplot from a grid of 1x1
    ax0 = plt.subplot(1, 1, 1)
    
    #fig, ax0 = plt.subplots()
    
    
    plt.plot(vY, vChord, color="red", linewidth=2.5, linestyle="-", label=r'local chord $c$ (m)')
    plt.plot(vY, vXle, color="green", linewidth=2.5, linestyle="-", label=r'local l.e. coordinate $X_{\mathrm{le}}$ (m)')
    plt.plot(vY, vTwist*180/np.pi, color="blue",  linewidth=2.5, linestyle="-", label=r"local $\epsilon_{\mathrm{g}}$ (deg)")
    plt.plot(vY, vAlpha0l*180/np.pi, color="brown",  linewidth=2.5, linestyle="-", label=r"local $\alpha_{0\ell}$ (deg)")
    
    if ('f_S_integral_indefinite' in kwargs):
        y = Symbol('y')
        f_S_integral_indefinite = kwargs['f_S_integral_indefinite']
        vS_integrand = []
        for y_ in vY:
            #print(y_)
            val = f_S_integral_indefinite.subs(y,y_)
            #print(val)
            vS_integrand.append(val)
            #vAlpha0L_integrand.append(f_alpha0L_integral_indefinite.subs(y,y_))
            #vAlpha0L_integrand = np.asarray(vAlpha0L_integrand)
        
        vS_integrand = np.asarray(vS_integrand)
        plt.plot(vY, vS_integrand/10, color="orange",  linewidth=2.5, linestyle="-", dashes=[1000,1], marker="." ,
                 label=r"Integrand function $0.1\,\int c(y)\mathrm{d}y$ (m${}^2$)")
                 
        # shaded region --> http://matplotlib.org/examples/showcase/integral_demo.html
        vertices = [(0, 0)] + list(zip(vY, vS_integrand/10)) + [(b/2, 0)]
        poly = Polygon(vertices, facecolor="green", alpha=0.3, edgecolor="none")
        ax0.add_patch(poly)

    if ('f_alpha0L_integral_indefinite' in kwargs):
        y = Symbol('y')
        f_alpha0L_integral_indefinite = kwargs['f_alpha0L_integral_indefinite']
        vAlpha0L_integrand = []
        for y_ in vY:
            #print(y_)
            val = f_alpha0L_integral_indefinite.subs(y,y_)
            #print(val)
            vAlpha0L_integrand.append(val)
            #vAlpha0L_integrand.append(f_alpha0L_integral_indefinite.subs(y,y_))
            #vAlpha0L_integrand = np.asarray(vAlpha0L_integrand)
        
        vAlpha0L_integrand = np.asarray(vAlpha0L_integrand)
        plt.plot(vY, vAlpha0L_integrand, color="orange",  linewidth=2.5, linestyle="-", dashes=[1000,1], marker="." ,
                 label=r"Integrand function $\big(\alpha_{0\ell} - \epsilon_{\mathrm{g}}\big) c$ (rad m)")
                 
        # shaded region --> http://matplotlib.org/examples/showcase/integral_demo.html
        vertices = [(0, 0)] + list(zip(vY, vAlpha0L_integrand)) + [(b/2, 0)]
        poly = Polygon(vertices, facecolor="orange", alpha=0.5, edgecolor="none")
        ax0.add_patch(poly)

    
    # shaded region --> http://matplotlib.org/examples/showcase/integral_demo.html
    #vertices = [(0, 0)] + list(zip(vY, vIntegrand*180/np.pi)) + [(b/2, 0)]
    #poly = Polygon(vertices, facecolor="orange", alpha=0.5, edgecolor="none")
    #ax0.add_patch(poly)
    
    plt.legend(loc='upper center', fontsize=18)
    
    tipLine, = plt.plot([b/2,b/2], [-4, 7], color="gray", linewidth=1.0, linestyle="-")
    tipLine.set_dashes([8, 4]) 
    plt.annotate(r'$y=\frac{1}{2}\,b$',
                 xy=(b/2, -4), xycoords='data',
                 xytext=(40, -40), textcoords='offset points', fontsize=22,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.5"))

    kinkLine, = plt.plot([b_k/2,b_k/2], [-4, 7], color="gray", linewidth=1.0, linestyle="-")
    kinkLine.set_dashes([8, 4]) 
    plt.annotate(r'$y=\frac{1}{2}\,b_{\mathrm{k}}$',
                 xy=(b_k/2, -4), xycoords='data',
                 xytext=(40, -40), textcoords='offset points', fontsize=22,
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.5"))
    
    zeroYLine, = plt.plot([-1,b/2], [0,0],  color="gray", linewidth=1.0, linestyle="-")
    zeroYLine.set_dashes([8, 4]) 
    
    plt.axis([0, 1.1*b/2, -5, 8])
    plt.title('Wing functions', fontsize=22)
    plt.xlabel('$y$ (m)', fontsize=22)
    #plt.ylabel('$X$ (m)', fontsize=22)
    
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',-6))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.1))    
    plt.show()
