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
from my_package import data_processing as dp
reload(dp)

Segment_ID, Node_ID_1, Node_ID_2, df = dp.combine_point_seg(combined_data_point, combined_data_segment)

# display(combined_data_segment.head(5))

print(Segment_ID)
print(Node_ID_1)
print(Node_ID_2)

print(df)


#%%
# save file
df.to_csv('compiled_data.csv', sep='\t')

df.to_pickle('compiled_data.pkl')

store = pd.HDFStore('compiled_data.h5')
store['df'] = df

#%%
del df
store.close()

#%%
import numpy as np
import pandas as pd
import os
from imp import reload 
from my_package import data_processing as dp
reload(dp)

df = pd.read_csv('compiled_data.csv', sep = '\t', index_col = 0)
df

#%%
## calculate the average thickness fo each segment
grouped_data = df['thickness'].groupby([df['objectID'], df['Segment ID']])
grouped_thickness_mean = grouped_data.mean()

grouped_thickness_mean

## get onject name 
objectname = list(np.unique(grouped_thickness_mean.index.get_level_values(0)))
objectname

#%%
# plot the thickness of each segment

import matplotlib.pyplot as plt
import seaborn as sns
import bokeh.palettes
import itertools
sns.set()

print(objectname)
objectname2 = ['Hypoxia', 'Normoxia']
range_max = int(np.ceil(max(grouped_thickness_mean)))
n_bins=range(0, range_max, 2)
color = ['red', 'blue']

normed_par = 1
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])
    
    plt.hist(grouped_thickness_mean.loc[objectname[i]], n_bins, alpha=0.5, label = objectname2[i], \
            normed=normed_par, color = color[i])
    
plt.xlim(left=0, right=range_max)
plt.xlabel('Thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='upper right')
plt.savefig('segment_thickness_prob.png', dpi = 300)
plt.close()

normed_par = 0
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])
    
    plt.hist(grouped_thickness_mean.loc[objectname[i]], n_bins, alpha=0.5, label = objectname2[i], \
            normed=normed_par, color = color[i])
    
plt.xlim(left=0, right=range_max)
plt.xlabel('Thickness (µm)')
plt.ylabel('Counts')
plt.legend(loc='upper right')
plt.savefig('segment_thickness_counts.png', dpi = 300)
plt.close()

#%%
# calculate the length fo each segment
import numpy as np
import pandas as pd
import os
from imp import reload 
from my_package import data_processing as dp
reload(dp)

length_sum = dp.distance_sum(df, objectname)
length_sum

#%%
#save file
length_sum.to_csv('compiled_data_length.csv', sep='\t')


#%%
# plot the length of each segment

import matplotlib.pyplot as plt
import seaborn as sns
import bokeh.palettes
import itertools
sns.set()

print(objectname)

objectname2 = ['Hypoxia', 'Normoxia']
range_max = int(np.ceil(max(length_sum['seg_length'])))
n_bins=range(0, range_max, 20 )
color = ['red', 'blue']

normed_par = 1
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])
    
    plt.hist(length_sum['seg_length'].loc[length_sum['objectID'] == objectname[i]], \
            n_bins, alpha=0.5, label = objectname2[i], \
            normed=normed_par, color = color[i])
    
plt.xlim(left=0, right=range_max)
plt.xlabel('Length (µm)')
plt.ylabel('Probability')
plt.legend(loc='upper right')
#plt.show()
plt.savefig('segment_length_prob.png', dpi = 300)
plt.close()

normed_par = 0
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])
    
    plt.hist(length_sum['seg_length'].loc[length_sum['objectID'] == objectname[i]], \
            n_bins, alpha=0.5, label = objectname2[i], \
            normed=normed_par, color = color[i])

plt.xlim(left=0, right=range_max)
plt.xlabel('Length (µm)')
plt.ylabel('Counts')
plt.legend(loc='upper right')
#plt.show()
plt.savefig('segment_length_counts.png', dpi = 300)
plt.close()

