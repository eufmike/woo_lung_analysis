#%% [markdown]
#  # Lung Vasculature Analysis
#  This notebook (.ipynb) is a working project for analyzing lung vasculature. It inculdes three parts:
#  1. converts skeleton analytical output (.xml) into .csv file.
#  2. calulates the length and average thickness of each segment.
#  3. makes two types of plots:
#      1. histogram of each dataset on length and thickness
#      2. average histogram on length and thickness (line plot with error bars)
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
#   ## Part 1:
#   Converting skeleton analytical output (.xml) into .csv file.
#   * Inputs: *.xml
#   * Outputs: *.csv
#   * Dependencies: xml, time, pandas, tqdm </br>
# 
#   * *.xml file includes three sheets: nodes, points, and segments.
#   * Warning: the progress bar controled by `tqdm` is not functioning well. It can not overwrite itself and creates multiple lines.
#%% [markdown]
#  ### Functions

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
#  ### Execution
#  To run the code, please change `path` to the directory hosts the raw data.

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
#   ## Part 2:
#   Calulating the length and average thickness of each segment.
#   * Inputs: nodes.csv, points.csv, segments.csv
#   * Outputs: segments_s.csv
# 
#   `SegStats` extracts euclidean coordinates and thickness of each point, then calculate the total length and average thickness.
#%% [markdown]
#  ### Functions

#%%
# load dependencies
from core.filamentanalysis import SegStats, PNSCount

path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019'
ipdir = 'csv'
ippath = os.path.join(path, ipdir)
img_group = []

# function
def stats_calculator(ippath, oppath):
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    
    var = ['df_nodes', 'df_points', 'df_segments']
    counts_combined = []
    names= []
    
    for img in imglist:
        filelist, fileabslist = ListFiles(os.path.join(ippath, img), extension='.csv')
        
        df_points = pd.read_csv(os.path.join(ippath, img, 'points.csv')) 
        df_segments = pd.read_csv(os.path.join(ippath, img, 'segments.csv')) 
        df_nodes = pd.read_csv(os.path.join(ippath, img,'nodes.csv'))
        
        opfilename = 'segments_s.csv'
        countfilename = 'count.csv'
        countfilename_combined = 'counts_combined.csv'
    
        if opfilename not in filelist:
            df_segments_s = SegStats(df_points, df_segments)            
            df_segments_s.to_csv(os.path.join(oppath, img, opfilename), index = False)
        
        counts = (PNSCount(df_points, df_nodes, df_segments))
        counts_combined.append(counts)
        names.append(img)

    fileinfo = pd.read_csv(os.path.join('./par', 'lung_file_idx.csv'))
    print(names)

    img_group = []
    for i in names:
        img_group.append(fileinfo[fileinfo['data_filename'] == i]['genotype'].item())

    if countfilename_combined not in imglist:
        df_counts_combined = pd.DataFrame(counts_combined, columns= ['Points', 'Nodes', 'Segments'])
        df_counts_combined['Names'] = names
        df_counts_combined['Genotype'] = img_group
        df_counts_combined.to_csv(os.path.join(path, countfilename_combined), index = False)
            
       

#%% [markdown]
#  ### Execution
#  To run the code, please change `path` to the directory hosts the raw data.

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
#  ## Part 3:
#  Creating two sets of plots:
#  1. histogram of each dataset on length and thickness
#  2. average histogram on length and thickness (line plot with error bars)
# 
#   * Inputs: segments_s.csv
#   * Outputs:
#       1. `histo/length/*.png`: frequency - length (µm)
#       2. `histo/thickness/*.png`: frequency - thickness (µm)
#       3. `histo_summary/length.png`: histogram in line plot style
#       4. `histo_summary/thickness.png`: histogram in line plot style
# 
#   `SegStats` extracts euclidean coordinates and thickness of each point, then calculate
#  the total length and average thickness.
# 
# 
#  In the ouputs, the code renames "thickness" to "radius" to avoid confusion. Quotes from
#  Amira User's Manual
#  > As an estimate of the local thickness, the closest distance to the label
#  boundary (boundary distance map) is stored at every point in the *Spatial Graph*.
#  The attribute is named *thickness* and constitutes the *radius* of the circular cross-section
#  of the filament at a given point of the centerline.

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

#%% [markdown]
#  Create plots with x-axis in different scales

#%%
# plot merged histogram in counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 0.07)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 0.07)


#%%
# plot merged histogram in counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 0.2)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 0.2)


#%%
# plot merged histogram in counts
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 1)
# plot merged histogram in frequency 
make_merged_plots(ippath, oppath, fileinfo, columns, frequency = True, x_max_factor = 1)

#%% [markdown]
# # Part 4
# 
#     Plot the Points, Nodes, and Segment Count in Bokeh with Holoview
#     
#     
# 
# 

#%%
import numpy as np
import pandas as pd
import holoviews as hv
from holoviews import opts, Cycle

#%%
hv.extension('bokeh')

path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019'
ipfile = 'counts_combined.csv'
ippath = (os.path.join(path, ipfile))

counts = pd.read_csv(ippath)

f1 = hv.Scatter((zip(counts.Points.items(), counts.Nodes.items())), ['Points'], ['Nodes'])

f2 = hv.Scatter((zip(counts.Points.items(), counts.Segments.items())), ['Points'], ['Segments'])
f3 = hv.Scatter((zip(counts.Nodes.items(), counts.Points.items())), ['Nodes'], ['Points'])
f4 = hv.Scatter((zip(counts.Nodes.items(), counts.Segments.items())), ['Nodes'], ['Segments'])
f5 = hv.Scatter((zip(counts.Segments.items(), counts.Points.items())), ['Segments'], ['Points'])
f6 = hv.Scatter((zip(counts.Segments.items(), counts.Nodes.items())), ['Segments'], ['Nodes'])

f1 + f2 + f3 + f4 + f5 + f6 



#%%
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')
from holoviews.operation import gridmatrix
from bokeh.sampledata.iris import flowers
from bokeh.palettes import brewer
import bokeh.models as bmod

counts = pd.read_csv(ippath)
colors = brewer["Spectral"][len(counts.Genotype.unique())]
colormap = {counts.Genotype.unique()[i] : colors[i] for i in range(len(counts.Genotype.unique()))}
colors = [colormap[x] for x in counts.Genotype]

print(colormap)

iris_ds = hv.Dataset(counts).groupby('Genotype').overlay()

point_grid = gridmatrix(iris_ds, chart_type=hv.Points)

(point_grid).opts(
    opts.Bivariate(bandwidth=0.5, cmap=hv.Cycle(values = colors)),
    opts.Points(size=5, alpha=0.5),
    opts.NdOverlay(batched= False))


