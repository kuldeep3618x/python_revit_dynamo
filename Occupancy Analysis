"""Occupancy Calcuations"""

__title__ = "Occupancy\nCalculations"
__author__= "J K Roshan\nKerketta"

import itertools

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from itertools import chain
from itertools import islice

####################################################################################################################

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

###################################################################################################################

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

from pyrevit import revit, DB


####################################################################################################################

# Reading an excel file using Python 
import xlrd 
from xlrd import open_workbook 


#Select Excel File from Folder

logger = script.get_logger()
# if__name__ == '__main__':
source_file = forms.pick_file(file_ext='xlsx')

# Give the location of Excel the file 
loc = source_file

# To open Workbook 
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0) 

#####################################################################################################################
# Read Excel Parameters and Family Category

identifier_param_to_read = sheet.col_values(1)

# Column values in Excel File
occupancy_type_identity = sheet.col_values(1)
occupancy_factor_NBC = sheet.col_values(2)
occupancy_factor_SBC = sheet.col_values(3)
occupancy_factor_IBC = sheet.col_values(4)
occupancy_factor_NFPA = sheet.col_values(5)
occupancy_factor_DCD = sheet.col_values(6)
occupancy_factor_BS = sheet.col_values(7)
occupancy_factor_FN = sheet.col_values(8)

occupancy_type_dictionary = {z[0]:list(z[1:]) for z in zip(occupancy_type_identity, occupancy_factor_NBC, occupancy_factor_SBC, occupancy_factor_IBC, occupancy_factor_NFPA, occupancy_factor_DCD, occupancy_factor_BS, occupancy_factor_FN)}
 
####################################################################################################################
# Function to acquire all elements of category & get parameter value by name 

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

####################################################################################################################
# Function to read Shared Parameter values as String

def shared_parameter_values(elems, parameter_name):
    elem_param_values = []
    for e in elems:
        for param in e.Parameters:
            if param.IsShared and param.Definition.Name == parameter_name:
                paramValue = e.get_Parameter(param.GUID)
                elem_param_values.append(paramValue.AsString())
    return elem_param_values

####################################################################################################################

def set_parameter_by_name(element, parameterName, value):
	element.LookupParameter(parameterName).Set(value)
 
######################################################################################################################

def output_statement(sample_room_num_with_issues, sample_room_name_with_issues):
 
    sample_room_num_with_mismatch = ['Room Number: ' + item + ', ' for item in sample_room_num_with_issues]
    sample_room_name_with_mismatch = ['Room Name: ' + item + '. ' for item in sample_room_name_with_issues]
   
    sample_test_issues = [i + j for i,j in zip(sample_room_num_with_mismatch, sample_room_name_with_mismatch)]
    for issues in sample_test_issues:
        print(issues)
        
######################################################################################################################

rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
room_numbers = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in rooms]
# print(room_numbers)
room_names = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms]
# print(room_name)

test_room_occupancy_type = [r.get_Parameter(BuiltInParameter.ROOM_OCCUPANCY).AsString() for r in rooms]
# print(test_room_occupancy_type) 

filter_rooms_with_no_occupancy_type_index = [ i for i, x in enumerate(test_room_occupancy_type) if x == None]
rooms_with_no_occupancy_type =[ rooms[i] for i in filter_rooms_with_no_occupancy_type_index ]
rooms_numbers_with_no_occupancy_type = [room_numbers[i] for i in filter_rooms_with_no_occupancy_type_index]
room_names_with_no_occupancy_type = [room_names[i] for i in filter_rooms_with_no_occupancy_type_index]
print('*'*120)
if len(room_names_with_no_occupancy_type) == 0:
    print('All Rooms have Occupancy Type Assigned')
else:
    print('The following Rooms have no Occupancy Type assigned:')
    # rooms_with_no_occupancy_type_issue = output_statement(rooms_numbers_with_no_occupancy_type,room_names_with_no_occupancy_type ) 
print('*'*120)


filter_rooms_with_occupancy_type_index = [i for i, x in enumerate(test_room_occupancy_type) if x != None] 
# print(filter_rooms_with_occupancy_type_index)