#%%
##################
# scatter plot
grouped_thickness_mean
thickness_df = grouped_thickness_mean.reset_index()
thickness_df
thickness_df.shape

length_sum.shape
length_sum

data = pd.merge(thickness_df, length_sum, on = ['objectID', 'Segment ID'])
data

objectname2 = ['Hypoxia', 'Normoxia']
color = ['red', 'blue']


for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])    
    plt.scatter(data['thickness'].loc[data['objectID'] == objectname[i]], \
                data['seg_length'].loc[data['objectID'] == objectname[i]], \
                color = color[i], alpha=0.5, label = objectname2[i], s= 3)

plt.xlabel('Thickness (µm)')
plt.ylabel('Length (µm)')
plt.legend(loc=1)
plt.savefig('scatter.png', dpi = 300)
plt.close()



#%%
##################
# create cumulative probability 
range_max = int(np.ceil(max(data['thickness'])))
print(range_max)

cumulative_data_thickness = {}
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])  

    data_thickness = data['thickness'].loc[data['objectID'] == objectname[i]]
    
    n_bins=list(range(0, range_max, 2))
    n_bins
    counts, bin_edges = np.histogram(data_thickness, bins = n_bins, normed = True)
    
    temp_data = {
                'counts': counts,
                'bin_edges': bin_edges,
                }
    cumulative_data_thickness[objectname[i]] = temp_data


range_max = int(np.ceil(max(data['seg_length'])))
print(range_max)

cumulative_data_length = {}
for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])  

    data_length = data['seg_length'].loc[data['objectID'] == objectname[i]]
    
    n_bins=list(range(0, range_max, 20))
    n_bins
    counts, bin_edges = np.histogram(data_length, bins = n_bins, normed = True)
    
    temp_data = {
                'counts': counts,
                'bin_edges': bin_edges,
                }
    cumulative_data_length[objectname[i]] = temp_data

#%%
# plot cumulative distrubtion
range_max = int(np.ceil(max(data['thickness'])))
range_max
objectname2 = ['Hypoxia', 'Normoxia']
color = ['red', 'blue']

for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])  
    cdf = np.cumsum(cumulative_data_thickness[objectname[i]]['counts'])
    bin_edges = cumulative_data_thickness[objectname[i]]['bin_edges']
    plt.plot(bin_edges[1:], cdf/cdf[-1], label = objectname2[i], color = color[i])

plt.xlim(left=0, right=range_max)
plt.xlabel('Thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='bottom right')
plt.savefig('segment_thickness_cumprob.png', dpi = 300)
plt.close()

range_max = int(np.ceil(max(data['seg_length'])))
range_max
objectname2 = ['Hypoxia', 'Normoxia']
color = ['red', 'blue']

for i in range(len(objectname)):
    print(objectname[i])
    print(color[i])  
    cdf = np.cumsum (cumulative_data_length[objectname[i]]['counts'])
    bin_edges = cumulative_data_length[objectname[i]]['bin_edges']
    plt.plot(bin_edges[1:], cdf/cdf[-1], label = objectname2[i], color = color[i])

plt.xlim(left=0, right=range_max)
plt.xlabel('Thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='bottom right')
plt.savefig('segment_length_cumprob.png', dpi = 300)
plt.close()

#%%
# statistic 
# ks-test

from scipy import stats
ks_result_thickness = stats.ks_2samp(\
                        cumulative_data_thickness[objectname[0]]['counts'], \
                        cumulative_data_thickness[objectname[1]]['counts'])
ks_result_thickness

ks_result_length = stats.ks_2samp(\
                        cumulative_data_length[objectname[0]]['counts'], \
                        cumulative_data_length[objectname[1]]['counts'])
ks_result_length


# print size
data.shape
print(objectname[0])
print(objectname[1])
print(data['thickness'].loc[data['objectID'] == objectname[0]].shape)
print(data['thickness'].loc[data['objectID'] == objectname[1]].shape)