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
    
    fileinfo['temp_group'] = fileinfo['genotype'] + '_' + fileinfo['treatment']
    
    for img in imglist:
        img_group = fileinfo[fileinfo['data_filename'] == img]['temp_group'].item()
        grped_imglist[img_group].append(img)

    return grped_imglist

def FindRange(ippath, variable):
    
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]

    # find min and max 
    min_list = []
    max_list = []

    for img in imglist: 
        df_segments = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
        min_list.append(df_segments[variable].min())
        max_list.append(df_segments[variable].max())
        
    data_range = [min(min_list), max(max_list)]
    
    return(data_range)

def IndividualHisto(df, column, x_max_factor, binsize = 100, bin_range = None):

    bins = np.linspace(bin_range[0], bin_range[1] * x_max_factor, binsize)    
    data = df[column]
    ax1 = plt.subplot(111)
    ax1.hist(data, bins = bins, 
                weights=(np.zeros_like(data) + 1. / data.size) * 100)
    
    return ax1

def make_individul_plots(ippath, oppath, fileinfo, columns, x_max_factor = 1):
    #print("1:" + oppath)
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]
    
    for key, value in columns.items():
        # get range
        data_range = FindRange(ippath, variable = key)
        
        # make histogram for individual dataset
        for img in imglist :
            #print("2:" + oppath)
            df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
            
            # histogram for average length  
            plt.figure(figsize=(5, 5))
            
            ax = IndividualHisto(df_segments_s, column = key, bin_range = data_range, x_max_factor = x_max_factor)
            ax.set_xlabel(value['x_label'])
            ax.set_ylabel('Frequency (%)')
                    
            DirCheck(os.path.join(oppath, 'histo', value['file_label']))
            opfilename = os.path.join(oppath, 'histo', value['file_label'], img + '.png')
            plt.savefig(opfilename)
            plt.close()
    return

def make_merged_plots(ippath, oppath, fileinfo, columns, frequency = False, x_max_factor = 1):
    # extract file list
    imglist = [x for x in os.listdir(ippath) if not x.startswith('.')]

    # treatment
    grp_imglist = GroupImg(ippath, fileinfo)

    # histogram type
    if frequency: 
        hist_type = 'frequency'
    else:  
        hist_type = 'counts'
    
    hist_type_dic = {
        'frequency': 'Frequency (%)',
        'counts': 'Counts',
    }

    for key, value in columns.items():
        # get range
        data_range = FindRange(ippath, variable = key)    

        fig, ax = plt.subplots(1, 1, figsize=(5,5), dpi = 300)
        dflist = []
        for treatment, imgs in grp_imglist.items():
            binsize = 200
            bins = np.linspace(data_range[0], data_range[1], binsize) 

            for img in imgs:
                df_segments_s = pd.read_csv(os.path.join(ippath, img, 'segments_s.csv'))
                df_segments_s['bins'] = pd.cut(df_segments_s[key], bins = bins)
                df_bins_count = df_segments_s.groupby('bins').size()
                df_bins_count = df_bins_count.reset_index()
                df_bins_count = df_bins_count.iloc[:, 1]
                
                if frequency: 
                    dflist.append(df_bins_count/len(df_segments_s) * 100)
                else:
                    dflist.append(df_bins_count)
            
            df_tmp = pd.concat(dflist, axis = 1)
            dfarray = np.array(df_tmp)
            array_mean = dfarray.mean(axis = 1, keepdims = True)
            array_sem = stats.sem(dfarray, axis = 1)
            bins_length = np.array([bins[0:-1]]).T
            
            ax.errorbar(bins_length, array_mean, yerr = array_sem, alpha = 0.5)
            ax.set_xlabel(value['x_label'])
            ax.set_ylabel(hist_type_dic[hist_type])
            ax.set_xlim(data_range[0] - (data_range[1]*x_max_factor - data_range[0]) * 0.05, data_range[1]*x_max_factor + (data_range[1]*x_max_factor - data_range[0]) * 0.05)
            
        ax.legend(grp_imglist.keys())
        opfilename = os.path.join(oppath, 'histo_summary', 'histo_' + hist_type + '_' +
                                 value['file_label'] + '_' +
                                 str(x_max_factor).replace('.', '_') +  
                                 '.png')
        plt.savefig(opfilename)
        # plt.show()
        plt.close()

    return
