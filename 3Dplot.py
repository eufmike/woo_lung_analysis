import os, sys
import numpy as np
import pandas as pd
from core.fileop import DirCheck
from core.msxml import MSXmlReader
from mayavi import mlab
from matplotlib import cm

# function to get unique values 
def unique(list1): 
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x)
    return unique_list

def Cmap2RGB(cmap_name):
    cmap = cm.get_cmap(cmap_name)
    cmaplist = [cmap(i) for i in range(cmap.N)]
    return cmaplist

ippath = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/csv/2_normoxia_01/'
var = ['df_nodes', 'df_points', 'df_segments']
fl_names = ['nodes.csv', 'points.csv', 'segments.csv']

for idx, val in enumerate(fl_names):
    exec("%s = pd.read_csv(os.path.join(ippath, '%s'))"%(var[idx], val))

# plot points
point_x = df_points['X Coord']
point_y = df_points['Y Coord']
point_z = df_points['Z Coord']

point_s = [50.0] * len(point_x)
scale_factor = 1

p1 = mlab.points3d(point_x, point_y, point_z, point_s, 
                    scale_factor = scale_factor, 
                    color = (200/255, 0.0, 0.0))

groups = unique(list(df_nodes['Coordination Number']))
print(groups)

#  get RGB color
cmapRGB = Cmap2RGB('Set3')
print(cmapRGB)

for idx, group in enumerate(groups):
    df_nodes_tmp = df_nodes[df_nodes['Coordination Number'] == group]
    # plot nodes
    node_x = df_nodes_tmp['X Coord']
    node_y = df_nodes_tmp['Y Coord']
    node_z = df_nodes_tmp['Z Coord']

    node_s = [50.0]*len(node_x)
    scale_factor = 1.5

    p2 = mlab.points3d(node_x, node_y, node_z, node_s, 
                        scale_factor = scale_factor, 
                        color = cmapRGB[idx][:3])

mlab.show()
