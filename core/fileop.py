import os, sys, re

def ListFiles(path, extension = None):
    # ListFiles creates a list of files from given dir and extension and exclude hidden files
    # subfolders is included. 
	filelist = []
	fileabslist = []
	for directory, dir_names, file_names in os.walk(path):
		
		for file_name in file_names:
			if (not file_name.startswith('.')) & (file_name.endswith(extension)):
				file_name_base = file_name.replace(extension, '')
				filepath_tmp =  os.path.join(directory, file_name)
				filelist.append(file_name_base)
				fileabslist.append(filepath_tmp)
	
	return filelist, fileabslist

def DirCheck(targetpaths):
	"""
	dircheck checks the target folder and create the folder if it does not exist.
	targetdirlist: list of folderpath
	"""
	# print(type(targetpaths))
	if isinstance(targetpaths, str): 
		# print(os.path.exists(targetpaths))
		if not os.path.exists(targetpaths):
			os.makedirs(targetpaths)
	elif isinstance(targetpaths, list): 
		for path in targetpaths:
			if not os.path.exists(path):
				os.makedirs(path)

def SplitAll(path):
    # SplitAll splits file path into individual string. 
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def SortByFolder(ipfilepaths, inputpattern = None):    
    # input
    # 'Tile_'

    class imgfile:
        def __init__(self, filename, filepath, index):
            self.filename = filename
            self.filepath = filepath
            self.index = index

    cleaned_filelist = [] 
    for ipfilepath in ipfilepaths:
        if inputpattern is not None: 
            x = re.search(inputpattern, ipfilepath) # search the string by the given pattern
            try: 
                ipfilepath_tmp = x.group(0)
                file_temp = SplitAll(ipfilepath) 
                filename = os.path.split(ipfilepath)[1]
                cleaned_filelist.append(imgfile(filename, ipfilepath, int(file_temp[-2])))          
            except AttributeError:
                found = ''
        else:
            ipfilepath_tmp = ipfilepath
            file_temp = SplitAll(ipfilepath_tmp) 
            filename = os.path.split(ipfilepath_tmp)[1]
            cleaned_filelist.append(imgfile(filename, ipfilepath_tmp, int(file_temp[-2])))        
        
    cleaned_filelist.sort(key =lambda x: x.index)

    return cleaned_filelist

def ListFolders(path):
	dirlist = []
	for dir_name in os.listdir(path):
		if (not dir_name.startswith('.')):
			dirlist.append(dir_name)
	return dirlist
