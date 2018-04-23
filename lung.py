#%%
import numpy as np
import pandas as pd
import os

dir = '/Users/major_minor1982/Documents/code/lung'
os.chdir(dir)
datafolder = 'raw_xlsx'
datapath = os.path.join(dir, datafolder)
filenames = os.listdir(datafolder)
print(filenames)

#%%
# load data by pandas
combined_data = pd.DataFrame([])
for m in filenames:
    
    filepath = os.path.join(dir, datafolder, m)
    data = pd.ExcelFile(filepath)
    
    sheetname = data.sheet_names
    data_point = data.parse(sheetname[1])
    data_point = pd.DataFrame(data_point)
    
    # objectname = pd.DataFrame(m)
    filename = os.path.splitext(m)[0]
    data_point['objectID'] = filename

    #data_merge = pd.concat([data_point, objectname], axis = 1) 
    combined_data = combined_data.append(data_point, ignore_index = True)


# show data
combined_data.head(5)
print(combined_data.shape[0])

#%%
import matplotlib.pyplot as plt
import seaborn
seaborn.set()
# n, bins, patches = plt.hist(data_point['thickness'], 50, normed=1, facecolor='green', alpha=0.75)
# plt.xlabel('thickness (µm)')
# plt.ylabel('Probability')
# plt.show()
# plt.savefig('thickness_histogram.png')
objectname = np.unique(combined_data['objectID'])
x1 = combined_data.loc[combined_data['objectID'] == objectname[0], 'thickness']
x2 = combined_data.loc[combined_data['objectID'] == objectname[1], 'thickness']
n_bins=range(0, 200, 5)

normed_par = 0
plt.hist(x1, n_bins, alpha=0.5, label = objectname[0], normed=normed_par)
plt.hist(x2, n_bins, alpha=0.5, label = objectname[1], normed=normed_par)
plt.xlim(left=0, right=200)
plt.xlabel('thickness (µm)')
plt.ylabel('Probability')
plt.legend(loc='upper right')
plt.show()
