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
df.to_csv("complited_data.csv", sep='\t')

#%%
df.to_pickle("complited_data.pkl")

#%%
store = pd.HDFStore('complited_data.h5')
store['df'] = df



#%%
df = store['df']
df
#%%
grouped_data = df.groupby([df['objectID'], df['Segment ID']])
grouped_mean = grouped_data.mean()
grouped_mean
grouped_mean['objectID']
grouped_data.groups.keys()

#%%
#df['thickness'].hist(by=df['objectID'], normed=1)
grouped_mean['thickness'].hist()

#%%
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

grouped_data.groups.keys()

objectname = np.unique(grouped_mean['objectID'])
print(objectname)
normed_par = 1
n_bins=range(0, 200, 2)

for i in objectname:
    plt.hist(i, n_bins, alpha=0.5, label = i, normed=normed_par)

plt.xlim(left=0, right=200)
plt.xlabel('thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='upper right')
plt.show()






#%%
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
