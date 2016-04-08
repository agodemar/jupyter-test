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

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')
plt.rcParams['savefig.dpi'] = 96

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

plt.rc('axes', 
       prop_cycle=(
           cycler('color', ['black', 'darkblue', 'red', 'green', 'blue', 'brown', 'orange', 'darkgreen'])
           + cycler('linestyle',["-", "--", "-.", ":", ".", "h", "H","-."])
           + cycler('dashes',[[10000,1], [10,5], [10,5,2,5], [3,3], [20,5,5,5], [30,5], [10,10], [2,5,5,3]])
           )
    )

#----------------------------------------------------------
def import_database_aerodynamic_center():
    fileName = "./resources/wing_aerodynamic_center.h5"
    f = h5py.File(fileName,'r',libver='latest')
    # K1
    data_K1 = f["(x_bar_ac_w)_k1_vs_lambda/data"]
    var0_K1 = f["(x_bar_ac_w)_k1_vs_lambda/var_0"]
    # K2
    data_K2 = f["(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/data"]
    var0_K2 = f["(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_0"]
    var1_K2 = f["(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_1"]
    var2_K2 = f["(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_2"]
    # xac/cr
    data_XacCr = f["(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/data"]
    var0_XacCr = f["(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_0"]
    var1_XacCr = f["(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_1"]
    var2_XacCr = f["(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_2"]
    return {
        'data_K1':data_K1, 
        'var0_K1':var0_K1, 
        'data_K2':data_K2, 
        'var0_K2':var0_K2, 
        'var1_K2':var1_K2, 
        'var2_K2':var2_K2,
        'data_XacCr':data_XacCr,
        'var0_XacCr':var0_XacCr,
        'var1_XacCr':var1_XacCr,
        'var2_XacCr':var2_XacCr
        }

#----------------------------------------------------------
def report_database_dimensions(database):
    shape_data_K1 = database['data_K1'].shape
    shape_var0_K1 = database['var0_K1'].shape
    
    shape_data_K2 = database['data_K2'].shape
    shape_var0_K2 = database['var0_K2'].shape
    shape_var1_K2 = database['var1_K2'].shape
    shape_var2_K2 = database['var2_K2'].shape
    
    shape_data_XacCr = database['data_XacCr'].shape
    shape_var0_XacCr = database['var0_XacCr'].shape
    shape_var1_XacCr = database['var1_XacCr'].shape
    shape_var2_XacCr = database['var2_XacCr'].shape
    
    print('(x_bar_ac_w)_k1_vs_lambda/var_0')
    print('shape of var0: {0}'.format(shape_var0_K1))
    print('(x_bar_ac_w)_k1_vs_lambda/data')
    print('shape of data: {0}'.format(shape_data_K1))
    """
    print('lambda --> K1')
    for i in range(shape_var0_K1[0]):
        print('{0}\t{1}'.format(dset_var0_K1[i],dset_data_K1[i]))
    """
    print('=====================================')
    print('(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_0')
    print('shape of var0: {0}'.format(shape_var0_K2))
    print('(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_1')
    print('shape of data: {0}'.format(shape_var1_K2))
    print('(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/var_2')
    print('shape of data: {0}'.format(shape_var2_K2))
    print('(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/data')
    print('shape of data: {0}'.format(shape_data_K2))
    print('=====================================')
    print("(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_0")
    print('shape of var0: {0}'.format(shape_var0_XacCr))
    print("(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_1")
    print('shape of data: {0}'.format(shape_var1_XacCr))
    print("(x_bar_ac_w)_x'_ac_over_root_chord_vs_tan_(L_LE)_over_beta_(AR_times_tan_(L_LE))_(lambda)/var_2")
    print('shape of data: {0}'.format(shape_var2_XacCr))
    print('(x_bar_ac_w)_k2_vs_L_LE_(AR)_(lambda)/data')
    print('shape of data: {0}'.format(shape_data_XacCr))

#----------------------------------------------------------
def plot_K1(var0_K1, data_K1):
    fig, ax = plt.subplots()
    plt.plot(var0_K1, data_K1, color="red", linewidth=2.5, linestyle="-")
    plt.title('Wing aerodynamic center --- effect of $\lambda$', fontsize=22)
    plt.xlabel('$\lambda$', fontsize=22)
    plt.ylabel('$K_1$', fontsize=22)
    plt.axis([0, 1, 0.8, 1.6])
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0.78))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.01))
    
    plt.show()

