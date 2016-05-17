# set the style of the notebook
from IPython.core.display import HTML
def css_styling():
    styles = open('./style/nbstyle.css', 'r').read()
    return HTML(styles)
css_styling()

# load libraries and set plot parameters
import math
import numpy as np
import scipy
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

import tailer #pip install tailer

import errno
import fnmatch
import os

import lxml.etree as etree
import re # regular expression module

#----------------------------------------------------------
def show_file_contents(fname, head=0, tail=0):
    # Display catalog file content
    for line in tailer.head(open(fname), head):
        print(line)
    print('\t...')
    print('\t...')
    for line in tailer.tail(open(fname), tail):
        print(line)
        
#----------------------------------------------------------
def show_file(fname):
    file = open(fname, 'r')
    for line in file:
        print(line, end='')

#----------------------------------------------------------

def mkdir_p(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

#----------------------------------------------------------
# example> move_files_to_folder('*.csv', './pippo'):
def move_files_to_folder(expr, folder):
    # create a folder
    mkdir_p(folder)
    # And move *.csv into that folder
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, expr): # e.g. '*.csv'
            print('{1} --> {0}/{1}'.format(folder,file))
            if os.path.isfile('{0}/{1}'.format(folder,file)):
                os.remove('{0}/{1}'.format(folder,file))
            os.rename(file,'{0}/{1}'.format(folder,file))

#----------------------------------------------------------
#http://lxml.de/tutorial.html
def pretty_print_from_file(fname, nodename):
    tree = etree.parse(fname)
    xmlstring0 = etree.tostring(tree.find(nodename), xml_declaration=False, pretty_print=True, encoding="unicode")
    xmlstring1 = re.sub('\\sxmlns:xsi="[^"]+"', '', xmlstring0, count=1)
    xmlstring = re.sub(r'^\s*$', '', xmlstring1)
    
    #print('')
    #print(xmlstring)
    print('\n'.join([line for line in xmlstring.split('\n') if line.strip()]))

#----------------------------------------------------------
def plot_Cmd_AngVel_EulerAng(data_fcs, data_velocities, data_attitude):
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['font.size'] = 16
    
    fig = plt.figure(figsize=(14,12))
    
    ax1 = fig.add_subplot(3,1,1)
    
    ax1.set_title("Commands")    
    ax1.set_xlabel('$t$ (s)')
    ax1.set_ylabel('(deg)')
    
    ax1.plot(data_fcs[:,0], data_fcs[:,18], color='r', label='$\delta_a$')
    ax1.plot(data_fcs[:,0], data_fcs[:,6], color='g', label='$\delta_e$')
    ax1.plot(data_fcs[:,0], data_fcs[:,9], color='b', label='$\delta_r$')
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels)
    
    ax2 = fig.add_subplot(3,1,2)
    
    ax2.set_title("Angular velocities")    
    ax2.set_xlabel('$t$ (s)')
    ax2.set_ylabel('(deg/s)')
    
    ax2.plot(data_velocities[:,0], 57.3*data_velocities[:,4], color='r', label='$p$')
    ax2.plot(data_velocities[:,0], 57.3*data_velocities[:,5], color='g', label='$q$')
    ax2.plot(data_velocities[:,0], 57.3*data_velocities[:,6], color='b', label='$r$')
    handles, labels = ax2.get_legend_handles_labels()
    ax2.legend(handles, labels)
    
    ax3 = fig.add_subplot(3,1,3)
    
    ax3.set_title("Euler angles")    
    ax3.set_xlabel('$t$ (s)')
    ax3.set_ylabel('(deg)')
    
    ax3.plot(data_attitude[:,0], 57.3*data_attitude[:,1], color='r', label="$\phi$")
    ax3.plot(data_attitude[:,0], 57.3*data_attitude[:,2], color='g', label="$\\theta$")
    ax3.plot(data_attitude[:,0], 0.1*57.3*data_attitude[:,3], color='b', label="$\psi$")
    handles, labels = ax3.get_legend_handles_labels()
    ax3.legend(handles, labels)
    
    plt.tight_layout()