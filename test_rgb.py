#%%
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from colorspacious import cspace_converter
from collections import OrderedDict

cmaps = OrderedDict()

#%%
def Cmap2RGB():
    cmap = cm.get_cmap('Set3')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    print(cmaplist)


#%%
Cmap2RGB()

