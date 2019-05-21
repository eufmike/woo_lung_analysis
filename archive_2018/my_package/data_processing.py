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


def distance_sum(df, objectname, key1 = 'objectID', key2 = 'Segment ID'):
    combined_data = pd.DataFrame([])  
    # for m in range(2):
    for m in range(len(objectname)):
        segmentname = np.unique(df[key2].loc[df[key1] == objectname[m]])
        print(segmentname)
        # for n in range(5):
        for n in range(len(segmentname)):
            # create temporary data sheet
            print(objectname[m])
            print(segmentname[n])
            temp_data = df.loc[df[key1] == objectname[m]].loc[df[key2] == segmentname[n]]
            
            temp_data_1 = temp_data.iloc[0:(len(temp_data)-1)]
            temp_data_1 = temp_data_1.reset_index()
            # temp_data_1

            temp_data_2 = temp_data.iloc[1:len(temp_data)]
            temp_data_2 = temp_data_2.reset_index()
            # temp_data_2

            # calculate distance between points
            data = temp_data_2.loc[:, ('X Coord', 'Y Coord', 'Z Coord')] - temp_data_1.loc[:, ('X Coord', 'Y Coord', 'Z Coord')]
            data['length'] = np.sqrt(data['X Coord']**2 + data['Y Coord']**2 + data['Z Coord']**2)
            
            # return total length
            total_seg_length = sum(data['length'])
            
            temp_data_result = {'objectID': [objectname[m]], \
                                'Segment ID': [segmentname[n]], \
                                'seg_length': [total_seg_length]}
            temp_data_result_df = pd.DataFrame(temp_data_result)
            combined_data = combined_data.append(temp_data_result_df, ignore_index = True)
            
    return combined_data