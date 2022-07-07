from contextlib import redirect_stdout
import imp
from multiprocessing import Event
from django.shortcuts import render, redirect
from .models import CheckboxData, CountryData, Summarized_Dataset
from .forms import CountryDataForm, Summarized_DatasetForm
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from datavisual.convert_csv import csv_file, get_difference, get_csv_files
from datavisual.convert_csv import sex_ratio
from datavisual.convert_csv import modality_ratio
from datavisual.convert_csv import count_protocol_numbers, count_protocol_numbers_for_all, count_sex_numbers,stack_plot_data, grouped_protocol_parameters
from .models import CheckboxData
import json
# Create your views here.

def home(request):
    return HttpResponse('Home Page')

# def admin_approval(request):
#     return render()

def UCSD_data(request):
    file_name = 'UCSD_data.csv'

    json_name = file_name.replace('.csv', '.json')
    json_name = os.path.join('cache', json_name)
    curr_dir = os.getcwd()
    json_dir = os.path.join(curr_dir, json_name)

    if os.path.exists(json_dir):
        f = open(json_dir)
        context = json.load(f)
        print('##############$$$$$$$$$$$$$ file bypass')
        return render(request, 'dashboard/UCSD_data.html', context)

    label_protocol, value_protocol = count_protocol_numbers(file_name)
    label_sex, value_sex = count_sex_numbers(file_name)

    echo_data = stack_plot_data(file_name, 'EchoTime')
    repetetion_data = stack_plot_data(file_name, 'RepetitionTime')
    flipangle_data = stack_plot_data(file_name, 'FlipAngle')
    slicethickness_data = stack_plot_data(file_name, 'SliceThickness')
    spacingbetweenslices_data = stack_plot_data(file_name, 'SpacingBetweenSlices')
    row_data = stack_plot_data(file_name, 'Rows')
    column_data = stack_plot_data(file_name, 'Columns')
    pixelspacing0_data = stack_plot_data(file_name, 'PixelSpacing0')
    total_grouped_protocol = grouped_protocol_parameters(file_name)


    echo_names = [i for i in echo_data]
    repetetion_names = [i for i in repetetion_data]
    flipangle_names = [i for i in flipangle_data]
    slicethickness_names = [i for i in slicethickness_data]
    spacingbetweenslices_names = [i for i in spacingbetweenslices_data]
    row_names = [i for i in row_data]
    column_names = [i for i in column_data]
    pixelspacing0_names = [i for i in pixelspacing0_data]


    protocol_plot_points = {}
    gender_plot_points = {}
    echo_plot_points = {}
    repetition_plot_points = {}
    flipangle_plot_points = {}
    slicethickness_plot_points = {}
    spacingbetweenslices_plot_points = {}
    row_plot_points = {}
    column_plot_points = {}
    pixelspacing0_plot_points = {}

    for count, label_name in enumerate(label_protocol):
        point_dict = {}
        point_dict[count] = value_protocol[count]
        protocol_plot_points[label_name] = point_dict

    print('formatted PROTOCOL:', protocol_plot_points)

    for count, label_name in enumerate(label_sex):
        point_dict = {}
        point_dict[count] = value_sex[count]
        gender_plot_points[label_name] = point_dict


    for i in pixelspacing0_names:
        if dict(pixelspacing0_data[i]):
            pixelspacing0_plot_points[i] = dict(pixelspacing0_data[i])

    for i in row_names:
        if dict(row_data[i]):
            row_plot_points[i] = dict(row_data[i])

    for i in column_names:
        if dict(column_data[i]):
            column_plot_points[i] = dict(column_data[i])

    for i in spacingbetweenslices_names:
        if dict(spacingbetweenslices_data[i]):
            spacingbetweenslices_plot_points[i] = dict(spacingbetweenslices_data[i])


    for i in slicethickness_names:
        if dict(slicethickness_data[i]):
            slicethickness_plot_points[i] = dict(slicethickness_data[i])

    for i in flipangle_names:
        if dict(flipangle_data[i]):
            flipangle_plot_points[i] = dict(flipangle_data[i])

    for i in repetetion_names:
        if dict(repetetion_data[i]):
            repetition_plot_points[i] = dict(repetetion_data[i])

    for i in echo_names:
        if dict(echo_data[i]):
            echo_plot_points[i] = dict(echo_data[i])

    

    print('TTTTrial', spacingbetweenslices_plot_points)

    print('TE:', echo_plot_points)
    print('TR:', repetition_plot_points)
    print('FA:', flipangle_plot_points)

    csv_names = get_csv_files()
    visible_doc = csv_names
    count_protocol_numbers_for_all(visible_doc)

    print('aaa',label_protocol)
    print('bbb',value_protocol)
    print('ccc',label_sex)
    print('ddd',value_sex)

    parameter_list = {'TE':echo_plot_points,\
         'TR':repetition_plot_points, 'FA':flipangle_plot_points,\
              'ST':slicethickness_plot_points, 'SliceSpacing':spacingbetweenslices_plot_points,\
                   'Rows':row_plot_points, 'Cols':column_plot_points
                   , 'PixelSpacing':pixelspacing0_plot_points}
    zero_item_out = {}
    for item in parameter_list:
        
        value_item = parameter_list[item]
        for x_1, y_1 in value_item.items():
            value_unit = value_item[x_1]
            dic_out = {}
            for x, y in value_unit.items():
                if y != 0:
                    dic_out[x] = y
            value_item[x_1] = dic_out
        zero_item_out[item] = value_item
    print(zero_item_out)            
    # print('param_list', parameter_list)
    parameter_list = zero_item_out
    protocol_dictionary = {}
    for i in label_protocol:
        para_dict = {}
        for j in parameter_list:
            if i in parameter_list[j]:
                
                para_dict[j] = parameter_list[j][i]

        protocol_dictionary[i] = para_dict
    # print(protocol_dictionary)





    context = {
        'label_protocol':label_protocol,
        'value_protocol':value_protocol,
        'label_sex':label_sex,
        'value_sex':value_sex,
        'echo_plot_points':echo_plot_points,
        'repetition_plot_points':repetition_plot_points,
        'flipangle_plot_points':flipangle_plot_points,
        'slicethickness_plot_points':slicethickness_plot_points,
        'spacingbetweenslices_plot_points':spacingbetweenslices_plot_points,
        'row_plot_points':row_plot_points,
        'column_plot_points':column_plot_points,
        'pixelspacing0_plot_points': pixelspacing0_plot_points,
        'protocol_plot_points':protocol_plot_points,
        'gender_plot_points': gender_plot_points,
        'total_grouped_protocol':total_grouped_protocol,
        'protocol_dictionary':protocol_dictionary,
        
    }

    
    with open(json_dir,'w') as context_dumped:
        json.dump(context, context_dumped)

    return render(request, 'dashboard/UCSD_data.html', context)

