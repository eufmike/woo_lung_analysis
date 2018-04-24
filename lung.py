#! /Users/michaelshih/anaconda3/bin/python

#%%
import numpy as np
import pandas as pd
import os
from imp import reload 
from my_package import data_processing as dp
reload(dp)

# create data list        
dir = '/Users/michaelshih/Documents/code/wucci/woo_lung_analysis'
os.chdir(dir)
datafolder = 'raw_xlsx'
datapath = os.path.join(dir, datafolder)
print(datapath)

# load data by pandas
filenames = dp.listdir_nohidden(datapath)
print(filenames)

combined_data_point = pd.DataFrame([])
combined_data_segment = pd.DataFrame([])

for m in filenames:
    
    # create file path
    filepath = os.path.join(dir, datafolder, m)
    data = pd.ExcelFile(filepath)
    
    # input xlsx file
    sheetname = data.sheet_names
    data_point = data.parse(sheetname[1])
    data_point = pd.DataFrame(data_point)
    data_segment = data.parse(sheetname[2])
    data_segment = pd.DataFrame(data_segment)

    # create column for each group
    filename = os.path.splitext(m)[0]
    data_point['objectID'] = filename
    data_segment['objectID'] = filename

    combined_data_point = combined_data_point.append(data_point, ignore_index = True)
    combined_data_segment = combined_data_segment.append(data_segment, ignore_index = True)

# show data
combined_data_point.head(5)
print(combined_data_point.shape[0])
combined_data_segment.head(5)
combined_data_segment.tail(5)
#%%
from imp import reload 
from my_package import data_processing
reload(data_processing)

df = dp.combine_point_seg(combined_data_point, combined_data_segment)
print(df)


#%%
import matplotlib.pyplot as plt
import seaborn
seaborn.set()
# n, bins, patches = plt.hist(data_point['thickness'], 50, normed=1, facecolor='green', alpha=0.75)
# plt.xlabel('thickness (µm)')
# plt.ylabel('Probability')
# plt.show()
# plt.savefig('thickness_histogram.png')
objectname = np.unique(combined_data_point['objectID'])
x1 = combined_data_point.loc[combined_data_point['objectID'] == objectname[0], 'thickness']
x2 = combined_data_point.loc[combined_data_point['objectID'] == objectname[1], 'thickness']
n_bins=range(0, 200, 2)

normed_par = 1
plt.hist(x1, n_bins, alpha=0.5, label = objectname[0], normed=normed_par)
plt.hist(x2, n_bins, alpha=0.5, label = objectname[1], normed=normed_par)
plt.xlim(left=0, right=200)
plt.xlabel('thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='upper right')
plt.show()
