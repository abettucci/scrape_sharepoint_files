from office365_api import SharePoint
import re
import sys, os
from pathlib import PurePath

# 1 args = SharePoint folder name. May include subfolders YouTube/2022
FOLDER_NAME = sys.argv[1]
# 2 args = locate or remote folder_dest
# FOLDER_DEST = sys.argv[2]
# 3 args = SharePoint file name. This is used when only one file is being downloaded
# If all files will be downloaded, then set this value as "None"
# FILE_NAME = sys.argv[3]
# 4 args = SharePoint file name pattern
# If no pattern match files are required to be downloaded, then set this value as "None"
# FILE_NAME_PATTERN = sys.argv[4]

def save_file(file_n, file_obj):
    file_dir_path = PurePath(FOLDER_DEST, file_n)
    with open(file_dir_path, 'wb') as f:
        f.write(file_obj)

def create_dir(path):
    dir_path = PurePath(FOLDER_DEST, path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_file(file_n, folder):
    file_obj = SharePoint().download_file(file_n, folder)
    save_file(file_n, file_obj)

def read_files(folder):
    files_list = SharePoint()._get_files_list(folder)
    print(files_list)

def get_files(folder):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        get_file(file.name, folder)

def get_files_by_pattern(keyword, folder):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        if re.search(keyword, file.name):
            get_file(file.name, folder)

# def upload_files(folder, keyword=None):
#     file_list = get_list_of_files(folder)
#     for file in file_list:
#         if keyword is None or keyword == 'None' or re.search(keyword, file[0]):
#             file_content = get_file_content(file[1])
#             SharePoint().upload_file(file[0], SHAREPOINT_FOLDER_NAME, file_content)

def get_list_of_files(folder):
    file_list = []
    folder_item_list = os.listdir(folder)
    for item in folder_item_list:
        item_full_path = PurePath(folder, item)
        if os.path.isfile(item_full_path):
            file_list.append([item, item_full_path])
    return file_list

# read files and return the content of files
def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

def get_folders(folder):
    l = []
    folder_obj = SharePoint().get_folder_list(folder)
    for subfolder_obj in folder_obj:
        subfolder = '/'.join([folder, subfolder_obj.name])
        l.append(subfolder)
    return l

def get_latest_file(folder, folder_dest):
    file_name, content = SharePoint().download_latest_file(folder)
    save_file(file_name, content, folder_dest)

def get_properties_by_folder(folder):
    files_properties = SharePoint().get_file_properties_from_folder(folder)
    print('File count:', len(files_properties))
    for file in files_properties:
        print(file)

if __name__ == '__main__':
    read_files(FOLDER_NAME)
    # if FILE_NAME != 'None':
    #     get_file(FILE_NAME, FOLDER_NAME)
    # elif FILE_NAME_PATTERN != 'None':
    #     get_files_by_pattern(FILE_NAME_PATTERN, FOLDER_NAME)
    # else:
    #     get_files(FOLDER_NAME)
