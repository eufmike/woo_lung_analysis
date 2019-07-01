import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from collections import defaultdict
import matplotlib.pyplot as plt
from core.fileop import DirCheck, ListFiles

def GroupImg(ippath, fileinfo):
    # group imgs from fileinfo    
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    
    grped_imglist = defaultdict(list)
    
    for img in imglist:
        img_group = fileinfo[fileinfo['data_filename'] == img]['treatment'].item()
        grped_imglist[img_group].append(img)
    
    return grped_imglist

def FindRange(ippath):
    
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

def IndividualHisto(df, column, binsize = 100, bin_range = None):

    bins = np.linspace(bin_range[0], bin_range[1], binsize)    
    data = df[column]
    ax1 = plt.subplot(111)
    ax1.hist(data, bins = bins, 
                weights=(np.zeros_like(data) + 1. / data.size) * 100)
    
    return ax1

def make_individul_plots(ippath, oppath, fileinfo):
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    # get range
    length_range, thickness_range = FindRange(ippath)
    # print(length_range, thickness_range)
    
    # create labels
    xlabel = ['Length (µm)', 'Thickness (µm)'] 

    # make histogram for individual dataset
    for img in imglist:
        
        df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
        
        # histogram for average length  
        plt.figure(figsize=(5, 5))
        
        ax = IndividualHisto(df_segments_s, column = 'length', bin_range = length_range)
        ax.set_xlabel(xlabel[0])
        ax.set_ylabel('Frequency (%)')
                   
        DirCheck(os.path.join(oppath, 'histo', 'length'))
        opfilename = os.path.join(oppath, 'histo', 'length', img + '.png')
        plt.savefig(opfilename)
        plt.close()

        # histogram for average thickness    
        plt.figure(figsize=(5, 5))

        ax = IndividualHisto(df_segments_s, column = 'thickness', bin_range = thickness_range)
        ax.set_xlabel(xlabel[1])
        ax.set_ylabel('Frequency (%)')
        
        DirCheck(os.path.join(oppath, 'histo', 'thickness'))
        opfilename = os.path.join(oppath, 'histo', 'thickness', img + '.png')
        plt.savefig(opfilename)
        plt.close()   

    return

def make_merged_plots(ippath, oppath, fileinfo):
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    # get range
    length_range, thickness_range = FindRange(ippath)
    
    # create labels
    xlabel = ['Length (µm)', 'Thickness (µm)']
    
    # treatment
    grp_imglist = GroupImg(ippath, fileinfo)
    
    fig, ax = plt.subplots(1, 1, figsize=(5,5))
    dflist = []
    for treatment, imgs in grp_imglist.items():
        binsize = 100
        bins = np.linspace(length_range[0], length_range[1], binsize) 
    
        for img in imgs:
            df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
            df_segments_s['bins'] = pd.cut(df_segments_s['length'], bins = bins)
            df_bins_count = df_segments_s.groupby('bins').size()
            df_bins_count = df_bins_count.reset_index()
            df_bins_count = df_bins_count.iloc[:, 1]
            dflist.append(df_bins_count)
        
        df_tmp = pd.concat(dflist, axis = 1)
        dfarray = np.array(df_tmp)
        array_mean = dfarray.mean(axis = 1, keepdims = True)
        # print(mean)
        array_sem = stats.sem(dfarray, axis = 1)
        # print(sem)
        bins_length = np.array([bins[0:-1]]).T
        # print(bins_length.shape)
        # print(mean.shape)
        
        ax.errorbar(bins_length, array_mean, yerr = array_sem, alpha = 0.8)
        ax.set_xlabel(xlabel[0])
        ax.set_ylabel('Counts')
        # ax.spines['right'].set_visible(False)
        # ax.spines['top'].set_visible(False)

    ax.legend(grp_imglist.keys())
    opfilename = os.path.join(oppath, 'histo_summary', 'histo_counts_length.png')
    plt.savefig(opfilename)
    plt.show()
    plt.close()
    
    
    # thickness
    fig, ax = plt.subplots(1, 1, figsize=(5,5))
    dflist = []
    for treatment, imgs in grp_imglist.items():
        binsize = 100
        
        bins = np.linspace(thickness_range[0], thickness_range[1], binsize) 
        
        for img in imgs:
            df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
            df_segments_s['bins'] = pd.cut(df_segments_s['thickness'], bins = bins)
            df_bins_count = df_segments_s.groupby('bins').size()
            df_bins_count = df_bins_count.reset_index()
            df_bins_count = df_bins_count.iloc[:, 1]
            dflist.append(df_bins_count)
        
        df_tmp = pd.concat(dflist, axis = 1)
        dfarray = np.array(df_tmp)
        array_mean = dfarray.mean(axis = 1, keepdims = True)
        #print(mean)
        array_sem = stats.sem(dfarray, axis = 1)
        #print(sem)
        bins_length = np.array([bins[0:-1]]).T
        # print(bins_length.shape)
        # print(mean.shape)
        ax.errorbar(bins_length, array_mean, yerr = array_sem, alpha = 0.8)
        ax.set_xlabel(xlabel[1])
        ax.set_ylabel('Counts')

    plt.legend(grp_imglist.keys())    
    opfilename = os.path.join(oppath, 'histo_summary', 'histo_counts_thickness.png')
    plt.savefig(opfilename)
    plt.show()
    plt.close()
    
    return