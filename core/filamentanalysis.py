import numpy as np
import pandas as pd
import os
from tqdm import tqdm

def SegStats(df_points, df_segments):
    # SegStats return the tola length and average thickness for each segments
    seg_dist_list = []
    seg_thickness_list = []
    
    for m in tqdm(range(len(df_segments))):
        # extract step points in segment
        point_ref = df_segments['Point IDs'][m]
        point_ref = point_ref.split(sep = ',')
        point_ref = list(map(int, point_ref)) # convert to integer

        # calculate total distance         
        point_1 = df_points.iloc[point_ref[:-1], :]
        point_2 = df_points.iloc[point_ref[1:], :]
        
        point_1_xyz = np.array(point_1[['X Coord', 'Y Coord', 'Z Coord']])
        point_2_xyz = np.array(point_2[['X Coord', 'Y Coord', 'Z Coord']])
        delta = point_2_xyz - point_1_xyz
        square = np.square(delta)
        dist = np.sum(np.sqrt(np.sum(square, axis = 1)))
        seg_dist_list.append(dist) 

        # calculate average thickness
        point = df_points.iloc[point_ref, :]
        thickness_avg = np.mean(point['thickness'])
        seg_thickness_list.append(thickness_avg)

    df = df_segments
    df['length'] = seg_dist_list
    df['thickness'] = seg_thickness_list

    return df


def BranchLabel(df_nodes, df_segments):
    df_nodes_tmp = df_nodes
    df_segments_tmp = df_segments
    print(df_nodes_tmp.dtypes)
    print(df_segments_tmp.dtypes)

    branch_lvl = {}
    ls_done = {}

    pbar1 = tqdm(total = len(df_nodes), desc = 'BranchLabel')

    i = 1
    branch_label = 0 
    while i > 0:
    # for idx in range(1):
        first_node = df_nodes_tmp.iloc[0, 0].item()
        print(first_node)
        print(first_node in df_nodes_tmp['Node ID'])

        ls_done_tmp, branch_lvl_tmp = BranchFinder(df_nodes_tmp, df_segments_tmp)            
        branch_lvl[branch_label] = branch_lvl_tmp 
        
        ls_done_tmp.sort()
        ls_done[branch_label] = ls_done_tmp
        
        print(ls_done_tmp)

        df_nodes_tmp = df_nodes_tmp.drop(ls_done_tmp)

        # display(df_nodes_tmp)
        # df_nodes_tmp = df_nodes_tmp.reset_index(drop=True)

        pbar1.update(len(ls_done_tmp))
        print('df length: {}'.format(len(df_nodes_tmp)))
        
        i = len(df_nodes_tmp)
        # if len(df_nodes_tmp) == 0:
        #    break

        branch_label += 1

    pbar1.close
    
    return(ls_done, branch_lvl)

def BranchFinder(df_nodes_tmp, df_segments_tmp):
    
    parents = df_nodes_tmp.iloc[0]['Node ID']
    parents = [int(parents)]
    
    
    #print(type(parents))

    ls_done = []
    branch_lvl = []

    i = 1
    level = 0
    
    # pbar2 = tqdm(total = len(df_nodes_tmp), desc = 'BranchFinder')
    
    while i > 0:
    # for level in range(10):
        print('level: {}'.format(level))
        print('parents:{}'.format(parents))
        ls_done = ls_done + parents

        childrens = []
              
        if len(parents) > 1:
            branch_lvl.append(level) 

        for parent in parents:
            # print(int(parent))
            
            # print(df_nodes_tmp.iloc[parent])
            # node_ref = df_nodes_tmp.loc[df_nodes_tmp['Node ID'] == parent, 'Node ID']
            # print(len(df_segments_tmp))
            # print(parent in list(df_nodes_tmp['Node ID']))
            node_ref = [x for x in list(df_nodes_tmp['Node ID']) if x == parent][0]
            
            # node_ref = node_ref.values[0]
            # print(node_ref)

            if parent not in list(df_nodes_tmp['Node ID']):
                print()
            '''
            if parent != node_ref:
                print(parent)
                print(node_ref)
                break
            '''

            n1 = list(df_segments_tmp['Node ID #1'] == node_ref)
            n2 = list(df_segments_tmp['Node ID #2'] == node_ref)

            selection = np.logical_or(n1, n2)

            df_seg_selected = df_segments_tmp.loc[selection] 
            # print(df_seg_selected)
        
            allnode = list(df_seg_selected['Node ID #1']) + list(df_seg_selected['Node ID #2'])
            # print(allnode)

            children = list(np.setdiff1d(allnode, ls_done))
        
            
            childrens = childrens + children 
            
            df_segments_tmp = df_segments_tmp.loc[np.invert(selection)]

        # print('childrens: {}'.format(childrens))
        childrens = list(np.unique(childrens))
        parents = childrens
        
        level += 1
        i = len(childrens)

    return(ls_done, branch_lvl)        
    







def CombinePointSeg(df_points, df_segments):
    # constructing
    combined_data = pd.DataFrame([])

    for m in range(df_segments.shape[0]):
        # extract step points in segment
        print(m)
        point_ref = df_segments['Point IDs'][m]
        point_ref = point_ref.split(sep = ',')
        df_point_ref = pd.DataFrame(point_ref, columns= ['Point ID'])

        df_point_ref['Segment ID'] = df_segments['Segment ID'][m]
        df_point_ref['Node ID #1'] = df_segments['Node ID #1'][m]
        df_point_ref['Node ID #2'] = df_segments['Node ID #2'][m]
        df_point_ref['Subsegment ID'] = pd.Series(list(range(0, len(point_ref)+1)))
        # display(df_point_ref)

        # change type for int64
        df_point_ref['Point ID'] = df_point_ref['Point ID'].astype('int64')
        
        print(df_point_ref.dtypes)

        # merge with df_points and df_segments
        df_merge = pd.merge(df_point_ref, df_points, on='Point ID')
        display(df_merge)

        '''
        # add object ID
        object_ID = [m+1] * len(data_steps_series)
        object_ID_dict = {'object ID':object_ID}
        object_ID_df = pd.DataFrame(object_ID_dict, dtype='category') 
        '''
        '''
        # append the data sheet
        combined_data = combined_data.append(data_merge, ignore_index = True)
        
        # remove variable
        del data_merge
        '''
        break

    #return [data_seg['Segment ID'][m], data_seg['Node ID #1'][m], data_seg['Node ID #2'][m], combined_data]

def ListdirNohidden(path):
    path_list = []
    for f in os.listdir(path):
        if (not f.startswith('.') and not f.startswith('~')):
            path_list.append(f)
    return path_list   


def DistanceSum(df, objectname, key1 = 'objectID', key2 = 'Segment ID'):
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


