#%% [markdown]

#%%
%load_ext autoreload
%autoreload 2
import os, sys, re, io
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
from core.fileop import DirCheck, ListFiles
import core.mkplot as mkplot 


#%% [markdown]
# Convert file from *.xml to *.csv
# Dependencies: xml, time, pandas, tqdm

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

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/'
ipdir = 'raw'
opdir = 'csv'
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir)
# make dir
DirCheck(oppath)

# convert files in batch
convert_xml_csv(ippath, oppath)

#%% [markdown]
# create average length and diameter for each image
#%%
# load dependencies
from core.filamentanalysis import SegStats, BranchLabel

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
                
#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/'
ipdir = 'csv'
opdir = 'csv'
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir)
# make dir
DirCheck(oppath)

# convert files in batch
stats_calculator(ippath, oppath)



#%% [markdown]
# Plot

#%%
# import depandencies
import scipy.stats as stats
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('default')


# functions
def group_img(ippath, fileinfo):
    # group imgs bu fileinfo    
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    
    grped_imglist = defaultdict(list)
    
    for img in imglist:
        img_group = fileinfo[fileinfo['data_filename'] == img]['treatment'].item()
        grped_imglist[img_group].append(img)
    
    return grped_imglist

def find_range(ippath):
    
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]

    # find min and max 
    length_min_list = []
    length_max_list = []
    thickness_min_list = []
    thickness_max_list = []
    for img in imglist: 
        df_segments = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
        length_min_list.append(df_segments['length'].min())
        length_max_list.append(df_segments['length'].max())
        thickness_min_list.append(df_segments['thickness'].min())
        thickness_max_list.append(df_segments['thickness'].max())
        
    length_range = [min(length_min_list), max(length_max_list)]
    thickness_range = [min(thickness_min_list), max(thickness_max_list)]
    
    return(length_range, thickness_range)

def individual_histo(df, binsize = 100, bin_range = list):
        
    bins_length = np.linspace(bin_range[0], bin_range[1], binsize)    

    ax1 = plt.subplot(111)
    data = df['length']
    ax1.hist(data, bins = bins_length, 
                weights=(np.zeros_like(data) + 1. / data.size) * 100)
    ax1.set_xlabel('Bins')
    ax1.set_ylabel('Frequency (%)')
    
    return ax1

def make_individul_plots(ippath, oppath):
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    # get range
    length_range, thickness_range = find_range(ippath)
    
    # make histogram for individual dataset
    for img in imglist:
        
        df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
        
        # histogram for average length  
        plt.figure(figsize=(5, 5))
        
        ax = individual_histo(df_segments_s, bin_range = length_range)
        
        DirCheck(os.path.join(oppath, 'histo', 'length'))
        opfilename = os.path.join(oppath, 'histo', 'length', img + '.png')
        plt.savefig(opfilename)
        plt.close()

        # histogram for average thickness    
        plt.figure(figsize=(5, 5))

        ax = individual_histo(df_segments_s, bin_range = thickness_range)
        
        DirCheck(os.path.join(oppath, 'histo', 'thickness'))
        opfilename = os.path.join(oppath, 'histo', 'thickness', img + '.png')
        plt.savefig(opfilename)
        plt.close()   

    return    

def make_merged_plots(ippath, oppath):
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    # get range
    length_range, thickness_range = find_range(ippath)

    grp_imglist = group_img(ippath, fileinfo)
    
    plt.figure(figsize=(5, 5))
    dflist = []
    for treatment, imgs in grp_imglist.items():
        binsize = 100
        bins_length = np.linspace(length_range[0], length_range[1], binsize) 
        for img in imgs:
            df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
            df_segments_s['bins'] = pd.cut(df_segments_s['length'], bins = bins_length)
            df_bins_count = df_segments_s.groupby('bins').size()
            df_bins_count = df_bins_count.reset_index()
            df_bins_count = df_bins_count.iloc[:, 1]
            dflist.append(df_bins_count)
        
        df_tmp = pd.concat(dflist, axis = 1)
        dfarray = np.array(df_tmp)
        mean = dfarray.mean(axis = 1, keepdims = True)
        #print(mean)
        sem = stats.sem(dfarray, axis = 1)
        #print(sem)
        ax1 = plt.subplot(111)
        bins_length = np.array([bins_length[0:-1]]).T
        print(bins_length.shape)
        print(mean.shape)
        ax1.errorbar(bins_length, mean, yerr = sem, alpha = 0.2)
    
    opfilename = os.path.join(oppath, 'histo_summary', 'length.png')
    plt.savefig(opfilename)
    plt.close()
    
    plt.figure(figsize=(5, 5))
    dflist = []
    for treatment, imgs in grp_imglist.items():
        binsize = 100
        bins_length = np.linspace(length_range[0], length_range[1], binsize) 
        for img in imgs:
            df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
            df_segments_s['bins'] = pd.cut(df_segments_s['thickness'], bins = bins_length)
            df_bins_count = df_segments_s.groupby('bins').size()
            df_bins_count = df_bins_count.reset_index()
            df_bins_count = df_bins_count.iloc[:, 1]
            dflist.append(df_bins_count)
        
        df_tmp = pd.concat(dflist, axis = 1)
        dfarray = np.array(df_tmp)
        mean = dfarray.mean(axis = 1, keepdims = True)
        #print(mean)
        sem = stats.sem(dfarray, axis = 1)
        #print(sem)
        ax1 = plt.subplot(111)
        bins_length = np.array([bins_length[0:-1]]).T
        print(bins_length.shape)
        print(mean.shape)
        ax1.errorbar(bins_length, mean, yerr = sem, alpha = 0.2)
    
    opfilename = os.path.join(oppath, 'histo_summary', 'thickness.png')
    plt.savefig(opfilename)
    plt.close()


    return

path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/'
ipdir = 'csv'
opdir1 = 'plot'
opdir2 = 'histogram'
subfolder = ['histo', 'histo_summary']
ippath = os.path.join(path, ipdir)
oppath = os.path.join(path, opdir1, opdir2)
for i in subfolder:
    oppath_sub = os.path.join(oppath, i)
    DirCheck(oppath_sub)


# load fileinfo
fileinfo = pd.read_csv(os.path.join(path, 'par', 'lung_file_idx.csv'))
# display(fileinfo)

#make_individul_plots(ippath, oppath)
make_merged_plots(ippath, oppath)



#%%