def UCSD_data_fake(request):
    file_name = 'UCSD_data_fake.csv'


    json_name = file_name.replace('.csv', '.json')
    json_name = os.path.join('cache', json_name)
    curr_dir = os.getcwd()
    json_dir = os.path.join(curr_dir, json_name)


    if os.path.exists(json_dir):
        f = open(json_dir)
        context = json.load(f)
        print('##############$$$$$$$$$$$$$ file bypass')
        return render(request, 'dashboard/UCSD_data.html', context)



    label_protocol, value_protocol = count_protocol_numbers(file_name)
    label_sex, value_sex = count_sex_numbers(file_name)

    echo_data = stack_plot_data(file_name, 'EchoTime')
    repetetion_data = stack_plot_data(file_name, 'RepetitionTime')
    flipangle_data = stack_plot_data(file_name, 'FlipAngle')
    slicethickness_data = stack_plot_data(file_name, 'SliceThickness')
    spacingbetweenslices_data = stack_plot_data(file_name, 'SpacingBetweenSlices')
    row_data = stack_plot_data(file_name, 'Rows')
    column_data = stack_plot_data(file_name, 'Columns')
    pixelspacing0_data = stack_plot_data(file_name, 'PixelSpacing0')
    total_grouped_protocol = grouped_protocol_parameters(file_name)


    echo_names = [i for i in echo_data]
    repetetion_names = [i for i in repetetion_data]
    flipangle_names = [i for i in flipangle_data]
    slicethickness_names = [i for i in slicethickness_data]
    spacingbetweenslices_names = [i for i in spacingbetweenslices_data]
    row_names = [i for i in row_data]
    column_names = [i for i in column_data]
    pixelspacing0_names = [i for i in pixelspacing0_data]


    protocol_plot_points = {}
    gender_plot_points = {}
    echo_plot_points = {}
    repetition_plot_points = {}
    flipangle_plot_points = {}
    slicethickness_plot_points = {}
    spacingbetweenslices_plot_points = {}
    row_plot_points = {}
    column_plot_points = {}
    pixelspacing0_plot_points = {}

    for count, label_name in enumerate(label_protocol):
        point_dict = {}
        point_dict[count] = value_protocol[count]
        protocol_plot_points[label_name] = point_dict

    print('formatted PROTOCOL:', protocol_plot_points)

    for count, label_name in enumerate(label_sex):
        point_dict = {}
        point_dict[count] = value_sex[count]
        gender_plot_points[label_name] = point_dict


    for i in pixelspacing0_names:
        if dict(pixelspacing0_data[i]):
            pixelspacing0_plot_points[i] = dict(pixelspacing0_data[i])

    for i in row_names:
        if dict(row_data[i]):
            row_plot_points[i] = dict(row_data[i])

    for i in column_names:
        if dict(column_data[i]):
            column_plot_points[i] = dict(column_data[i])

    for i in spacingbetweenslices_names:
        if dict(spacingbetweenslices_data[i]):
            spacingbetweenslices_plot_points[i] = dict(spacingbetweenslices_data[i])


    for i in slicethickness_names:
        if dict(slicethickness_data[i]):
            slicethickness_plot_points[i] = dict(slicethickness_data[i])

    for i in flipangle_names:
        if dict(flipangle_data[i]):
            flipangle_plot_points[i] = dict(flipangle_data[i])

    for i in repetetion_names:
        if dict(repetetion_data[i]):
            repetition_plot_points[i] = dict(repetetion_data[i])

    for i in echo_names:
        if dict(echo_data[i]):
            echo_plot_points[i] = dict(echo_data[i])

    

    print('TTTTrial', spacingbetweenslices_plot_points)

    print('TE:', echo_plot_points)
    print('TR:', repetition_plot_points)
    print('FA:', flipangle_plot_points)

    csv_names = get_csv_files()
    visible_doc = csv_names
    count_protocol_numbers_for_all(visible_doc)

    print('aaa',label_protocol)
    print('bbb',value_protocol)
    print('ccc',label_sex)
    print('ddd',value_sex)

    parameter_list = {'TE':echo_plot_points,\
         'TR':repetition_plot_points, 'FA':flipangle_plot_points,\
              'ST':slicethickness_plot_points, 'SliceSpacing':spacingbetweenslices_plot_points,\
                   'Rows':row_plot_points, 'Cols':column_plot_points
                   , 'PixelSpacing':pixelspacing0_plot_points}
    zero_item_out = {}
    for item in parameter_list:
        
        value_item = parameter_list[item]
        for x_1, y_1 in value_item.items():
            value_unit = value_item[x_1]
            dic_out = {}
            for x, y in value_unit.items():
                if y != 0:
                    dic_out[x] = y
            value_item[x_1] = dic_out
        zero_item_out[item] = value_item
    print(zero_item_out)            
    # print('param_list', parameter_list)
    parameter_list = zero_item_out
    protocol_dictionary = {}
    for i in label_protocol:
        para_dict = {}
        for j in parameter_list:
            if i in parameter_list[j]:
                
                para_dict[j] = parameter_list[j][i]

        protocol_dictionary[i] = para_dict
    print('PPPPPPPPPROROROR###################################################',protocol_dictionary)





    context = {
        'label_protocol':label_protocol,
        'value_protocol':value_protocol,
        'label_sex':label_sex,
        'value_sex':value_sex,
        'echo_plot_points':echo_plot_points,
        'repetition_plot_points':repetition_plot_points,
        'flipangle_plot_points':flipangle_plot_points,
        'slicethickness_plot_points':slicethickness_plot_points,
        'spacingbetweenslices_plot_points':spacingbetweenslices_plot_points,
        'row_plot_points':row_plot_points,
        'column_plot_points':column_plot_points,
        'pixelspacing0_plot_points': pixelspacing0_plot_points,
        'protocol_plot_points':protocol_plot_points,
        'gender_plot_points': gender_plot_points,
        'total_grouped_protocol':total_grouped_protocol,
        'protocol_dictionary':protocol_dictionary,
        
    }

    with open(json_dir,'w') as context_dumped:
        json.dump(context, context_dumped)

    return render(request, 'dashboard/UCSD_data_fake.html', context)


