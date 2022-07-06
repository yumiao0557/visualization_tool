![npm](https://img.shields.io/badge/Surgalign-Data%20Visualization-blue)
# Database Visualization Interface

Surgalign Spine Technology


## Introduction

The purpose of this repository and program is to run a Django based data visualization dashboard. This dashboard consists of multiple data sources from DICOM files. All data are displayed based on [Canvas JS Chart](https://canvasjs.com/) and data are presented in both cross-sectional and longitudinal forms.


## Setup Virtual Environment

* You will need [Git Bash](https://gitforwindows.org/) throughout the whole process.
* Clone this repository in your local directory.
* Access this folder and type `. /venv/Scripts/activate` in your git bash window to activate thr virtual environment.
* Access `datavisual` folder and type `pip install -r requirements.txt` in your git bash window to install necessary dependencies to make the web app to run.


## Required Packages

* pydicom
* tqdm
* Django
* django-crispy-forms
* dicom-csv

## Running the Program

* Type `python manage.py runserver` in your git bash window to run this web app in your local host.
* Wait fot the few seconds and go to your browser and type http://127.0.0.1:8000/ to open the web app.

### Dashboard

1. The distribution of all data are shown as doughnut chart on the web page
2. The checkbox menu could filter unwanted parameters.
3. As parameters are set, click confirm and the doughnut will be updated according to the parameters selected.
4. The Document name section listed the database name associated with the parameter selectied. If no corresponding parameter exists in the dataset, the document will be hidden.
5. Click the document name will direct user to a new page where more specific detailed information related to that dataset is presented. 

### Dataset Page

1. After clicking the dataset hyper link from dashboard, user are directed to a new dataset page.
2. This page listed the distribution of protocol, gender information associated with the dataset selected.
3. The doughnut chart is interactive and could show more detailed information according to the specific protocol selected.
4. The parameters of detailed doughnut chart are
  * TR: Repetition Time
  * TE: Echo Time
  * FA: Flip Angle
  * ST: Slice Thickness
  * SliceSpacing: Spacing between Slices
  * Rows: Rows
  * Cols: Columns
  * PixelSpacing: Pixel Spacing 0
5. The number of different parameter combinations is also shown in this page as a column graph

## API Reference and Data Models

### API Used
* [Django](https://www.djangoproject.com/)
* [Canvas JS](https://canvasjs.com/)
* [Bootstraps](https://getbootstrap.com/)
* CSS
* Django Built-in SQLite

### Data Model Structure
```python
class CheckboxData(models.Model):
    sort_by_name = models.CharField(max_length=100)
    approved = models.BooleanField(default=True)
```
# System Design

![alt text](https://github.com/YuMiao329/web_app_data_visualization/blob/main/Data%20Visualization%20Project%20Diagram.png?raw=true)

# Software License:
This program has an MIT License. All of the code is open to be edited and distributed.
