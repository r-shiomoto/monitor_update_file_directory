# A script to monitor the update of  both files and a directory using the modified date in the file and the number of the files in the directory.
# If you want to run this script, you may need to install plyer, which is a popup notification library.

# Import libraries

import os
from plyer import notification
import datetime as dt
import time

# Initialize variables.

target = input('Enter the path to a file or a directory that you want to monitor.')
sleep = 10 # waiting seconds


# Define functions

def rtn_modified_time(file_path: str) -> dt.datetime:
    """Given a file path, this function returns the modification date as a datetime type.
    
    Parameters
    ----------
    file_path: str
        file path.
        
    Return
    ------
    modified_time: dt.datetime
        the modification date as a datetime type.
    
    """
    
    file_info = os.stat(file_path)
    modified_time = dt.datetime.fromtimestamp(file_info.st_mtime)
    return modified_time

def notificate_from_dts(dt1: dt.datetime, dt2: dt.datetime, file: str) -> bool:
    """Function that receives two datetime.datetime types and file paths and notifies if they are different.
    
    Parameters
    ----------
    dt1: dt.datetime
        A datetime type assuming original.
    dt2: dt.datetime
        A datetime type assuming modified.
    file: str
        A modified file.
        
    Return
    ------
    bool
        It become a flag of breaking loop.
    
    """
    if dt1 != dt2:
        notification.notify(
            title="【Notification】",
            message=f"{file} is modified.",
            app_name="App name",
            app_icon="notification.ico",
            timeout=30)
        return True
    else:
        return False


# Start monitoring.

if os.path.isfile(target): # When monitoring files.
    file_path = target
    modified_dt1 = rtn_modified_time(file_path) # Get the file modification date at the time of loading.
    while True:
        file = os.path.basename(file_path)
        modified_dt2 = rtn_modified_time(file_path)
        flag = notificate_from_dts(modified_dt1, modified_dt2, file)
        if flag:
            print(f'{file} is modified at {modified_dt2.strftime("%Y/%m/%d %H:%M:%S")}')
            break
        time.sleep(sleep)

else: # When monitoring files.
    dir_path = target
    time_dic1 = {} # key is file name, value is the file modification date.
    original_files = [] # List of original files.
    for file in os.listdir(dir_path):
        time_dic1[file] = rtn_modified_time(dir_path + f'\\{file}')
        original_files.append(file)
        
    while True:
        flag_while = False
        files = os.listdir(dir_path)
        
        if len(set(original_files)) != len(set(files)): # When number of files in directory changes.
            if len(set(original_files)) > len(set(files)):
                msg = 'removed'
            elif len(set(original_files)) < len(set(files)):
                msg = 'added'
            flag_while = True
            diff_file = list(set(original_files) ^ set(files))
            notification.notify(
                title="【Notification】",
                message=f"{diff_file[0]} is {msg}.",
                app_name="App name",
                app_icon="notification.ico",
                timeout=30)
            print(f'{diff_file[0]} is {msg} at {dt.datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
            break
            
        for file in files: # When individual files in a folder are updated.
            modified_dt1 = time_dic1[file]
            modified_dt2 = rtn_modified_time(dir_path + f'\\{file}')
            flag = notificate_from_dts(modified_dt1, modified_dt2, file)
            if flag:
                flag_while = True
                print(f'{file} is modified at {modified_dt2.strftime("%Y/%m/%d %H:%M:%S")}')
                break
        
        if flag_while:
            break
            
        time.sleep(sleep)

_=input('Enter any key to close this window.') # To stay at the command prompt.