def LSpine_data(request):
    file_name = 'LSpine_data.csv'


    json_name = file_name.replace('.csv', '.json')
    json_name = os.path.join('cache', json_name)
    curr_dir = os.getcwd()
    json_dir = os.path.join(curr_dir, json_name)


    if os.path.exists(json_dir):
        f = open(json_dir)
        context = json.load(f)
        print('##############$$$$$$$$$$$$$ file bypass')
        return render(request, 'dashboard/UCSD_data.html', context)



    label_protocol, value_protocol = count_protocol_numbers(file_name)
    label_sex, value_sex = count_sex_numbers(file_name)

    echo_data = stack_plot_data(file_name, 'EchoTime')
    repetetion_data = stack_plot_data(file_name, 'RepetitionTime')
    flipangle_data = stack_plot_data(file_name, 'FlipAngle')
    slicethickness_data = stack_plot_data(file_name, 'SliceThickness')
    spacingbetweenslices_data = stack_plot_data(file_name, 'SpacingBetweenSlices')
    row_data = stack_plot_data(file_name, 'Rows')
    column_data = stack_plot_data(file_name, 'Columns')
    pixelspacing0_data = stack_plot_data(file_name, 'PixelSpacing0')
    total_grouped_protocol = grouped_protocol_parameters(file_name)


    echo_names = [i for i in echo_data]
    repetetion_names = [i for i in repetetion_data]
    flipangle_names = [i for i in flipangle_data]
    slicethickness_names = [i for i in slicethickness_data]
    spacingbetweenslices_names = [i for i in spacingbetweenslices_data]
    row_names = [i for i in row_data]
    column_names = [i for i in column_data]
    pixelspacing0_names = [i for i in pixelspacing0_data]


    protocol_plot_points = {}
    gender_plot_points = {}
    echo_plot_points = {}
    repetition_plot_points = {}
    flipangle_plot_points = {}
    slicethickness_plot_points = {}
    spacingbetweenslices_plot_points = {}
    row_plot_points = {}
    column_plot_points = {}
    pixelspacing0_plot_points = {}

    for count, label_name in enumerate(label_protocol):
        point_dict = {}
        point_dict[count] = value_protocol[count]
        protocol_plot_points[label_name] = point_dict

    print('formatted PROTOCOL:', protocol_plot_points)

    for count, label_name in enumerate(label_sex):
        point_dict = {}
        point_dict[count] = value_sex[count]
        gender_plot_points[label_name] = point_dict


    for i in pixelspacing0_names:
        if dict(pixelspacing0_data[i]):
            pixelspacing0_plot_points[i] = dict(pixelspacing0_data[i])

    for i in row_names:
        if dict(row_data[i]):
            row_plot_points[i] = dict(row_data[i])

    for i in column_names:
        if dict(column_data[i]):
            column_plot_points[i] = dict(column_data[i])

    for i in spacingbetweenslices_names:
        if dict(spacingbetweenslices_data[i]):
            spacingbetweenslices_plot_points[i] = dict(spacingbetweenslices_data[i])


    for i in slicethickness_names:
        if dict(slicethickness_data[i]):
            slicethickness_plot_points[i] = dict(slicethickness_data[i])

    for i in flipangle_names:
        if dict(flipangle_data[i]):
            flipangle_plot_points[i] = dict(flipangle_data[i])

    for i in repetetion_names:
        if dict(repetetion_data[i]):
            repetition_plot_points[i] = dict(repetetion_data[i])

    for i in echo_names:
        if dict(echo_data[i]):
            echo_plot_points[i] = dict(echo_data[i])

    

    print('TTTTrial', spacingbetweenslices_plot_points)

    print('TE:', echo_plot_points)
    print('TR:', repetition_plot_points)
    print('FA:', flipangle_plot_points)

    csv_names = get_csv_files()
    visible_doc = csv_names
    count_protocol_numbers_for_all(visible_doc)

    print('aaa',label_protocol)
    print('bbb',value_protocol)
    print('ccc',label_sex)
    print('ddd',value_sex)

    parameter_list = {'TE':echo_plot_points,\
         'TR':repetition_plot_points, 'FA':flipangle_plot_points,\
              'ST':slicethickness_plot_points, 'SliceSpacing':spacingbetweenslices_plot_points,\
                   'Rows':row_plot_points, 'Cols':column_plot_points
                   , 'PixelSpacing':pixelspacing0_plot_points}
    zero_item_out = {}
    for item in parameter_list:
        
        value_item = parameter_list[item]
        for x_1, y_1 in value_item.items():
            value_unit = value_item[x_1]
            dic_out = {}
            for x, y in value_unit.items():
                if y != 0:
                    dic_out[x] = y
            value_item[x_1] = dic_out
        zero_item_out[item] = value_item
    print(zero_item_out)            
    # print('param_list', parameter_list)
    parameter_list = zero_item_out
    protocol_dictionary = {}
    for i in label_protocol:
        para_dict = {}
        for j in parameter_list:
            if i in parameter_list[j]:
                
                para_dict[j] = parameter_list[j][i]

        protocol_dictionary[i] = para_dict
    print('PPPPPPPPPROROROR###################################################',protocol_dictionary)





    context = {
        'label_protocol':label_protocol,
        'value_protocol':value_protocol,
        'label_sex':label_sex,
        'value_sex':value_sex,
        'echo_plot_points':echo_plot_points,
        'repetition_plot_points':repetition_plot_points,
        'flipangle_plot_points':flipangle_plot_points,
        'slicethickness_plot_points':slicethickness_plot_points,
        'spacingbetweenslices_plot_points':spacingbetweenslices_plot_points,
        'row_plot_points':row_plot_points,
        'column_plot_points':column_plot_points,
        'pixelspacing0_plot_points': pixelspacing0_plot_points,
        'protocol_plot_points':protocol_plot_points,
        'gender_plot_points': gender_plot_points,
        'total_grouped_protocol':total_grouped_protocol,
        'protocol_dictionary':protocol_dictionary,
        
    }

    with open(json_dir,'w') as context_dumped:
        json.dump(context, context_dumped)

    
    return render(request, 'dashboard/LSpine_data.html', context)