rooms_with_occupancy_type = [rooms[i] for i in filter_rooms_with_occupancy_type_index]
rooms_numbers_with_occupancy_type = [room_numbers[i] for i in filter_rooms_with_occupancy_type_index]
room_names_with_occupancy_type = [room_names[i] for i in filter_rooms_with_occupancy_type_index]
room_occupancy_type = [test_room_occupancy_type[i] for i in filter_rooms_with_occupancy_type_index]
# print(room_occupancy_type)

room_occupancy_type_invalid = list((set(room_occupancy_type).difference(occupancy_type_identity)))
index_of_invalid_room_occupancy_type = []
for i in range(len(room_occupancy_type)):
    if room_occupancy_type[i] in room_occupancy_type_invalid:
        index_of_invalid_room_occupancy_type.append(i)
# print(index_of_invalid_room_occupancy_type)

rooms_with_invalid_occupancy_type = [rooms_with_occupancy_type[i] for i in index_of_invalid_room_occupancy_type]
rooms_numbers_with_invalid_occupancy_type = [rooms_numbers_with_occupancy_type[i] for i in index_of_invalid_room_occupancy_type]
room_names_with_invalid_occupancy_type = [room_names_with_occupancy_type[i] for i in index_of_invalid_room_occupancy_type]
room_occupancy_type_invalid = [room_occupancy_type[i] for i in index_of_invalid_room_occupancy_type]
# print(room_occupancy_type_invalid)

if len(room_occupancy_type_invalid) == 0:
    print('All Rooms with Occupancy Type provided are valid')
else:
    print('The following Rooms have invalid Occupancy Type assigned:')
    rooms_with_invalid_occupancy_type_issue = output_statement(rooms_numbers_with_invalid_occupancy_type,room_names_with_invalid_occupancy_type) 
print('*'*120)

set_index_of_invalid_room_occupancy_type = set(index_of_invalid_room_occupancy_type) 
rooms_with_valid_occupancy_type = [e for i, e in enumerate(rooms_with_occupancy_type) if i not in set_index_of_invalid_room_occupancy_type]
room_valid_occupancy_types = [e for i, e in enumerate(room_occupancy_type) if i not in set_index_of_invalid_room_occupancy_type]
# print(room_valid_occupancy_types)

area_in_rooms_with_valid_occupancy_type = [ar.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble() for ar in rooms_with_valid_occupancy_type]
area_in_rooms_with_valid_occupancy_type = [round((ar/10)) for ar in area_in_rooms_with_valid_occupancy_type]
area_in_rooms_with_valid_occupancy_type = [1 if x == 0 else x for x in area_in_rooms_with_valid_occupancy_type]
# print(area_in_rooms_with_valid_occupancy_type)

####################################################################################################################

