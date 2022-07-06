from enum import unique
from re import sub
from dicom_csv import join_tree, order_series, stack_images
from pydicom import dcmread
from pathlib import Path
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

currfoldername = os.getcwd()

subfolders = [ f.path for f in os.scandir(currfoldername) if f.is_dir() ]
# print(subfolders)

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

all_dirs = fast_scandir(currfoldername)
only_sub_dirs = [ele for ele in all_dirs if ele not in subfolders]
# print(only_sub_dirs)
# print(len(only_sub_dirs))
# print()
# full_list = pd.DataFrame()

for folders in only_sub_dirs:
    meta = join_tree(folders, verbose=2)
    full_list = meta.iloc[[-1]]
    break

full_list['Folder'] = None
full_list['FakeID'] = None
for folders in tqdm(only_sub_dirs):
    meta = join_tree(folders, verbose=2)
    # TODO: GET ONE ROW PER FOLDER AND CONCAT INTO DF
    # full_list
    one_row = meta.iloc[[-1]]
    one_row['Folder'] = folders
    one_row['FakeID'] = os.path.basename(os.path.dirname(folders))
    full_list = pd.concat([full_list, one_row])


full_list = full_list.iloc[1:]
# print(full_list)

csvname = 'parsed_csv_demo.csv'
full_list.to_csv(csvname)

###
import csv
import json

csvfile = open(csvname, 'r')
jsonfile = open('file.json', 'w')


reader = csv.DictReader(csvfile)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')



# fileread = dcmread(filename)
# print(fileread)
# pddata = pd.DataFrame(fileread)


# meta = join_tree(filename, verbose=2)

# print(meta)

# 2. Select series to load
# uid = '1.3.12.2.1107.5.2.43.166239.2021110810064442568387627.0.0.0' # unique identifier of a series you want to load,
#             # you could list them by `meta.SeriesInstanceUID.unique()`
# # uid = uid.tolist()
# # del uid[0]
# # uid = np.array(uid)

# series = meta.query("SeriesInstanceUID==@uid")
# # 3. Read files & combine them into a single volume
# images2d = [dcmread(folder / row[1].PathToFolder / row[1].FileName) for row in series.iterrows()] 
# image3d = stack_images(order_series(images2d))

# print(image3d)