#----------------------------------------------------------
def plot_K2(var0_K2, var1_K2, var2_K2, data_K2, j_lambda=0):

    if j_lambda > 5 :
        print('Index j_lambda={0} out of range. Maximum allowed value 5'.format(j_lambda))
        return
    
    fig, ax = plt.subplots()
    
    #plt.gca().set_prop_cycle(
    #    cycler('color', ['c', 'm', 'y', 'k']) + cycler('lw', [1, 2, 3, 4]))
    
    idx_max_LambdaLE = 9
    
    for i_AR in range(0, 6):
        slice_ij = None
        slice_ij = data_K2[:,i_AR,j_lambda]
        line, = plt.plot(var2_K2, slice_ij, linewidth=2.5, linestyle="-")
        line.set_dashes([1000,1]) # HUUUUGE
        plt.annotate(r'$\mathrm{AR} = \,$'+r'{0}'.format(var1_K2[i_AR]),
                     xy=(var2_K2[idx_max_LambdaLE], slice_ij[idx_max_LambdaLE]), xycoords='data',
                     xytext=(40, 0), textcoords='offset points', fontsize=22,
                     arrowprops=dict(arrowstyle="->")) # , connectionstyle="arc3,rad=.5"
    plt.title(
        'Wing aerodynamic center --- effect of $(\Lambda_{\mathrm{le}},\mathrm{AR})$, '
        +r'$\lambda = {0:.3}$'.format(var0_K2[j_lambda]),
        fontsize=22)
    
    plt.axis([0, 45, 0, 1.1*max(data_K2[:,5,j_lambda])])
    
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',-0.05))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.5))
    
    plt.xlabel('$\Lambda_{\mathrm{le}}$ (deg)', fontsize=22)
    plt.ylabel('$K_2$', fontsize=22)
    plt.show()

#----------------------------------------------------------
def plot_XacCr(var0_XacCr, var1_XacCr, var2_XacCr, data_XacCr, j_lambda=0):
    
    if j_lambda > 5 :
        print('Index j_lambda={0} out of range. Maximum allowed value 5'.format(j_lambda))
        return

    fig, ax = plt.subplots()
    
    #plt.gca().set_prop_cycle(
    #    cycler('color', ['c', 'm', 'y', 'k']) + cycler('lw', [1, 2, 3, 4]))
    
    idx_max_TanLambdaLE = 10
    
    for i_AR in range(0, 7):
        slice_ij = None
        slice_ij = data_XacCr[:,i_AR,j_lambda]
        line, = plt.plot(var2_XacCr, slice_ij, linewidth=2.5, linestyle="-")
        line.set_dashes([1000,1]) # HUUUUGE
        plt.annotate(r'$\mathrm{AR} \tan\Lambda_{\mathrm{le}} =\,$'+r'{0}'.format(var1_XacCr[i_AR,0]),
                     xy=(var2_XacCr[idx_max_TanLambdaLE], slice_ij[idx_max_TanLambdaLE]), xycoords='data',
                     xytext=(40, 0), textcoords='offset points', fontsize=22,
                     arrowprops=dict(arrowstyle="->")) # , connectionstyle="arc3,rad=.5"
    plt.title(
        r'Wing aerodynamic center --- effect of $(\tan\Lambda_{\mathrm{le}}/\sqrt{1-M^2},\mathrm{AR}\tan\Lambda_{\mathrm{le}})$, '
        +'$\lambda = {0:.3}$'.format(var0_XacCr[j_lambda]),
        fontsize=22)
    
    plt.axis([0, 2.2, -0.05, 1.1*max(data_XacCr[:,6,j_lambda])])
    
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',-0.07))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.05))
    
    plt.xlabel(r'$\tan\Lambda_{\mathrm{le}}/\sqrt{1-M^2}$', fontsize=22)
    plt.ylabel('$X_{\mathrm{ac}}\'/c_{\mathrm{r}}$', fontsize=22)
    plt.show()

#----------------------------------------------------------
def plot_interpolate_K1(var0_K1, data_K1, lam):
    g = interp1d(var0_K1, data_K1)
    K1 = g(lam)
    print('lambda = {0} --> K_1 = {1}'.format(lam,K1))
    fig, ax = plt.subplots()
    plt.plot(var0_K1, data_K1, color="brown", linewidth=2.5, linestyle="-")

    # interpolated data
    plt.scatter(lam, K1, marker='o', s=40)
    help_line, = plt.plot([lam,lam,0],[0,K1,K1], color="red", linewidth=1.5, linestyle="--")
    help_line.set_dashes([8, 4]) 
    
    plt.title('Wing aerodynamic center --- effect of $\lambda$', fontsize=22)
    plt.xlabel('$\lambda$', fontsize=22)
    plt.ylabel('$K_1$', fontsize=22)
    plt.axis([0, 1, 0.8, 1.6])
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0.78))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.01))
    
    plt.show()

