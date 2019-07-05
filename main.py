#%% [markdown]
# # Lung Vasculature Analysis
# This notebook (.ipynb) is a working project for analyzing lung vasculature. It inculdes three parts:
# 1. converts skeleton analytical output (.xml) into .csv file.  
# 2. calulates the length and average thickness of each segment.
# 3. makes two types of plots: 
#     1. histogram of each dataset on length and thickness
#     2. average histogram on length and thickness (line plot with error bars)
# 

#%%
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import os, sys, re, io
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
from core.fileop import DirCheck, ListFiles
import core.mkplot as mkplot 

#%% [markdown]
#  ## Part 1: 
#  Converting skeleton analytical output (.xml) into .csv file.
#  * Inputs: *.xml 
#  * Outputs: *.csv
#  * Dependencies: xml, time, pandas, tqdm </br>
#  
#  * *.xml file includes three sheets: nodes, points, and segments. 
#  * Warning: the progress bar controled by `tqdm` is not functioning well. It can not overwrite itself and creates multiple lines. 
#%% [markdown]
# ### Functions

#%%
# import dependencies
import xml.etree.ElementTree as etree
from core.msxml import MSXmlReader

# function
def convert_xml_csv(ippath, oppath):
    filelist, fileabslist = ListFiles(ippath, extension='.xml')
    
    for idx, f in enumerate(filelist):
        filename = f.replace('.xml', '')
        ip = os.path.join(ippath, f) 
        op = os.path.join(oppath, filename)
        
        print(ip)
        print(op)

        # create path
        if filename not in os.listdir(oppath):
            DirCheck(op)
            
            # convert *.xml to *.csv 
            csv_all = MSXmlReader(ip)
            
            # save each spreadsheet into individual *.csv file
            for key, value in csv_all.items():
                oppath_tmp = os.path.join(op, key + '.csv')
                value.to_csv(oppath_tmp, index = False)

#%% [markdown]
# ### Execution
# To run the code, please change `path` to the directory hosts the raw data. 

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019'
ipdir = 'raw'
opdir = 'csv'
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir)
# make dir
DirCheck(oppath)

# convert files in batch
convert_xml_csv(ippath, oppath)

#%% [markdown]
#  ## Part 2: 
#  Calulating the length and average thickness of each segment.
#  * Inputs: nodes.csv, points.csv, segments.csv
#  * Outputs: segments_s.csv
#  
#  `SegStats` extracts euclidean coordinates and thickness of each point, then calculate the total length and average thickness. 
#%% [markdown]
# ### Functions

#%%
# load dependencies
from core.filamentanalysis import SegStats

# function
def stats_calculator(ippath, oppath):
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    
    var = ['df_nodes', 'df_points', 'df_segments']
    for img in imglist:
        filelist, fileabslist = ListFiles(os.path.join(ippath, img), extension='.csv')
        
        df_points = pd.read_csv(os.path.join(ippath, img, 'points.csv')) 
        df_segments = pd.read_csv(os.path.join(ippath, img, 'segments.csv')) 
        
        opfilename = 'segments_s.csv'
    
        if opfilename not in filelist:
            df_segments_s = SegStats(df_points, df_segments)            
            df_segments_s.to_csv(os.path.join(oppath, img, opfilename), index = False)
                

#%% [markdown]
# ### Execution
# To run the code, please change `path` to the directory hosts the raw data. 

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019'
ipdir = 'csv'
opdir = 'csv'
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir)
# make dir
DirCheck(oppath)

# convert files in batch
stats_calculator(ippath, oppath)

#%% [markdown]
# ## Part 3: 
# Creating two sets of plots: 
# 1. histogram of each dataset on length and thickness
# 2. average histogram on length and thickness (line plot with error bars)
# 
#  * Inputs: segments_s.csv
#  * Outputs: 
#      1. `histo/length/*.png`: frequency - length (µm)
#      2. `histo/thickness/*.png`: frequency - thickness (µm)
#      3. `histo_summary/length.png`: histogram in line plot style
#      4. `histo_summary/thickness.png`: histogram in line plot style
#  
#  `SegStats` extracts euclidean coordinates and thickness of each point, then calculate 
# the total length and average thickness. 
# 
# 
# In the ouputs, the code renames "thickness" to "radius" to avoid confusion. Quotes from 
# Amira User's Manual
# > As an estimate of the local thickness, the closest distance to the label 
# boundary (boundary distance map) is stored at every point in the *Spatial Graph*. 
# The attribute is named *thickness* and constitutes the *radius* of the circular cross-section 
# of the filament at a given point of the centerline.


#%%
# import depandencies
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('default')
import scipy.stats as stats
from core.mkplot import GroupImg, FindRange, IndividualHisto
from core.mkplot import make_individul_plots, make_merged_plots


#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019'
ipdir = 'csv'
opdir1 = 'plot'
opdir2 = 'histogram'
subfolder = ['histo', 'histo_summary']
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir1, opdir2)
for i in subfolder:
    oppath_sub = os.path.join(oppath, i)
    DirCheck(oppath_sub)

#%%
# load fileinfo
fileinfo = pd.read_csv(os.path.join('./par', 'lung_file_idx.csv'))

columns = {
    'length': {
        'x_label': 'Length (µm)',
        'file_label': 'length',
    },
    'thickness': {
        'x_label': 'Radius (µm)',
        'file_label': 'radius',
    },
}

#%%
# plot individual histogram
make_individul_plots(ippath, oppath, fileinfo, columns)

#%%
# plot merged histogram sin counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 0.07)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 0.07)

#%%
# plot merged histogram sin counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 0.2)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 0.2)

#%%
# plot merged histogram sin counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 1)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 1)

#%%

