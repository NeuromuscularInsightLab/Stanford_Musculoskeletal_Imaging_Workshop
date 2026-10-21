# Your project name
Template for github repository creation. Please update with your specific details.

 < Short description of your project and code >

## Table of content
* [1.Dependencies](#1dependencies)
* [2.Installation](#2installation)
* [3.Data organization](#3data-organization)
* [4.Preprocessing](#4preprocessing)
* [5.Statistical Analysis](#5statistical-analysis)

## 1.Dependencies

* SCT v6.0
* FSL 6.0
* Python 3.9


## 2.Installation

* Create python environment
~~~
conda create --name Dermatomal_Mapping_R01 python==3.9
~~~

* Activate environment
~~~
conda activate Dermatomal_Mapping_R01
~~~

* Install requirements
~~~
pip install -r requirements.txt
~~~

## 3.Data organization
~~~
BIDS
├── sourcedata
│   │
│   └── sub-XXX
│       └── anat
│           ├── sub-XX_T2w.nii.gz
│           └── sub-XX_T2w.json
│       └── func
│            ├── sub-XX_task-XX_bold.nii.gz
│            └── sub-XX_task-XX_bold.json
├── derivatives
     │
     ├── labels
     └── sub-XXX

~~~

## 4.Preprocessing
Run
~~~
# command to run your preprocessing script
~~~

## 5.Statistical Analysis