def product(request):
    return render(request, 'dashboard/product.html')

def order(request):
    return render(request, 'dashboard/order.html')

def staff(request):
    return render(request, 'dashboard/staff.html')

@csrf_exempt
def index(request):
    # BIG TODO: CHANGE COUNTRY DATA INTO SUMMARIZED INFORMATION OF
    # EACH DATASET


    checkbox_value = CheckboxData.objects.all().order_by('sort_by_name')
    print(checkbox_value)
    label, value = count_protocol_numbers(csv_file)
    
    id_list = ['Gender_Male','Gender_Female','Gender_Other',
        'Modality_CT', 'Modality_MR',
        'Modality_EEG', 'Modality_SPECT','Modality_PET']

    
    csv_names = get_csv_files()
    # default all docs visible before confirm buttom
    visible_doc = csv_names
    print('csv_names',csv_names)
    checkbox_names = [i.sort_by_name for i in checkbox_value]
    
    print(checkbox_names)
    # print(checkbox_value.sort_by_name)
    ## TODO: HERE TO CALCULATE REAL RATIO HERE BECAUSE IT COULD BE
    ## CHANGING AFTER TOGGLING THE CHECKBOX

    total_rows, sex_distribution, total_f, total_m, total_o, blank_doc = sex_ratio()
    total_rows_modality, modality_distribution, total_CT, total_MR,\
     total_EEG, total_PET, total_SPECT = modality_ratio()

    modality_arr = [total_CT, total_MR, total_EEG, total_PET, total_SPECT]
    sex_arr = [total_m, total_f, total_o]

    modality_names = ['CT', 'MR', 'EEG', 'PET', 'SPECT']
    sex_names = ['M','F','O']
    print('modalitu names', modality_names)

    if request.method == 'GET':
        names_test = request.GET.getlist('names')
        print(names_test)

    if request.method == 'POST':
        id_list = request.POST.getlist('boxes')
        name_clicked = request.POST.getlist('names')
        
        print('nameclicked:', name_clicked)
        non_match = get_difference(checkbox_names, id_list)
        print('nonmatch',non_match)
        disp_dict = {'Gender_Male':'M','Gender_Female':'F','Gender_Other':'O',
        'Modality_CT':'CT', 'Modality_MR':'MR',
        'Modality_EEG':'EEG', 'Modality_SPECT':'SPECT','Modality_PET':'PET'}


        print(non_match)
        total_rows_modality, modality_distribution, total_CT, total_MR,\
        total_EEG, total_PET, total_SPECT = modality_ratio(not_include=non_match)
        modality_arr = [total_CT, total_MR, total_EEG, total_PET, total_SPECT]

        print(modality_arr)
        total_rows, sex_distribution, total_f, total_m, total_o, blank_doc = sex_ratio(not_include=non_match)
        sex_arr = [total_m, total_f, total_o]

        visible_doc = get_difference(csv_names, blank_doc)
        print('docs visible',visible_doc)
        
        # update checkmark
        checkbox_value.update(approved = False)
        
        for x in id_list:
            print(x)
            CheckboxData.objects.filter(sort_by_name=str(x)).update(approved=True)

 
        messages.success(request, ('You confirmed a change'))
    #     form = Summarized_DatasetForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    #         return redirect('/')
    # else:
    #     form = Summarized_DatasetForm()

    sex_datapoints = {}
    sex_totalnumber = {'totalnumber':sum(sex_arr)}
    for i in range(len(sex_arr)):
        sex_datapoints[sex_names[i]] = sex_arr[i]
    sex_datapoints = {x:y for x,y in sex_datapoints.items() if y!=0}

    modality_datapoints = {}
    modality_totalnumber = {'totalnumber':sum(modality_arr)}
    for i in range(len(modality_arr)):
        modality_datapoints[modality_names[i]] = modality_arr[i]
    print('model PPPPPPOINTS', modality_datapoints)
    # remove key if value is 0 to update the legend in modality graph
    modality_datapoints = {x:y for x,y in modality_datapoints.items() if y!=0}

    # for key, value in modality_datapoints:
    #     print(key, value)

    print(modality_datapoints)

    # { y: 5, legendText: "CT", indexLabel: "Android 53%" },
    # { y: 35.0, legendText: "iOS 35%", indexLabel: "Apple iOS 35%" },
    # { y: 7, legendText: "Blackberry 7%", indexLabel: "Blackberry 7%" },
    # { y: 2, legendText: "Windows 2%", indexLabel: "Windows Phone 2%" },
    # { y: 5, legendText: "Others 5%", indexLabel: "Others 5%" }


    result = count_protocol_numbers_for_all(visible_doc)
    # print('all spec results:', result['parsed_csv_demo_2.csv'])

    context={
        # 'form': form,
        'label': label,
        'value': value,
        'total_rows': total_rows,
        'sex_distribution': sex_distribution,
        'total_f': total_f,
        'total_m': total_m,
        'total_o':total_o,
        # 'toggle_list': toggle_list,
        'approve': True,
        
        'csv_names':csv_names,
        'visible_doc':visible_doc,
        'checkbox_value':checkbox_value,
        'id_list':id_list,

        'sex_arr':sex_arr,
        'sex_names':sex_names,
        'sex_datapoints':sex_datapoints,
        'sex_totalnumber': sex_totalnumber,

        'modality_arr': modality_arr,
        'modality_names':modality_names,
        'modality_datapoints':modality_datapoints,
        'modality_totalnumber': modality_totalnumber,

        'result':result,

        # 'sum_fe'

    }

    
    # return render(request, 'dashboard/index.html', context)
    return render(request, 'dashboard/index.html', context)

# TODO: Use this to display the imported csv meta data
def function1(request):
    return HttpResponse('This is a test page for function 1')



import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
 
def Import_csv(request):
    print('s')               
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file) 
            empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                 
                fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                obj = tbl_Employee.objects.create(Empcode=dbframe.Empcode,firstName=dbframe.firstName, middleName=dbframe.middleName,
                                                lastName=dbframe.lastName, email=dbframe.email, phoneNo=dbframe.phoneNo, address=dbframe.address, 
                                                experience=dbframe.experience, gender=dbframe.gender, DOB=fromdate_time_obj,
                                                qualification=dbframe.qualification)
                print(type(obj))
                obj.save()
 
            return render(request, 'dashboard/importexcel.html', {
                'uploaded_file_url': uploaded_file_url
            })    
    except Exception as identifier:            
        print(identifier)
     
    return render(request, 'dashboard/importexcel.html',{})