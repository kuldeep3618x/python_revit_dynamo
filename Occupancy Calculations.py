"""Occupancy Calcuations"""

__title__ = "Occupancy\nCalculations"
__author__= "kamlesh"

from pyrevit.coreutils import envvars
from decimal import *

####################################################################################################################

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

####################################################################################################################

# Reading an excel file using Python 
import xlrd 
from xlrd import open_workbook 

# Give the location of the file 
loc = ('C:\Users\A\Desktop\python_examples\AMI OCCUPANCY TABLE.xls') 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
####################################################################################################################
# Function to acquire all elements of category & get parameter value by name 

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()


    
#####################################################################################################################
# Excel values for Occupant Load factor and Occupant Load factor values

occupancy = sheet.col_values(0)
occupant_load_factor = sheet.col_values(1)

occupant_load_factor_int = list()
occupant_load_factor_int = [round(x,1) for x in occupant_load_factor]
# print(occupant_load_factor_int)

zipbObj = zip(occupancy, occupant_load_factor_int)
dict_of_occupancy = dict(zipbObj)
# print(dict_of_occupancy)

#####################################################################################################################
#All elements of category- Rooms

rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
# print(rooms)

#####################################################################################################################

# For checking if required
# Acquiring Room Numbers
# room_numbers = list()
# room_numbers = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in rooms]
# print(room_numbers)

# Acquiring Room Names
# room_name = list()
# room_name = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms]
# print(room_name)

#####################################################################################################################
# Acquiring Occupancy Types from Rooms
occupant_load_rooms = list()
for room in rooms:
    for param in room.Parameters:
        if param.IsShared and param.Definition.Name == 'ali':   #Change Parameter to assign the Occupant Load
            paramValue = room.get_Parameter(param.GUID)
            occupant_load_rooms.append(paramValue.AsString())
# print(occupant_load_rooms)

#####################################################################################################################
#####################################################################################################################
# Function for removing values from list 

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


# Function for acquiring index of item in list

def indices(the_list, val):
    # """Always returns a list containing the indices of val in the_list"""
    retval = []
    last = 0
    while val in the_list[last:]:
             i = the_list[last:].index(val) 
             retval.append(last + i)
             last += i + 1   
    return retval

#####################################################################################################################
#####################################################################################################################

occupant_load_rooms_filter_Exit_Stairs = remove_values_from_list(occupant_load_rooms,'Exit_Stairs')
# print(occupant_load_rooms_filter_Exit_Stairs)


# occupant_load_rooms_filter_None = filter(None, occupant_load_rooms_filter_Exit_Stairs)
# print(occupant_load_rooms_filter_None)



occupant_load_rooms_filter_Industrial = remove_values_from_list(occupant_load_rooms_filter_Exit_Stairs,'Industrial_0')
# print(occupant_load_rooms_filter_Industrial)


occupant_load_rooms_filter_None = filter(None, occupant_load_rooms_filter_Industrial)
# print(occupant_load_rooms_filter_None)




#####################################################################################################################
# Filtering indices with 'Stairs' & 'None'

Exit_Stairs_index = indices(occupant_load_rooms, 'Exit_Stairs')
Industrial_index = indices(occupant_load_rooms, 'Industrial_0')
Room_None_index = indices(occupant_load_rooms, None)

# Combining indices for 'None' & "Exit_Stairs"
for i in Room_None_index:
    Exit_Stairs_index.append(i)
# print(Exit_Stairs_index)

for i in Industrial_index:
    Exit_Stairs_index.append(i)
# print(Exit_Stairs_index)

Room_filtered = list()
Room_filtered = [ j for i, j in enumerate(rooms) if i not in (Exit_Stairs_index)]
# print(Room_filtered)

# Acquiring Room Numbers
room_numbers = list()
room_numbers = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in Room_filtered]
# print(room_numbers)

# Acquiring Room Names
room_name = list()
room_name = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in Room_filtered]
# print(room_name)



#####################################################################################################################

# Acquiring areas for filtered Rooms

area_in_Room_filtered = list()
area_in_Room_filtered = [ar.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble() for ar in Room_filtered]
area_in_Room_filtered = [(ar/10) for ar in area_in_Room_filtered]                    
area_in_Room_filtered = [round(ar) for ar in area_in_Room_filtered]
area_in_Room_filtered = [ 1 if x==0 else x for x in area_in_Room_filtered]
# print(area_in_Room_filtered)

#####################################################################################################################
# Acquire final list of occupant load factors for filtered from dictionary

occupant_filtered_values = list()
for r in occupant_load_rooms_filter_None:
    occupant_filtered_values = dict_of_occupancy[r]

occupant_filtered_values = map(dict_of_occupancy.get, occupant_load_rooms_filter_None)
occupant_filtered_values = [float(oc) for oc in occupant_filtered_values]  
# print(occupant_filtered_values)
 

#####################################################################################################################
# Occupancy Calcuations

occupant_count = [x/y for x,y in zip(map(float, area_in_Room_filtered), map(float, occupant_filtered_values))]
occupant_count = [long(round(oc)) for oc in occupant_count]
occupant_count = [int(oc) for oc in occupant_count]
occupant_count = [ 1 if x==0 else x for x in occupant_count]
occupant_count = [str(oc) for oc in occupant_count]
# print(occupant_count)

######################################################################################################################

def tolist(obj1):
    if hasattr(obj1,"__iter__"): return obj1
    else: return [obj1]

Room_filtered = tolist(Room_filtered)
occupant_count = tolist(occupant_count)

######################################################################################################################

def set_parameter_by_name(element, parameterName, value):
	element.LookupParameter(parameterName).Set(value)
 
 
 
######################################################################################################################

#Start Transaction

t = Transaction(doc, 'script')
write_oc_pass = list()
write_oc_fail = list()

t.Start()
for r in Room_filtered:
    try:
        write_oc_pass = [ set_parameter_by_name(r,'SWAP',oc) for r,oc in zip(Room_filtered, occupant_count)]
    except:
        write_oc_fail.append(oc)
       
t.Commit()     
# print(write_oc_pass)
print(write_oc_fail)                

######################################################################################################################
