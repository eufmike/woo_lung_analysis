#%% [markdown]

#%%
% load_ext autoreload
%autoreload 2
import os, sys, re, io
import matplotlib
import numpy as np
import pandas as pd
import xml.etree.ElementTree as etree
from tqdm import tqdm
import time
from core.fileop import DirCheck
from core.msxml import MSXmlReader

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/lung_vs_002.xml'

csv_all = MSXmlReader(path)

#%%
display(csv_all['nodes'])

#%%
oppath = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/' 
for key, value in csv_all.items():
    opfilename = 'lung_vs_002_' + key + '.csv'
    opfilepath = os.path.join(oppath, opfilename)
    value.to_csv(opfilepath, index = False)

