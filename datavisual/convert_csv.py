from enum import unique
from posixpath import dirname
import pandas as pd
import numpy as np
import os
import re


csv_file_basic = 'UCSD_data.csv'
current_dir = os.getcwd()
csv_file = os.path.join(current_dir, csv_file_basic)

def count_protocol_numbers(csv_file):
    df = pd.read_csv(csv_file)
    ptc = df.groupby(['ProtocolName']).size()
    # result = list(zip(list(ptc.index), list(ptc)))
    label = list(ptc.index)
    value = list(ptc)
    return label, value


def count_sex_numbers(csv_file):
    df = pd.read_csv(csv_file)
    ptc = df.groupby(['PatientSex']).size()
    
    label = list(ptc.index)
    value = list(ptc)

    if (len(label)==1):
        value.append(0)
        value.append(0)
        if label[0]=='M':
            label.append('F')
            label.append('O')  
        elif label[0] == 'F':
            label.append('M')
            label.append('O')
        elif label[0] == 'O':
            label.append('M')
            label.append('F')

    if (len(label)==2):
        value.append(0)
        if 'M' in label and 'F' in label:
            label.append('O')  
        elif 'O' in label and 'F' in label:
            label.append('M')
        elif 'O' in label and 'M' in label:
            label.append('F')
    return label, value

#label, value = count_protocol_numbers(csv_file)
#print(label)
#print(value)

def count_protocol_numbers_for_all(visible_docs):
    doc_specs = {}

    for doc in visible_docs:
        df = pd.read_csv(doc)
        ptc = df.groupby(['ProtocolName']).size()
        doc_specs[doc] = ptc
    return doc_specs

# def protocol_count(csv_file):
#     label, value = count_protocol_numbers(csv_file)


def sort_dict_by_key(d, reverse = False):
  return dict(sorted(d.items(), reverse = reverse))

def count_age(csv_file):
    df = pd.read_csv(csv_file)
    agelist = df.PatientAge
    number_groups = 0
    # number_groups = agelist.groupby(['PatientAge']).size()
    agelist = list(agelist)
    number_lists = []
    for num in agelist:
        num = int(re.sub("\D", "", num))
        number_lists.append(num)


    
    return number_lists, number_groups
#number_lists, number_groups = count_age(csv_file)


#print('Age List', number_lists)
#print('Number Groups', number_groups)


def stack_plot_data(csv_file, column_name):


    df_original = pd.read_csv(csv_file)
    label, value = count_protocol_numbers(csv_file)
    unique_data = df_original[column_name].unique()
    unique_data = unique_data[np.logical_not(np.isnan(unique_data))]
    print(unique_data)
    # print(label)
    data_proto = {}
    for protocol in label:
        # print('prot',protocol)
        
        df = df_original[df_original['ProtocolName'] == protocol]
        # print(df['ProtocolName'] == protocol)
        # print(df.shape)
        data_assort = df.groupby([column_name]).size()
        
        #unique_data = df_original['EchoTime'].unique()
        # data_proto[protocol] = data_assort

        unit_all_zero = 0
        for data_unit in unique_data:
            if data_unit not in data_assort:
                data_assort[data_unit] = 0
            unit_all_zero += data_assort[data_unit]


        data_assort = sort_dict_by_key(data_assort)
        
        # get rid of legend with all zero values
        if unit_all_zero > 0:
            data_proto[protocol] = data_assort

    return data_proto
#echo_result = stack_plot_data(csv_file, 'EchoTime')
#repete_result = stack_plot_data(csv_file, 'RepetitionTime')
#print(echo_result)
#print(repete_result)


def grouped_protocol_parameters(csv_file):
    df_original = pd.read_csv(csv_file)
    label, value = count_protocol_numbers(csv_file)
    total_grouped_protocol = {}
    for tag in label:
        df = df_original[df_original['ProtocolName'] == tag]
        dict_whole = {}
        list_whole = []
        for i in range(df.shape[0]):
            tuple_unit =()
            tuple_unit =  (df.iloc[i].EchoTime, df.iloc[i].RepetitionTime, df.iloc[i].FlipAngle,\
                 df.iloc[i].SliceThickness, df.iloc[i].SpacingBetweenSlices,df.iloc[i].Rows, df.iloc[i].Columns, df.iloc[i].PixelSpacing0)


            to_string = f'TE: {tuple_unit[0]}, TR: {tuple_unit[1]}, FA: {tuple_unit[2]}, ST: {tuple_unit[3]}, Space: {tuple_unit[4]}, Rows: {tuple_unit[5]}, Cols: {tuple_unit[6]}, PS: {tuple_unit[7]}'
            list_whole.append(to_string)
        # print(np.array(list_whole).unique())
        # unique_list = set(list_whole)
        # print(unique_list)
        for i in list_whole:
            dict_whole[i] = dict_whole.get(i, 0) + 1

        # for i in dict_whole:
        #     dict_whole[i] = dict_whole.get(i, 0) + 1
        total_grouped_protocol[tag] = dict_whole
    return total_grouped_protocol

    print(total_grouped_protocol)
            # print(dict_whole)
        # grouped_set = df.groupby(['EchoTime', 'RepetitionTime']).size()
        # print('GROUPED SET:', grouped_set)


#print('AAAAANSS:',grouped_protocol_parameters(csv_file))


# def repetetion_time(csv_file):


#     df_original = pd.read_csv(csv_file)
#     label, value = count_protocol_numbers(csv_file)
#     unique_repete = df_original['RepetitionTime'].unique()
#     unique_repete = unique_repete[np.logical_not(np.isnan(unique_repete))]
#     print(unique_repete)
#     # print(label)
#     repete_proto = {}
#     for protocol in label:
#         # print('prot',protocol)
        
