import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from collections import defaultdict
import matplotlib.pyplot as plt

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