def occupant_count_calculation(sheet_col_for_code):
    values_from_dict_code = [occupancy_type_dictionary[x][sheet_col_for_code] for x in room_valid_occupancy_types]
    
    filter_occupancy_values_index_with_non_NA = [i for i, x in enumerate(values_from_dict_code) if x != 'NA']
    rooms_with_valid_occupancy_values = [rooms_with_valid_occupancy_type[i] for i in  filter_occupancy_values_index_with_non_NA]
    room_valid_occupancy_values = [values_from_dict_code[i] for i in filter_occupancy_values_index_with_non_NA]
    area_in_rooms_with_valid_occupancy_values = [area_in_rooms_with_valid_occupancy_type[i] for i in filter_occupancy_values_index_with_non_NA]
    occupant_count_as_per_code = [x/y for x,y in zip(map(float, area_in_rooms_with_valid_occupancy_values), map(float, room_valid_occupancy_values))]
        
    occupant_count_as_per_code = [long(round(oc)) for oc in occupant_count_as_per_code]
    occupant_count_as_per_code = [int(oc) for oc in occupant_count_as_per_code]
    occupant_count_as_per_code = [ 1 if x == 0 else x for x in occupant_count_as_per_code]
    occupant_count_total = sum(occupant_count_as_per_code)
    
    room_level_name = [r.Level.Name for r in rooms_with_valid_occupancy_values]
    room_level_elevation = [r.Level.Elevation for r in rooms_with_valid_occupancy_values]
      
    temp_list = []
    for i in range(len(room_level_elevation)):
        temp_list.append([room_level_elevation[i], i])
    temp_list.sort()
    
    index_of_room_level_sorted = []
    for x in temp_list:
        index_of_room_level_sorted.append(x[1])
        
    
    sorted_room_level_elevation_name = [room_level_name[i] for i in index_of_room_level_sorted]
    create_sublist_by_level_name = [list(y) for x,y in itertools.groupby(sorted_room_level_elevation_name)]
    
    length_of_sublist_of_level_name = [len(x) for x in create_sublist_by_level_name]
    
    sorted_rooms_by_level = [rooms_with_valid_occupancy_values[i] for i in index_of_room_level_sorted]
    create_sublist_for_rooms = iter(sorted_rooms_by_level)
    create_sublist_for_rooms = [list(islice(create_sublist_for_rooms, elem)) for elem in length_of_sublist_of_level_name]

    
    sorted_room_level_elevation = [room_level_elevation[i] for i in index_of_room_level_sorted]
    create_sublist_for_levels_of_rooms = iter(sorted_room_level_elevation)
    create_sublist_for_levels_of_rooms = [list(islice(create_sublist_for_levels_of_rooms, elem)) for elem in length_of_sublist_of_level_name]
    
    sorted_room_valid_occupancy_values = [room_valid_occupancy_values[i] for i in index_of_room_level_sorted] 
    create_sublist_for_room_valid_occupancy_values_by_level = iter(sorted_room_valid_occupancy_values)
    create_sublist_for_room_valid_occupancy_values_by_level = [list(islice(create_sublist_for_room_valid_occupancy_values_by_level, elem)) for elem in length_of_sublist_of_level_name]
    
    sorted_room_occupant_count_by_level = [occupant_count_as_per_code[i] for i in index_of_room_level_sorted]
    create_sublist_for_room_occupant_count_by_level = iter(sorted_room_occupant_count_by_level)
    create_sublist_for_room_occupant_count_by_level = [list(islice(create_sublist_for_room_occupant_count_by_level, elem)) for elem in length_of_sublist_of_level_name]
    length_of_sublist_for_occupant_count = [len(x) for x in create_sublist_for_room_occupant_count_by_level]
    
    sum_of_occupancy_count_for_each_level = [sum(x) for x in create_sublist_for_room_occupant_count_by_level]
    
    unique_room_level_names = [set(x) for x in create_sublist_by_level_name]
    unique_room_level_names = [list(x) for x in unique_room_level_names]    
    unique_room_level_names = [item for sublist in unique_room_level_names for item in sublist]
    
    egress_capacity_requirement_for_each_level = [round(x * 7.6) for x in sum_of_occupancy_count_for_each_level]
    
    ####################################################################################################################
    
    occupant_count_greater_than_fifty = []
    
    for x in create_sublist_for_room_occupant_count_by_level:
        temp = [i for i, y in enumerate(x) if (y > 50) ]
    
        occupant_count_greater_than_fifty.append(temp)
    
   
   #################################################################################################################### 
    
    
    # Write occupancy values
    
    occupant_count_as_per_code_for_writing_to_param = [ str(oc) for oc in occupant_count_as_per_code]
    
    # Start Transaction
    
    t =  Transaction(doc, 'script')
    write_oc_pass = list()
    write_oc_fail = list()

    t.Start()
    for r in rooms_with_valid_occupancy_values:
        try:
            write_oc_pass = [ set_parameter_by_name(r,'Occupant',oc) for r,oc in zip(rooms_with_valid_occupancy_values, occupant_count_as_per_code_for_writing_to_param)]
        except:
            write_oc_fail.append(oc)
       
    t.Commit()     
    
    filter_occupancy_values_index_with_NA = [ i for i, x in enumerate(values_from_dict_code) if x == 'NA']
    rooms_with_NA_occupancy_values = [rooms_with_valid_occupancy_type[i] for i in filter_occupancy_values_index_with_NA]
    room_NA_occupancy_values = [values_from_dict_code[i] for i in filter_occupancy_values_index_with_NA]
    
    # Start Transaction
    
    t =  Transaction(doc, 'script')
    write_oc_pass = list()
    write_oc_fail = list()

    t.Start()
    for r in rooms_with_NA_occupancy_values:
        try:
            write_oc_pass = [set_parameter_by_name(r,'Occupant',oc) for r,oc in zip(rooms_with_NA_occupancy_values, room_NA_occupancy_values)]
        except:
            write_oc_fail.append(oc)
       
    t.Commit()     

    return(occupant_count_total, unique_room_level_names, sum_of_occupancy_count_for_each_level, egress_capacity_requirement_for_each_level,occupant_count_greater_than_fifty)
    
