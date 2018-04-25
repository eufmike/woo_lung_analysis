import numpy as np
import pandas as pd
import os

def combine_point_seg(data_point, data_seg):
    combined_data = pd.DataFrame([])
    for m in [0]:
    # for m in range(data_seg.shape[0]):
        # extract step points in segment
        print(m)
        data_point_ref = data_seg['Point IDs'][m]
        data_point_ref = data_point_ref.split(sep = ',')
        data_point_ref = pd.DataFrame(data_point_ref, columns= ['Point ID'])
        
        data_point_ref['Segment ID'] = data_seg['Segment ID'][m]
        data_point_ref['Node ID #1'] = data_seg['Node ID #1'][m]
        data_point_ref['Node ID #2'] = data_seg['Node ID #2'][m]
        data_point_ref['objectID'] = data_seg['objectID'][m]

        
        # change type for float64
        data_point_ref['Point ID'] = pd.to_numeric(data_point_ref['Point ID'])
        
        # merge with ddata_point and data_seg
        data_merge = pd.merge(data_point_ref, data_point, on=['objectID','Point ID'])
        '''
        # add object ID
        object_ID = [m+1] * len(data_steps_series)
        object_ID_dict = {'object ID':object_ID}
        object_ID_df = pd.DataFrame(object_ID_dict, dtype='category') 
        '''
        # append the data sheet
        combined_data = combined_data.append(data_merge, ignore_index = True)
        
        # remove variable
        del data_merge

    return [data_seg['Segment ID'][m], data_seg['Node ID #1'][m], data_seg['Node ID #2'][m], combined_data]

def listdir_nohidden(path):
    path_list = []
    for f in os.listdir(path):
        if (not f.startswith('.') and not f.startswith('~')):
            path_list.append(f)
    return path_list   