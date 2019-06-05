import xml.etree.ElementTree as etree
import time
from tqdm import tqdm
import pandas as pd

def MSXmlReader(path):
    # xml loading
    start = time.time()
    xml = etree.parse(path)
    root = xml.getroot()
    print(root)
    end = time.time()
    print('loading time: {}'.format(end- start))

    # parse xml    
    ns = {
    'ss':"urn:schemas-microsoft-com:office:spreadsheet"
    }

    vardic = {}
    for ws in root[1:]:
        ws_attrib = ws.attrib
        ws_name = ws.attrib['{'+ns['ss']+'}Name']
        ws_name = ws_name.lower()
        # print(ws_name)

        header = []
        tb = ws[0]
        # print(len(tb))
        for cell in tb[0]:
            header.append(cell[0].text)
        # print(header)
        var_count = len(header)
        # print('variable count: {}'.format(var_count))
        
        data_dic = {}
        for r_idx in tqdm(range(len(tb))[1:]):
            # print(r_idx)
            row = tb[r_idx]
            content = []
            for cell in row:
                content.append(cell[0].text)
            # print(content)
            data_dic[str(r_idx-1)] = content
        
        # create dataframe for each variable
        exec("df_%s = pd.DataFrame.from_dict(data_dic, orient = 'index', columns=header)"%(ws_name))
        
        exec("vardic['%s']=df_%s"%(ws_name, ws_name))

    return(vardic)