####################################################################################################################  

def output_statement_for_rooms_of_each_level(sample_unique_room_level_names, sample_sum_of_occupancy_count_for_each_level, sample_egress_capacity_requirement_for_each_level):
    
    sample_sum_of_occupancy_count_for_each_level = [str(x) for x in sample_sum_of_occupancy_count_for_each_level]
    sample_egress_capacity_requirement_for_each_level = [str(x) for x in sample_egress_capacity_requirement_for_each_level]
    
    sample_unique_room_level_names_output = ['Level' + item + ' has ' for item in sample_unique_room_level_names]
    sample_sum_of_occupancy_count_for_each_level_output = [item + ' persons as Occupant Load and the minimum egress width of staircases required is ' for item in sample_sum_of_occupancy_count_for_each_level]
    sample_egress_capacity_requirement_for_each_level_output = [item + 'mm.' for item in sample_egress_capacity_requirement_for_each_level]

    sample_output_for_room_level_occupancy_sorted = [i + j + k for i,j,k in zip(sample_unique_room_level_names_output, sample_sum_of_occupancy_count_for_each_level_output, sample_egress_capacity_requirement_for_each_level_output)]
    for output in sample_output_for_room_level_occupancy_sorted:
        print(output)

######################################################################################################################

from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 

####################################################################################################################    

userInputcategory = SelectFromList('Select Fire Code to follow', ['01.NBC', '02.SBC', '03.IBC', '04.NFPA', '05.DCD', '06.BS', '07.FN'])
userInputcategory = str(userInputcategory)

######################################################################################################################

if userInputcategory == '01.NBC':
    occupancy_calculation_as_per_NBC = occupant_count_calculation(0)
    occupant_count_total_as_per_NBC = occupancy_calculation_as_per_NBC[0]
    occupant_level_name_as_per_NBC = occupancy_calculation_as_per_NBC[1]
    occupant_count_for_each_level_as_per_NBC = occupancy_calculation_as_per_NBC[2]
    egress_capacity_for_each_level_as_per_NBC = occupancy_calculation_as_per_NBC[3]
    print("The total occupant count for the building, as per NBC is : {} people.".format(occupant_count_total_as_per_NBC))
    print('*'*120)
    occupancy_calculation_per_level_as_per_NBC = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_NBC,  occupant_count_for_each_level_as_per_NBC, egress_capacity_for_each_level_as_per_NBC)
    print('*'*120)
    print(occupancy_calculation_as_per_NBC[4])
######################################################################################################################
elif userInputcategory == '02.SBC':
    occupancy_calculation_as_per_SBC = occupant_count_calculation(1)
    occupant_count_total_as_per_SBC = occupancy_calculation_as_per_SBC[0]
    occupant_level_name_as_per_SBC = occupancy_calculation_as_per_SBC[1]
    occupant_count_for_each_level_as_per_SBC = occupancy_calculation_as_per_SBC[2]
    egress_capacity_for_each_level_as_per_SBC = occupancy_calculation_as_per_SBC[3]
    print("The total occupant count for the building, as per SBC is : {} people.".format(occupant_count_total_as_per_SBC))
    print('*'*120)
    occupancy_calculation_per_level_as_per_SBC = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_SBC, occupant_count_for_each_level_as_per_SBC, egress_capacity_for_each_level_as_per_SBC)
    print('*'*120)    
    