#----------------------------------------------------------
def plot_interpolate_K2(var0_K2, var1_K2, var2_K2, data_K2, j_lambda, 
                        LamLE_deg, AR):

    if j_lambda > 5 :
        print('Index j_lambda={0} out of range. Maximum allowed value 5'.format(j_lambda))
        return

    # interpolation in 2D
    g = interp2d(var1_K2, var2_K2, data_K2[:,:,j_lambda], kind='linear')
    K2 = g(AR, LamLE_deg)
    print('Lambda_LE = {0} deg, AR = {1} --> K_2 = {2}'.format(LamLE_deg, AR, K2))
    
    fig, ax = plt.subplots()
    
    #plt.gca().set_prop_cycle(
    #    cycler('color', ['c', 'm', 'y', 'k']) + cycler('lw', [1, 2, 3, 4]))
    
    idx_max_LambdaLE = 9
    
    for i_AR in range(0, 6):
        slice_ij = None
        slice_ij = data_K2[:,i_AR,j_lambda]
        line, = plt.plot(var2_K2, slice_ij, linewidth=2.5, linestyle="-")
        line.set_dashes([1000,1]) # HUUUUGE
        plt.annotate(r'$\mathrm{AR} = \,$'+r'{0}'.format(var1_K2[i_AR]),
                     xy=(var2_K2[idx_max_LambdaLE], slice_ij[idx_max_LambdaLE]), xycoords='data',
                     xytext=(40, 0), textcoords='offset points', fontsize=22,
                     arrowprops=dict(arrowstyle="->")) # , connectionstyle="arc3,rad=.5"

    # interpolated data
    plt.scatter(LamLE_deg, K2, marker='o', s=40)
    help_line, = plt.plot([LamLE_deg,LamLE_deg,0],[0,K2,K2], color="red", linewidth=1.5, linestyle="--")
    help_line.set_dashes([8, 4]) 
    
    plt.title(
        'Wing aerodynamic center --- effect of $(\Lambda_{\mathrm{le}},\mathrm{AR})$, '
        +r'$\lambda = {0:.3}$'.format(var0_K2[j_lambda]),
        fontsize=22)
    
    plt.axis([0, 45, 0, 1.1*max(data_K2[:,5,j_lambda])])
    
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',-0.03))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.5))
    
    plt.xlabel('$\Lambda_{\mathrm{le}}$ (deg)', fontsize=22)
    plt.ylabel('$K_2$', fontsize=22)
    plt.show()

#----------------------------------------------------------
def plot_interpolate_XacCr(var0_XacCr, var1_XacCr, var2_XacCr, data_XacCr, j_lambda, 
                           LamLE_deg, AR, Mach):
    
    if j_lambda > 5 :
        print('Index j_lambda={0} out of range. Maximum allowed value 5'.format(j_lambda))
        return

    # interpolation in 2D
    g = interp2d(var1_XacCr, var2_XacCr, data_XacCr[:,:,j_lambda], kind='linear')
    y_ = AR*math.tan(LamLE_deg*np.pi/180)
    x_ = math.tan(LamLE_deg*np.pi/180)/math.sqrt(1 - math.pow(Mach,2))
    XacCr = g(y_,x_)
    print('x_1 = tan(Lambda_LE)/sqrt(1-M^2) = {0}\nx_2 = AR*tan(Lambda_LE) = {1}\n --> Xac\'/c_r = {2}'
        .format(x_, y_, XacCr))

    fig, ax = plt.subplots()
    
    #plt.gca().set_prop_cycle(
    #    cycler('color', ['c', 'm', 'y', 'k']) + cycler('lw', [1, 2, 3, 4]))
    
    idx_max_TanLambdaLE = 10
    
    for i_AR in range(0, 7):
        slice_ij = None
        slice_ij = data_XacCr[:,i_AR,j_lambda]
        line, = plt.plot(var2_XacCr, slice_ij, linewidth=2.5, linestyle="-")
        line.set_dashes([1000,1]) # HUUUUGE
        plt.annotate(r'$\mathrm{AR} \tan\Lambda_{\mathrm{le}} =\,$'+r'{0}'.format(var1_XacCr[i_AR,0]),
                     xy=(var2_XacCr[idx_max_TanLambdaLE], slice_ij[idx_max_TanLambdaLE]), xycoords='data',
                     xytext=(40, 0), textcoords='offset points', fontsize=22,
                     arrowprops=dict(arrowstyle="->")) # , connectionstyle="arc3,rad=.5"

    # interpolated data
    plt.scatter(x_, XacCr, marker='o', s=40)
    help_line, = plt.plot([x_,x_,0],[0,XacCr,XacCr], color="red", linewidth=1.5, linestyle="-")
    help_line.set_dashes([8, 4]) 
    
    plt.title(
        r'Wing aerodynamic center --- effect of $(\tan\Lambda_{\mathrm{le}}/\sqrt{1-M^2},\mathrm{AR}\tan\Lambda_{\mathrm{le}})$, '
        +'$\lambda = {0:.3}$'.format(var0_XacCr[j_lambda]),
        fontsize=22)
    
    plt.axis([0, 2.2, -0.05, 1.1*max(data_XacCr[:,6,j_lambda])])
    
    # Moving spines
    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',-0.07))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',-0.05))
    
    plt.xlabel(r'$\tan\Lambda_{\mathrm{le}}/\sqrt{1-M^2}$', fontsize=22)
    plt.ylabel('$X_{\mathrm{ac}}\'/c_{\mathrm{r}}$', fontsize=22)
    plt.show()

