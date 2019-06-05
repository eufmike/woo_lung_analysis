#%% [markdown]
# Use python built-in xml module to parse msxml file
# Results turn to be slow
#%%
import os, sys, re, io
import matplotlib
import numpy as np
import pandas as pd
import xml.etree.ElementTree as etree
from tqdm import tqdm

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/lung_vs_002.xml'

#%%
tree = etree.parse(path)
root = tree.getroot()
print(root)

#%%
ns = {
    'ss':"urn:schemas-microsoft-com:office:spreadsheet",
    'html':"http://www.w3.org/TR/REC-html40"
    }

for ws in root.findall('ss:Worksheet', ns):
    print(ws)
    ws_name = ws.attrib
    ws_name_text = ws_name['{'+ ns['ss']+'}Name']
    print(ws_name_text)
    for table in ws.findall('ss:Table', ns):
        
        for r in table.findall('ss:Row', ns)[:1]:
            header = []
            for c in r.findall('ss:Cell', ns):
                data = c.find('ss:Data', ns)
                #print(data.text)
                header.append(data.text)    
            # print(header)
        
        exec("df_%s = pd.DataFrame(columns=header)"%(ws_name_text))
        
        content = table.findall('ss:Row', ns)[1:]
        for r_idx in tqdm(range(len(content))):
            row = []
            r_value = content[r_idx]
            for c in r_value.findall('ss:Cell', ns):
                data = c.find('ss:Data', ns)
                #print(data.text)
                row.append(data.text)    
            # print(row)
            
            exec("df_%s.loc[r_idx] = row"%(ws_name_text))
            

    # exec("df_%s = []")  


#%%
# print(df_Nodes)
# print(df_Points)

#%% [markdown]
# testing parse through lxml
# in the middle of it (almost give up)
#%%
from lxml import etree
import os, sys, re, io
import matplotlib
import numpy as np
import pandas as pd
from tqdm import tqdm

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/lung_vs_002.xml'

#%%
xml = etree.parse(path)
root = xml.getroot()
print(root)
# print(root.items())
# print(root.keys())
# print(root.get('version', ''))


#%% 
'''
for worksheet in root.getchildren():
    print('worksheet')
    # print(worksheet.tag)
    print(worksheet.attrib)
    
    for table in worksheet.getchildren():
        print('table')
        print(table.tag)
'''
#%%
ns = {
    'ss':"urn:schemas-microsoft-com:office:spreadsheet",
    'html':"http://www.w3.org/TR/REC-html40"
    }

for worksheet in root.findall('ss:Worksheet', ns):
    print('worksheet')
    # print(worksheet.tag)
    print(worksheet.attrib)
    
    ws_name = worksheet.attrib
    ws_name_text = ws_name['{'+ ns['ss']+'}Name']

    header = []
    data = []
    
    for table in worksheet.findall('ss:Table', ns):
        print(table.tag)
    
        for row in table.findall('ss:Row', ns)[0]:
            print(row.tag)
            
            for cell in row.getchildren():
                print(cell.tag)
                
                data = cell.getchildren()
                print(data.text)
                header.append(data.text)
                
    print(header)
    exec("df_%s = pd.DataFrame(columns=header)"%(ws_name_text))
        
    '''
    content = worksheet.findall('ss:Table', ns)[1:]
    
    r_value = []
    
    for r_idx in range(len(content)): 
        row = content[r_idx]
        
        for cell in row.getchildren():
            # print(cell.tag) 
            data = cell.getchildren()[0]
            print(data.text)
            r_value.append(data.text)
    '''
    break

#%%
import os, sys, re, io
import matplotlib
import numpy as np
import pandas as pd
import xml.etree.ElementTree as etree
from tqdm import tqdm

#%%
path = '/Volumes/LaCie_DataStorage/Woo-lungs/2019/data/normoxia/lung_vs_002.xml'
xml = etree.parse(path)
root = xml.getroot()
print(root)

#%%
ns = {
    'ss':"urn:schemas-microsoft-com:office:spreadsheet",
    'html':"http://www.w3.org/TR/REC-html40"
    }

for ws in root[1:]:
    ws_attrib = ws.attrib
    ws_name = ws.attrib['{'+ns['ss']+'}Name']
    print(ws_name)

    header = []
    tb = ws[0]
    # print(len(tb))
    for cell in tb[0]:
        header.append(cell[0].text)
    print(header)
    var_count = len(header)
    print('variable count: {}'.format(var_count))
    
    data_dic = {}
    for r_idx in tqdm(range(len(tb))[1:10]):
        # print(r_idx)
        row = tb[r_idx]
        content = []
        for cell in row:
            content.append(cell[0].text)
        # print(content)
        data_dic[str(r_idx)] = content
    
    exec("df_%s = pd.DataFrame.from_dict(data_dic, orient = 'index', columns=header)"%(ws_name))

#%%
print(df_Nodes)

#%%
