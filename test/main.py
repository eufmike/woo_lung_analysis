#%%
%load_ext autoreload
%autoreload 2
import os, sys, re, io
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('default')
# style.use('fivethirtyeight')

from core.fileop import DirCheck, ListFiles
from core.filamentanalysis import SegStats, BranchLabel

#%%
ippath = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/'
var = ['df_nodes', 'df_points', 'df_segments']
fl_names = ['lung_vs_002_nodes.csv', 'lung_vs_002_points.csv', 'lung_vs_002_segments.csv']

for idx in range(len(fl_names)):
    exec("%s = pd.read_csv(os.path.join(ippath, '%s'))"%(var[idx], fl_names[idx]))

#%%
# calculate length for each segments
filelist = ListFiles(ippath, extension='.csv')[0]
filelist = [filename + '.csv' for filename in filelist]
print(filelist)

#%%
opfilename = 'lung_vs_002_segments_s.csv'
if opfilename in filelist:
    df_segments_s = pd.read_csv(os.path.join(ippath, opfilename), header = 0)
else:
    df_segments_s = SegStats(df_points, df_segments)            
    df_segments_s.to_csv(os.path.join(ippath, opfilename), index = False)

#%%
display(df_segments_s)

#%%
def binminmax(data, binsize = 100, bin_min = 0):
    val_max = np.max(data)
    bin_max = np.ceil(val_max/binsize) * binsize
    bins = np.linspace(bin_min, bin_max, binsize)
    return bins

#%%
plt.figure(figsize=(5, 5))
ax1 = plt.subplot(211)
ax1 = plt.hist(df_segments_s['length'], bins = binminmax(df_segments_s['length']))
ax2 = plt.subplot(212)
ax1 = plt.hist(df_segments_s['thickness'], bins = binminmax(df_segments_s['thickness']))
plt.show()

#%%
display(df_nodes)
display(df_segments)


#%%
display(df_nodes.iloc[23966, 0])
#%%
print(df_nodes.loc[df_nodes['Node ID'] == 471, 'Node ID'].item())
#%%
# characterize branch connection
ls_done, branch_lvl = BranchLabel(df_nodes, df_segments)

#%%
print(len(df_nodes))
print(len(ls_done[0]))

#%%
# print(ls_done)
print(ls_done)

#%%
print(branch_lvl)

#%%


#%%