######################################################################################################################   
elif userInputcategory == '03.IBC':
    occupancy_calculation_as_per_IBC = occupant_count_calculation(2)
    occupant_count_total_as_per_IBC = occupancy_calculation_as_per_IBC[0]
    occupant_level_name_as_per_IBC = occupancy_calculation_as_per_IBC[1]
    occupant_count_for_each_level_as_per_IBC = occupancy_calculation_as_per_IBC[2]
    egress_capacity_for_each_level_as_per_IBC = occupancy_calculation_as_per_IBC[3]    
    print("The total occupant count for the building, as per IBC is : {} people.".format(occupant_count_total_as_per_IBC))
    print('*'*120)
    occupancy_calculation_per_level_as_per_IBC = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_IBC, occupant_count_for_each_level_as_per_IBC, egress_capacity_for_each_level_as_per_IBC)
    print('*'*120)    
 
######################################################################################################################
elif userInputcategory == '04.NFPA':
    occupancy_calculation_as_per_NFPA = occupant_count_calculation(3)
    occupant_count_total_as_per_NFPA = occupancy_calculation_as_per_NFPA[0]
    occupant_level_name_as_per_NFPA = occupancy_calculation_as_per_NFPA[1]
    occupant_count_for_each_level_as_per_NFPA = occupancy_calculation_as_per_NFPA[2]
    egress_capacity_for_each_level_as_per_NFPA = occupancy_calculation_as_per_NFPA[3]  
    print("The total occupant count for the building, as per NFPA is : {} people.".format(occupant_count_total_as_per_NFPA))
    print('*'*120)
    occupancy_calculation_per_level_as_per_NFPA = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_NFPA, occupant_count_for_each_level_as_per_NFPA, egress_capacity_for_each_level_as_per_NFPA)
    print('*'*120)     
    
######################################################################################################################
elif userInputcategory == '05.DCD':
    occupancy_calculation_as_per_DCD = occupant_count_calculation(4)
    occupant_count_total_as_per_DCD = occupancy_calculation_as_per_DCD[0]
    occupant_level_name_as_per_DCD = occupancy_calculation_as_per_DCD[1]
    occupant_count_for_each_level_as_per_DCD = occupancy_calculation_as_per_DCD[2]
    egress_capacity_for_each_level_as_per_DCD = occupancy_calculation_as_per_DCD[3]     
    print("The total occupant count for the building, as per DCD is : {} people.".format(occupant_count_total_as_per_DCD))
    print('*'*120)
    occupancy_calculation_per_level_as_per_DCD = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_DCD, occupant_count_for_each_level_as_per_DCD, egress_capacity_for_each_level_as_per_DCD)
    print('*'*120)     
 
######################################################################################################################
elif userInputcategory == '06.BS':
    occupancy_calculation_as_per_BS = occupant_count_calculation(5)
    occupant_count_total_as_per_BS = occupancy_calculation_as_per_BS[0]
    occupant_level_name_as_per_BS = occupancy_calculation_as_per_BS[1]
    occupant_count_for_each_level_as_per_BS = occupancy_calculation_as_per_BS[2]
    egress_capacity_for_each_level_as_per_BS = occupancy_calculation_as_per_BS[3]   
    print("The total occupant count for the building, as per BS is : {} people.".format(occupant_count_total_as_per_BS))
    print('*'*120)
    occupancy_calculation_per_level_as_per_BS = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_BS, occupant_count_for_each_level_as_per_BS, egress_capacity_for_each_level_as_per_BS)
    print('*'*120)    
    
######################################################################################################################
elif userInputcategory == '07.FN':
    occupancy_calculation_as_per_FN = occupant_count_calculation(6)
    occupant_count_total_as_per_FN = occupancy_calculation_as_per_FN[0]
    occupant_level_name_as_per_FN = occupancy_calculation_as_per_FN[1]
    occupant_count_for_each_level_as_per_FN = occupancy_calculation_as_per_FN[2]
    egress_capacity_for_each_level_as_per_FN = occupancy_calculation_as_per_FN[3]     
    print("The total occupant count for the building, as per FN is : {} people.".format(occupant_count_total_as_per_FN))
    print('*'*120)
    occupancy_calculation_per_level_as_per_FN = output_statement_for_rooms_of_each_level(occupant_level_name_as_per_FN, occupant_count_for_each_level_as_per_FN, egress_capacity_for_each_level_as_per_FN)
    print('*'*120)
      
######################################################################################################################
else:
    pass

 ######################################################################################################################
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