#         df = df_original[df_original['ProtocolName'] == protocol]
#         # print(df['ProtocolName'] == protocol)
#         # print(df.shape)
#         repete_assort = df.groupby(['RepetitionTime']).size()
        
#         #unique_echo = df_original['EchoTime'].unique()
#         # echo_proto[protocol] = echo_assort

#         for repete_unit in unique_repete:
#             if repete_unit not in repete_assort:
#                 repete_assort[repete_unit] = 0


#         repete_assort = sort_dict_by_key(repete_assort)
        

#         repete_proto[protocol] = repete_assort

#     return repete_proto
# repete_result = repetetion_time(csv_file)
# print(repete_result)

# for things in echo_result:
#     keys = echo_result[things]
#     for item1, item2 in keys:
#         print(item2)


    # print(keys)
    # print(values)
    # print(keys.items)
    # print(values)



def modality_ratio(not_include=None):
    ext = ('.csv')
    total_rows_modality = 0
    modality_distribution = {}
    modality_numbers = {}
    total_CT = 0
    total_MR = 0
    total_EEG = 0
    total_PET = 0
    total_SPECT = 0
    # no_female = 0
    # no_male = 1
    disp_dict = {'Gender_Male':'M','Gender_Female':'F','Gender_Other':'O',
        'Modality_CT':'CT', 'Modality_MR':'MR',
        'Modality_EEG':'EEG', 'Modality_SPECT':'SPECT','Modality_PET':'PET'}
    for files in os.listdir(current_dir):
        if files.endswith(ext):
            df = pd.read_csv(files)
            
            # if not_include:
            #     print(not_include,' not included')

            #     df = df[df['PatientSex'] != not_include]
            #     # print(df.head(5))
            #     print('len df',len(df))
            # print(files)

            if not_include:
                for i in not_include:
                    if i.startswith('Gender_'):
                        df = df[df['PatientSex'] != disp_dict[i]]
                    if i.startswith('Modality_'):
                        df = df[df['Modality'] != disp_dict[i]]


            total_rows_modality += len(df)

            modality_numbers['CT'] = len(df[df['Modality']=='CT'])
            modality_numbers['SPECT'] = len(df[df['Modality']=='SPECT'])
            modality_numbers['PET'] = len(df[df['Modality']=='PET'])
            modality_numbers['EEG'] = len(df[df['Modality']=='EEG'])
            modality_numbers['MR'] = len(df[df['Modality']=='MR'])

            modality_distribution[files] = modality_numbers.copy()

            total_CT += modality_distribution[files].get('CT',0)
            total_MR += modality_distribution[files].get('MR',0)
            total_EEG += modality_distribution[files].get('EEG',0)
            total_PET += modality_distribution[files].get('PET',0)
            total_SPECT += modality_distribution[files].get('SPECT',0)
        # else:
        #     continue
    
    print(total_rows_modality)
    print(modality_distribution)
    print(total_CT)
    print(total_MR)
    print(total_EEG)
    print(total_PET)
    print(total_SPECT)

    return total_rows_modality, modality_distribution, total_CT, total_MR,\
        total_EEG, total_PET, total_SPECT

#total_rows_modality, modality_distribution, total_CT, total_MR,\
#     total_EEG, total_PET, total_SPECT = modality_ratio()

def sex_ratio(not_include=None):
    ext = ('.csv')
    total_rows = 0
    sex_distribution = {}
    sex_numbers = {}
    total_f = 0
    total_m = 0
    total_o = 0
    # no_female = 0
    # no_male = 1
    blank_doc = []
    disp_dict = {'Gender_Male':'M','Gender_Female':'F', 'Gender_Other':'O',
        'Modality_CT':'CT', 'Modality_MR':'MR',
        'Modality_EEG':'EEG', 'Modality_SPECT':'SPECT','Modality_PET':'PET'}
    for files in os.listdir(current_dir):
        if files.endswith(ext):
            df = pd.read_csv(files)


            if not_include:
                print('not_include has', not_include)
                for i in not_include:
                    if i.startswith('Gender_'):
                        df = df[df['PatientSex'] != disp_dict[i]]
                    if i.startswith('Modality_'):
                        df = df[df['Modality'] != disp_dict[i]]


            print(files)
            total_rows += len(df)

            sex_numbers['F'] = len(df[df['PatientSex'].str.contains('F')])
            sex_numbers['M'] = len(df[df['PatientSex'].str.contains('M')])
            sex_numbers['O'] = len(df[df['PatientSex'].str.contains('O')])

            sex_distribution[files] = sex_numbers.copy()

            total_f += sex_distribution[files].get('F',0)
            total_m += sex_distribution[files].get('M',0)
            total_o += sex_distribution[files].get('O',0)
        # else:
        #     continue
    
    for j in sex_distribution:
        # print('printhere',j)
        if sex_distribution[j]['M'] + sex_distribution[j]['F'] + sex_distribution[j]['O'] == 0:
            print('blank data here',j)
            blank_doc.append(j)

    # print('sex_dis',sex_distribution.values())

    print(total_rows)
    print(sex_distribution)
    print(total_f)
    print(total_m)
    return total_rows, sex_distribution, total_f, total_m,total_o, blank_doc

#total_rows, sex_distribution, total_f, total_m, total_o, blank_doc = sex_ratio()


def get_difference(list_a, list_b):
    result = []
    for i in list_a:
        if i not in list_b:
            result.append(i)
    return result

def get_csv_files():
    ext = ('.csv')
    names = []
    for files in os.listdir(current_dir):
        if files.endswith(ext):
            names.append(files)
    return names
