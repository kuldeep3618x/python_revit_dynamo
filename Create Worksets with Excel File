"""Create Worksets"""

# pylint: disable=E0401,W0703,C0103
from collections import namedtuple




__title__ = "Create\nWorksets"
__author__= "J K Roshan Kerketta"

import os.path as os
from pyrevit import script
from pyrevit import forms


import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *


# Import DocumentManager and TransactionManager

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

####################################################################################################################

logger = script.get_logger()
# if__name__ == '__main__':
source_file = forms.pick_file(file_ext='xls')

####################################################################################################################

# Reading an excel file using Python 

import xlrd 
from xlrd import open_workbook 

# Give the location of the file 

loc = source_file
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 

sheet_Architecture = wb.sheet_by_index(0)    #ARCHITECTURE
sheet_Skin = wb.sheet_by_index(1)      #SKIN
sheet_Interior = wb.sheet_by_index(2)      #INTERIOR
sheet_Signage = wb.sheet_by_index(3)    #SIGNAGE

####################################################################################################################

collector = FilteredWorksetCollector(doc)
worksets_in_current_doc = collector.OfKind(WorksetKind.UserWorkset).ToWorksets()

# print(worksets_in_current_doc)

workset_names_in_current_doc = [(workset.Name) for workset in worksets_in_current_doc]
# print(workset_names_in_current_doc)

#########################################################################################################
# Select- UserInput

from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 

userInputcategory = SelectFromList('Select Revit Model Worksets by File Type', ['01.Architecture', '02.Architecture-Skin', '03.Architecture-Interior', '04.Architecture-Signage'])
userInputcategory = str(userInputcategory)

#Workset Names in Excel file

if userInputcategory == '01.Architecture':
    workset_names = sheet_Architecture.col_values(1)
elif userInputcategory == '02.Architecture-Skin':
    workset_names = sheet_Skin.col_values(1)
elif userInputcategory == '03.Architecture-Interior':
    workset_names = sheet_Interior.col_values(1)
elif userInputcategory == '04.Architecture-Signage':
    workset_names = sheet_Signage.col_values(1)

####################################################################################################################

# Filtered Workset Names 

filtered_Worksets = [w for w in workset_names if w not in workset_names_in_current_doc]
print(filtered_Worksets)

####################################################################################################################
t = Transaction(doc)
t.Start('Create Workset')
newWorksets = []
for w in filtered_Worksets:
    Workset.Create(doc, w)
    newWorksets.append(workset_names)

t.Commit()

####################################################################################################################
