"""Occupancy Calcuations"""

__title__ = "Occupancy\nCalculations"
__author__= "J K Roshan\nKerketta"

####################################################################################################################
import itertools
import operator

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from pyrevit.api import UI  
from pyrevit import revit, DB

from itertools import chain
from itertools import islice
from pyrevit import HOST_APP

####################################################################################################################

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

from System.Collections.Generic import * 

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('ProtoGeometry')                       
from Autodesk.DesignScript.Geometry import *            
        
clr.AddReference("RevitNodes")                          
import Revit                                            
clr.ImportExtensions(Revit.Elements)                    
clr.ImportExtensions(Revit.GeometryConversion)         

clr.AddReference("RevitServices")                       
import RevitServices                                    
from RevitServices.Persistence import DocumentManager    

####################################################################################################################

doc = __revit__.ActiveUIDocument.Document

uiapp = DocumentManager.Instance.CurrentUIApplication   
app = uiapp.Application                                

uidoc = __revit__.ActiveUIDocument
activeV = doc.ActiveView

##################################################################################################################

# Reading an excel file using Python 
import xlrd 
from xlrd import open_workbook 

# Select Excel File from Folder

logger = script.get_logger()
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

def format_length(length_value, doc = None):
    doc = doc or HOST_APP.doc
    return DB.UnitFormatUtils.Format(units = doc.GetUnits(), unitType = DB.UnitType.UT_Length, value = length_value, maxAccuracy = False, forEditing =False)

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
# Function to write Shared Parameter values

def set_parameter_by_name(element, parameterName, value):
	element.LookupParameter(parameterName).Set(value)

####################################################################################################################
# Perform Set Parameter By Name as a Transaction

def set_parameter_by_name_transaction(sample_elements, sample_param_name, sample_param_values):
    
    t = Transaction(doc, 'script')
    write_param_pass = []
    write_param_fail = []
    t.Start()
    for e in sample_elements:
        try:
            write_param_pass = [set_parameter_by_name(e,sample_param_name,val) for e,val in zip(sample_elements, sample_param_values)]
        except:
            write_param_fail.append(val)
    t.Commit()  

####################################################################################################################

def all_elements_with_type_parameter_AsDouble(sample_doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in sample_doors:
        door_type = d.Symbol
        door_family_param = door_type.LookupParameter(door_family_type_parameter)
        temp = []
        if door_family_param:
            temp = door_family_param.AsDouble()
            door_family_test.append(temp)
        else:
            temp = 'fail'
            door_family_test.append(temp)
    return door_family_test

def unit_conversion(revit_value_in_feet):
    resultant_value_from_revit = [float(x) for x in revit_value_in_feet]
    resultant_value_unit_conversion = [format_length(x) for x in resultant_value_from_revit]
    resultant_value_converted_to_mm = [int(x) for x in resultant_value_unit_conversion]
    return(resultant_value_converted_to_mm)

#####################################################################################################################
# Function to print Output statements for None & Invalid Types

def output_statement(sample_room_num_with_issues, sample_room_name_with_issues):
 
    sample_room_num_with_mismatch = ['Room Number: ' + item + ', ' for item in sample_room_num_with_issues]
    sample_room_name_with_mismatch = ['Room Name: ' + item + '. ' for item in sample_room_name_with_issues]
   
    sample_test_issues = [i + j for i,j in zip(sample_room_num_with_mismatch, sample_room_name_with_mismatch)]
    for issues in sample_test_issues:
        print(issues)
        
######################################################################################################################
# Acquireing Doors and filtering Doors

doors = all_elements_of_category(BuiltInCategory.OST_Doors)
door_comments = [d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString() for d in doors]
# print(door_comments)
exclusions = ["ROLLING SHUTTER", "ACCESS PANEL", "CLOSET DOOR", "Curtain wall door"]

indices_for_non_glazed_doors = [i for i, x in enumerate(door_comments) if x not in exclusions]
# print(indices_for_non_glazed_doors)

##############
# Filter Doors

doors = [doors[i] for i in indices_for_non_glazed_doors]
door_room_nums = shared_parameter_values(doors, 'Room_Number')
door_nums = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in doors]
                              
######################################################################################################################
# Acquireing Rooms 
                                
rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
room_numbers = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in rooms]
# print(room_numbers)
room_names = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms]
# print(room_name)

######################################################################################################################
# Get Room Occupancy Type

test_room_occupancy_type = [r.get_Parameter(BuiltInParameter.ROOM_OCCUPANCY).AsString() for r in rooms]
# print(test_room_occupancy_type) 

######################################################################################################################
# Rooms with no Occupancy Type

filter_rooms_with_no_occupancy_type_index = [ i for i, x in enumerate(test_room_occupancy_type) if x == None]
rooms_with_no_occupancy_type =[ rooms[i] for i in filter_rooms_with_no_occupancy_type_index ]
rooms_numbers_with_no_occupancy_type = [room_numbers[i] for i in filter_rooms_with_no_occupancy_type_index]
room_names_with_no_occupancy_type = [room_names[i] for i in filter_rooms_with_no_occupancy_type_index]
print('*'*120)
if len(room_names_with_no_occupancy_type) == 0:
    print('All Rooms have Occupancy Type Assigned')
else:
    print('The following Rooms have no Occupancy Type assigned:')
    rooms_with_no_occupancy_type_issue = output_statement(rooms_numbers_with_no_occupancy_type,room_names_with_no_occupancy_type ) 
print('*'*120)

######################################################################################################################
# Filtered Rooms with Occupancy Type

filter_rooms_with_occupancy_type_index = [i for i, x in enumerate(test_room_occupancy_type) if x != None] 
# print(filter_rooms_with_occupancy_type_index)

rooms_with_occupancy_type = [rooms[i] for i in filter_rooms_with_occupancy_type_index]
rooms_numbers_with_occupancy_type = [room_numbers[i] for i in filter_rooms_with_occupancy_type_index]
room_names_with_occupancy_type = [room_names[i] for i in filter_rooms_with_occupancy_type_index]
room_occupancy_type = [test_room_occupancy_type[i] for i in filter_rooms_with_occupancy_type_index]
# print(room_occupancy_type)

######################################################################################################################
# Rooms with Invalid Occupancy Type

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
    print('The following Rooms have invalid Occupancy Type assigned.\nVERY IMPORTANT- Please fix all invalid Occupancy Types, it will cause incorrect calculations.')
    rooms_with_invalid_occupancy_type_issue = output_statement(rooms_numbers_with_invalid_occupancy_type,room_names_with_invalid_occupancy_type) 
print('*'*120)

######################################################################################################################
# Rooms with Valid Occupancy Type

set_index_of_invalid_room_occupancy_type = set(index_of_invalid_room_occupancy_type) 
rooms_with_valid_occupancy_type = [e for i, e in enumerate(rooms_with_occupancy_type) if i not in set_index_of_invalid_room_occupancy_type]
room_valid_occupancy_types = [e for i, e in enumerate(room_occupancy_type) if i not in set_index_of_invalid_room_occupancy_type]
# print(room_valid_occupancy_types)

area_in_rooms_with_valid_occupancy_type = [ar.get_Parameter(BuiltInParameter.ROOM_AREA).AsDouble() for ar in rooms_with_valid_occupancy_type]
area_in_rooms_with_valid_occupancy_type = [round((ar/10)) for ar in area_in_rooms_with_valid_occupancy_type]
area_in_rooms_with_valid_occupancy_type = [1 if x == 0 else x for x in area_in_rooms_with_valid_occupancy_type]
# print(area_in_rooms_with_valid_occupancy_type)

####################################################################################################################
# Occupant Count Calculation

def occupant_count_calculation(sheet_col_for_code):
    values_from_dict_code = [occupancy_type_dictionary[x][sheet_col_for_code] for x in room_valid_occupancy_types]
    
    ################################################################################################################
    # Filter Rooms, Occupancies with values from Dictionaries not as 'NA'
    
    filter_occupancy_values_index_with_non_NA = [i for i, x in enumerate(values_from_dict_code) if x != 'NA']
    rooms_with_valid_occupancy_values = [rooms_with_valid_occupancy_type[i] for i in  filter_occupancy_values_index_with_non_NA]
    room_valid_occupancy_values = [values_from_dict_code[i] for i in filter_occupancy_values_index_with_non_NA]
    area_in_rooms_with_valid_occupancy_values = [area_in_rooms_with_valid_occupancy_type[i] for i in filter_occupancy_values_index_with_non_NA]
    occupant_count_as_per_code = [x/y for x,y in zip(map(float, area_in_rooms_with_valid_occupancy_values), map(float, room_valid_occupancy_values))]
    
    ################################################################################################################
    # Calculate Occupant Count
        
    occupant_count_as_per_code = [long(round(oc)) for oc in occupant_count_as_per_code]
    occupant_count_as_per_code = [int(oc) for oc in occupant_count_as_per_code]
    occupant_count_as_per_code = [ 1 if x == 0 else x for x in occupant_count_as_per_code]
    occupant_count_total = sum(occupant_count_as_per_code)
    
    ################################################################################################################
    # Calculating Floor Level Occupancies 
      
    
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
    
    ################################################################################################################################
    # Clean Existing Room values
    
    room_count = len(rooms)
    list_of_default_values = [''] * room_count
    reset_all_room_occupancies = set_parameter_by_name_transaction(rooms, 'Occupant', list_of_default_values)
                                                                                   
    ################################################################################################################################
    # Write Occupancy Values
    
    occupant_count_as_per_code_for_writing_to_param = [ str(oc) for oc in occupant_count_as_per_code]
    write_occupant_count_to_rooms = set_parameter_by_name_transaction(rooms_with_valid_occupancy_values, 'Occupant', occupant_count_as_per_code_for_writing_to_param)
          
    ################################################################################################################################
    # Write Occupancy Values as 'NA' for Rooms with no Occupant count
    
    filter_occupancy_values_index_with_NA = [ i for i, x in enumerate(values_from_dict_code) if x == 'NA']
    rooms_with_NA_occupancy_values = [rooms_with_valid_occupancy_type[i] for i in filter_occupancy_values_index_with_NA]
    room_NA_occupancy_values = [values_from_dict_code[i] for i in filter_occupancy_values_index_with_NA]

    write_occupant_count_NA_to_rooms_with_no_occupancy_type = set_parameter_by_name_transaction(rooms_with_NA_occupancy_values, 'Occupant', room_NA_occupancy_values)
          
    ################################################################################################################  
    return(occupant_count_total, unique_room_level_names, sum_of_occupancy_count_for_each_level, egress_capacity_requirement_for_each_level, create_sublist_for_rooms, create_sublist_for_room_occupant_count_by_level)
             
####################################################################################################################  
# Create_sublist_for_room_occupant_count_by_level

def filter_room_egress_capacity(room_oc_count_sublist_by_lvl, filter, val):
    idx_oc_count_filter = []
    if filter == 'greater':
        for x in room_oc_count_sublist_by_lvl:
            temp = [i for i, y in enumerate(x) if (y > val)]
            idx_oc_count_filter.append(temp)
        return idx_oc_count_filter    

    elif filter == 'lesser':
        for x in room_oc_count_sublist_by_lvl:
            temp = [i for i, y in enumerate(x) if (y < val)]
            idx_oc_count_filter.append(temp)
        return idx_oc_count_filter 
            
    else:
        pass

def clean_filter_list(idx_oc_count_filter, room_sublist_by_lvl, room_oc_count_sublist_by_lvl ):
    #Filtering Rooms with occupant count, removing rooms with no occupant count
    
    idx_oc_count_sblist_not_empty = [i for i, x in enumerate(idx_oc_count_filter) if((len(x) != 0))]
    sblist_of_rooms_filtered_not_empty = [room_sublist_by_lvl[i] for i in idx_oc_count_sblist_not_empty]
    sblist_of_room_oc_count_filtered_not_empty = [room_oc_count_sublist_by_lvl[i] for i in idx_oc_count_sblist_not_empty]
    filter_idx_sublist_of_room_oc_at_lvl = [idx_oc_count_filter[i] for i in idx_oc_count_sblist_not_empty] 
    
    # Lookup nested Rooms with nested indices for valid Rooms at filtered Levels
    sblist_of_rooms_at_level_count_filter =  [[sblist_of_rooms_filtered_not_empty[sub_idx][item] for item in sublist] for sub_idx, sublist in enumerate(filter_idx_sublist_of_room_oc_at_lvl)]
    sblist_of_room_oc_count_filter = [[sblist_of_room_oc_count_filtered_not_empty[sub_idx][item] for item in sublist] for sub_idx, sublist in enumerate(filter_idx_sublist_of_room_oc_at_lvl)]
    length_of_sblist_of_rooms_at_level_count_filter = [len(x) for x in sblist_of_rooms_at_level_count_filter]

    # Room Occupancy as per filter

    flat_list_rooms_with_oc_count_as_filtered = [item for sublist in sblist_of_rooms_at_level_count_filter for item in sublist]
    filtered_room_names_as_per_oc_count = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in flat_list_rooms_with_oc_count_as_filtered]
    filtered_room_nums_as_per_oc_count = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in flat_list_rooms_with_oc_count_as_filtered]
    filtered_room_oc_count_as_per_count_filter = [item for sublist in sblist_of_room_oc_count_filter for item in sublist] 

    return flat_list_rooms_with_oc_count_as_filtered, filtered_room_names_as_per_oc_count, filtered_room_nums_as_per_oc_count, filtered_room_oc_count_as_per_count_filter

####################################################################################################################  
# Lookup Door Room Numbers against Room Numbers

def lookup_doors_in_rooms_as_oc_count_filter(flat_list_rooms_with_oc_count_filtered, filtered_room_names_as_per_oc_count, filtered_room_nums_as_per_oc_count, filtered_room_oc_count_as_per_count_filter, door_room_nums, doors):
    lookup_doors_in_rooms_as_count_filter = []
    for search_item in filtered_room_nums_as_per_oc_count:
        search_result = []   
        for i in range(len(door_room_nums)):
            if search_item == door_room_nums[i]:
                search_result.append(i)
        if len(search_result) > 0:
            lookup_doors_in_rooms_as_count_filter.append(search_result)
        else:
            lookup_doors_in_rooms_as_count_filter.append([None])   

    idx_of_rooms_with_doors_and_oc_as_count_filter = [i for i, x in enumerate(lookup_doors_in_rooms_as_count_filter) if x[0] != None]
    rnums_with_doors_and_oc_as_count_filter = [filtered_room_nums_as_per_oc_count[i] for i in idx_of_rooms_with_doors_and_oc_as_count_filter]
    rnames_with_doors_and_oc_as_count_filter = [filtered_room_names_as_per_oc_count[i] for i in idx_of_rooms_with_doors_and_oc_as_count_filter]
    rooms_with_doors_and_oc_as_count_filter = [flat_list_rooms_with_oc_count_filtered[i] for i in idx_of_rooms_with_doors_and_oc_as_count_filter]
    room_oc_count_for_rooms_with_doors_and_count_filter = [filtered_room_oc_count_as_per_count_filter[i] for i in idx_of_rooms_with_doors_and_oc_as_count_filter]
    
    # Looking up Doors for clean list of Rooms with doors & Occupancy as per count filter
    final_lookup_doors_in_rooms_with_oc_count_filter = []
    for search_item in rnums_with_doors_and_oc_as_count_filter:
        search_result = []
        for i in range(len(door_room_nums)):
            if search_item == door_room_nums[i]:
                search_result.append(i)
        if len(search_result)>0:
            final_lookup_doors_in_rooms_with_oc_count_filter.append(search_result)
        else:
            final_lookup_doors_in_rooms_with_oc_count_filter.append(None)
    
    length_of_sublist_of_doors_in_rooms_with_oc_count_filter = [len(x) for x in final_lookup_doors_in_rooms_with_oc_count_filter]
    
    # Check Door Room Numbers exist in Rooms with Occupancy as per count filter
    
    acquire_door_rnums_for_doors_with_oc_count_filter = []
    for f in final_lookup_doors_in_rooms_with_oc_count_filter:
        temp = []
        temp = [door_room_nums[i] for i in f]
        acquire_door_rnums_for_doors_with_oc_count_filter.append(temp)
    
    # Check Doors exist in Rooms with Occupancy as per count filter   
    
    acquire_doors_for_doors_in_rooms_with_oc_count_filter = []
    for f in final_lookup_doors_in_rooms_with_oc_count_filter:
        temp = []
        temp = [doors[i] for i in f]
        acquire_doors_for_doors_in_rooms_with_oc_count_filter.append(temp)
    
    # Door List Flattened for acquiring Widths
    acquire_doors_for_doors_in_rooms_with_oc_count_filter = [item for sublist in acquire_doors_for_doors_in_rooms_with_oc_count_filter for item in sublist]
    
    # Door Widths in Flattened List and conversion from feet to millimeters
    acquire_door_widths_for_doors_in_rooms_with_oc_count_filter = all_elements_with_type_parameter_AsDouble(acquire_doors_for_doors_in_rooms_with_oc_count_filter, 'Width')
    acquire_door_widths_for_doors_in_rooms_with_oc_count_filter = unit_conversion(acquire_door_widths_for_doors_in_rooms_with_oc_count_filter)
    
    # Create sublist for Door Widths for further assessment
    create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter = iter(acquire_door_widths_for_doors_in_rooms_with_oc_count_filter)
    create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter = [list(islice(create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter, elem)) for elem in length_of_sublist_of_doors_in_rooms_with_oc_count_filter]
    
    return create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter,rnums_with_doors_and_oc_as_count_filter, rnames_with_doors_and_oc_as_count_filter, rooms_with_doors_and_oc_as_count_filter, room_oc_count_for_rooms_with_doors_and_count_filter
   
####################################################################################################################  
# Lookup Doors as per Door Count Filter
   
def idx_filter_door_count_on_dwidths(create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter, count_filter, val):
    idx_of_doors_as_per_dcount_filter = []
    if count_filter == 'greater':
        idx_of_doors_as_per_dcount_filter = [i for i, x in enumerate(create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter) if len(x) > val]
        return idx_of_doors_as_per_dcount_filter
    elif count_filter == 'lesser':
        idx_of_doors_as_per_dcount_filter = [i for i, x in enumerate(create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter) if len(x) < val]
        return idx_of_doors_as_per_dcount_filter
    else:
        pass

# Lookup Rooms with Occupant Count and Door Count Filter
    
def room_info_filter_as_per_dcount_filter(idx_of_doors_as_per_dcount_filter,rnums_with_doors_and_oc_as_count_filter,rnames_with_doors_and_oc_as_count_filter, rooms_with_doors_and_oc_as_count_filter, room_oc_count_for_rooms_with_doors_and_count_filter):    
    rnums_with_oc_filter_and_dcount_filter = [rnums_with_doors_and_oc_as_count_filter[i] for i in idx_of_doors_as_per_dcount_filter]
    rnames_with_oc_filter_and_dcount_filter = [rnames_with_doors_and_oc_as_count_filter[i] for i in idx_of_doors_as_per_dcount_filter]
    rooms_with_oc_filter_and_dcount_filter = [rooms_with_doors_and_oc_as_count_filter[i] for i in idx_of_doors_as_per_dcount_filter]
    room_oc_count_filter_and_dcount_filter = [room_oc_count_for_rooms_with_doors_and_count_filter[i] for i in idx_of_doors_as_per_dcount_filter]
    return rnums_with_oc_filter_and_dcount_filter, rnames_with_oc_filter_and_dcount_filter, rooms_with_oc_filter_and_dcount_filter, room_oc_count_filter_and_dcount_filter

# Door Widths for Filtered Rooms - Occupant filter & Door count Filter

def door_widths_for_doors_in_rooms_with_oc_filter_dcount_filter(create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter, idx_filter_door_count_on_dwidths, room_oc_count_filter_and_dcount_filter):
    door_width_for_doors_in_rooms_with_oc_and_dcount_filter = [create_sublist_of_dwidths_of_doors_in_rooms_with_oc_count_filter[i] for i in idx_filter_door_count_on_dwidths]
    total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter = [sum(x) for x in door_width_for_doors_in_rooms_with_oc_and_dcount_filter]

    # Required Door Width
    total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter = [(x*7.6) for x in room_oc_count_filter_and_dcount_filter]
    total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter = [int(x) for x in total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter]
    
    # Index of Doors with insufficient width as per Egress capacity
    # index_of_insufficient_door_width_with_oc_and_dcount_filter = [idx for idx, x in enumerate(total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter) if x < total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter]
    index_of_insufficient_door_width_with_oc_and_dcount_filter = [idx for idx, (a,b) in enumerate(zip(total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter,total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter)) if a < b ]
    
    return total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter, total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter, index_of_insufficient_door_width_with_oc_and_dcount_filter
    
def output_analysis_for_door_widths(index_of_insufficient_door_width_with_oc_and_dcount_filter, rnums_with_oc_filter_and_dcount_filter, rnames_with_oc_filter_and_dcount_filter, total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter,total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter):
    if len(index_of_insufficient_door_width_with_oc_and_dcount_filter) != 0:
        rnums_with_oc_filter_dcount_filter_insuff_width = [rnums_with_oc_filter_and_dcount_filter[i] for i in index_of_insufficient_door_width_with_oc_and_dcount_filter]
        rnames_with_oc_filter_dcount_filter_insuff_width = [rnames_with_oc_filter_and_dcount_filter[i] for i in index_of_insufficient_door_width_with_oc_and_dcount_filter]
        total_egress_width_for_rooms_with_oc_filter_dcount_filter_insuff_width = [total_egress_width_for_doors_in_rooms_with_oc_and_dcount_filter[i] for i in index_of_insufficient_door_width_with_oc_and_dcount_filter]
        total_egress_width_reqd_for_room_with_oc_filter_dcount_filter_insuff_width = [total_egress_width_required_for_doors_in_rooms_with_oc_and_dcount_filter[i] for i in index_of_insufficient_door_width_with_oc_and_dcount_filter]
        
        reqd_egress_width_for_room_with_oc_dcount_filter_insuff_width = [str(x-y) for x,y in  zip(total_egress_width_reqd_for_room_with_oc_filter_dcount_filter_insuff_width, total_egress_width_for_rooms_with_oc_filter_dcount_filter_insuff_width)]
        total_egress_width_for_rooms_with_oc_filter_dcount_filter_insuff_width = [str(x) for x in total_egress_width_for_rooms_with_oc_filter_dcount_filter_insuff_width]
        total_egress_width_reqd_for_room_with_oc_filter_dcount_filter_insuff_width = [str(x) for x in total_egress_width_reqd_for_room_with_oc_filter_dcount_filter_insuff_width]
        
        print('The following Rooms with Doors donot meet the total egress width requirements as per code:')
        sample_rnums_with_egress_width_issues = ['Room Number: '+ item + ', ' for item in rnums_with_oc_filter_dcount_filter_insuff_width]
        sample_rnames_with_egress_width_issues = ['Room Names: ' + item + ', ' for item in rnames_with_oc_filter_dcount_filter_insuff_width]
        sample_egress_width_for_rooms_with_insuff_egress_issues = ['Total Egress width currently: ' + item + ', ' for item in total_egress_width_for_rooms_with_oc_filter_dcount_filter_insuff_width]
        sample_egress_width_reqd_for_rooms_with_insuff_egress_issues = ['Total Egress width to achieve: ' + item + ', ' for item in total_egress_width_reqd_for_room_with_oc_filter_dcount_filter_insuff_width]
        sample_egress_width_to_achieve = ['Additional Egress width to achieve: ' + item + '. ' for item in reqd_egress_width_for_room_with_oc_dcount_filter_insuff_width]
        sample_test_issues_for_egress_width = [i + j + k + l + m for i,j,k,l,m in zip(sample_rnums_with_egress_width_issues, sample_rnames_with_egress_width_issues, sample_egress_width_for_rooms_with_insuff_egress_issues, sample_egress_width_reqd_for_rooms_with_insuff_egress_issues, sample_egress_width_to_achieve)]
        for issues in sample_test_issues_for_egress_width:
            print(issues)

    else:
        print('Total Egress Width in the respective Rooms meet the code requirement.')
  
####################################################################################################################  

def output_statement_for_rooms_of_each_level(sample_unique_room_level_names, sample_sum_of_occupancy_count_for_each_level, sample_egress_capacity_requirement_for_each_level):
    
    sample_sum_of_occupancy_count_for_each_level = [str(x) for x in sample_sum_of_occupancy_count_for_each_level]
    sample_egress_capacity_requirement_for_each_level = [str(x) for x in sample_egress_capacity_requirement_for_each_level]
    
    sample_unique_room_level_names_output = ['Level- ' + item + ' has ' for item in sample_unique_room_level_names]
    sample_sum_of_occupancy_count_for_each_level_output = [item + ' persons as Occupant Load and the minimum egress width of staircases required is ' for item in sample_sum_of_occupancy_count_for_each_level]
    sample_egress_capacity_requirement_for_each_level_output = [item + ' mm.' for item in sample_egress_capacity_requirement_for_each_level]

    sample_output_for_room_level_occupancy_sorted = [i + j + k for i,j,k in zip(sample_unique_room_level_names_output, sample_sum_of_occupancy_count_for_each_level_output, sample_egress_capacity_requirement_for_each_level_output)]
    for output in sample_output_for_room_level_occupancy_sorted:
        print(output)

#################################################################################################################### 

def process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_code, code):
   
    occupant_count_total_as_per_code= occupancy_calculation_as_per_code[0]
    occupant_level_name_as_per_code= occupancy_calculation_as_per_code[1]
    occupant_count_for_each_level_as_per_code= occupancy_calculation_as_per_code[2]
    egress_capacity_for_each_level_as_per_code= occupancy_calculation_as_per_code[3]
    print("The total occupant count for the building, as per {} code is : {} persons.".format(code,occupant_count_total_as_per_code))
    print('*'*120)
    occupancy_calculation_per_level_as_per_code= output_statement_for_rooms_of_each_level(occupant_level_name_as_per_code,  occupant_count_for_each_level_as_per_code, egress_capacity_for_each_level_as_per_code)
    print('*'*120)
    
    # Occupant count for Rooms and Rooms with occupant count as per code
        
    rooms_sublist_by_lvl_as_per_code= occupancy_calculation_as_per_code[4]
    room_oc_count_sublist_by_lvl_as_per_code= occupancy_calculation_as_per_code[5]
    
    # Occupancy Analysis for Rooms with Occupancy Greater than 50 ppl
    idx_oc_count_greater_50_ppl_code= filter_room_egress_capacity(room_oc_count_sublist_by_lvl_as_per_code, 'greater', 50)
    
    clean_oc_count_greater_50_code= clean_filter_list(idx_oc_count_greater_50_ppl_code, rooms_sublist_by_lvl_as_per_code, room_oc_count_sublist_by_lvl_as_per_code)
    flat_rooms_with_oc_count_greater_50_code= clean_oc_count_greater_50_code[0]
    filtered_rnames_as_oc_count_greater_50_code= clean_oc_count_greater_50_code[1]
    filtered_rnums_as_oc_count_greater_50_code= clean_oc_count_greater_50_code[2]
    filtered_room_oc_count_greater_50_code= clean_oc_count_greater_50_code[3]
 
    filter_doors_as_per_oc_count_greater_50_code= lookup_doors_in_rooms_as_oc_count_filter(flat_rooms_with_oc_count_greater_50_code, filtered_rnames_as_oc_count_greater_50_code, filtered_rnums_as_oc_count_greater_50_code, filtered_room_oc_count_greater_50_code, door_room_nums, doors)
    filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_greater_50_code= filter_doors_as_per_oc_count_greater_50_code[0]
    rnums_with_doors_and_oc_as_count_greater_50_code= filter_doors_as_per_oc_count_greater_50_code[1]
    rnames_with_doors_and_oc_as_count_greater_50_code= filter_doors_as_per_oc_count_greater_50_code[2]
    rooms_with_doors_and_oc_as_count_greater_50_code= filter_doors_as_per_oc_count_greater_50_code[3]
    room_oc_count_for_rooms_with_doors_and_count_greater_50_code= filter_doors_as_per_oc_count_greater_50_code[4]
    
    ######################################################################################################################################
    # For occupant count greater than 50 and having more than one door
    
    idx_door_count_greater_1_on_dwidths_code= idx_filter_door_count_on_dwidths(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_greater_50_code, 'greater', 1)
    
    filtered_rooms_as_per_oc_greater_50_dcount_greater_1_code= room_info_filter_as_per_dcount_filter(idx_door_count_greater_1_on_dwidths_code, rnums_with_doors_and_oc_as_count_greater_50_code,rnames_with_doors_and_oc_as_count_greater_50_code, rooms_with_doors_and_oc_as_count_greater_50_code, room_oc_count_for_rooms_with_doors_and_count_greater_50_code)
     
    rnums_with_oc_greater_50_and_dcount_greater_1_code= filtered_rooms_as_per_oc_greater_50_dcount_greater_1_code[0]
    rnames_with_oc_greater_50_and_dcount_greater_1_code= filtered_rooms_as_per_oc_greater_50_dcount_greater_1_code[1] 
    rooms_with_oc_greater_50_and_dcount_greater_1_code= filtered_rooms_as_per_oc_greater_50_dcount_greater_1_code[2]
    room_oc_count_greater_50_and_dcount_greater_1_code= filtered_rooms_as_per_oc_greater_50_dcount_greater_1_code[3] 
    
    filtered_door_widths_as_per_oc_and_dcount_greater_1_code= door_widths_for_doors_in_rooms_with_oc_filter_dcount_filter(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_greater_50_code, idx_door_count_greater_1_on_dwidths_code, room_oc_count_greater_50_and_dcount_greater_1_code)
    total_egress_width_for_doors_in_rooms_with_oc_dcount_greater_1_code= filtered_door_widths_as_per_oc_and_dcount_greater_1_code[0]
    total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_greater_1_code= filtered_door_widths_as_per_oc_and_dcount_greater_1_code[1]
    idx_of_insufficent_door_width_with_oc_dcount_greater_1_code= filtered_door_widths_as_per_oc_and_dcount_greater_1_code[2]
    print("Analysis of Rooms, as per {} code with Occupancy greater than 50 persons & have two or more doors.".format(code))
    print('*'*30)
    egress_width_analysis_code = output_analysis_for_door_widths(idx_of_insufficent_door_width_with_oc_dcount_greater_1_code, rnums_with_oc_greater_50_and_dcount_greater_1_code, rnames_with_oc_greater_50_and_dcount_greater_1_code, total_egress_width_for_doors_in_rooms_with_oc_dcount_greater_1_code, total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_greater_1_code) 
    if len(idx_of_insufficent_door_width_with_oc_dcount_greater_1_code) != 0:
        print('IMPORTANT- Please note that the addin does not take into account Doors from linked Revit files.\nPlease do take into account these doors, additionally in the mentioned Rooms.')
    else:
        pass
    print('*'*120)
    
    # For occupant count greater than 50 and having less than two doors
        
    idx_door_count_lesser_2_on_dwidths_code= idx_filter_door_count_on_dwidths(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_greater_50_code, 'lesser', 2)
    filtered_rooms_as_per_oc_greater_50_dcount_lesser_2_code= room_info_filter_as_per_dcount_filter(idx_door_count_lesser_2_on_dwidths_code, rnums_with_doors_and_oc_as_count_greater_50_code,rnames_with_doors_and_oc_as_count_greater_50_code, rooms_with_doors_and_oc_as_count_greater_50_code, room_oc_count_for_rooms_with_doors_and_count_greater_50_code)
    
    rnums_with_oc_greater_50_and_dcount_lesser_2_code= filtered_rooms_as_per_oc_greater_50_dcount_lesser_2_code[0]
    rnames_with_oc_greater_50_and_dcount_lesser_2_code= filtered_rooms_as_per_oc_greater_50_dcount_lesser_2_code[1] 
    rooms_with_oc_greater_50_and_dcount_lesser_2_code= filtered_rooms_as_per_oc_greater_50_dcount_lesser_2_code[2]
    room_oc_count_greater_50_and_dcount_lesser_2_code= filtered_rooms_as_per_oc_greater_50_dcount_lesser_2_code[3] 
    
    filtered_door_widths_as_per_oc_and_dcount_lesser_2_code= door_widths_for_doors_in_rooms_with_oc_filter_dcount_filter(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_greater_50_code, idx_door_count_lesser_2_on_dwidths_code, room_oc_count_greater_50_and_dcount_lesser_2_code)
    total_egress_width_for_doors_in_rooms_with_oc_dcount_lesser_2_code= filtered_door_widths_as_per_oc_and_dcount_lesser_2_code[0]
    total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_lesser_2_code= filtered_door_widths_as_per_oc_and_dcount_lesser_2_code[1]
    idx_of_insufficent_door_width_with_oc_dcount_lesser_2_code= filtered_door_widths_as_per_oc_and_dcount_lesser_2_code[2]
    print("Analysis of Rooms, as per {} code with Occupancy greater than 50 persons & has one door only.".format(code))
    print('*'*30)
    egress_width_analysis_code= output_analysis_for_door_widths(idx_of_insufficent_door_width_with_oc_dcount_lesser_2_code, rnums_with_oc_greater_50_and_dcount_lesser_2_code, rnames_with_oc_greater_50_and_dcount_lesser_2_code, total_egress_width_for_doors_in_rooms_with_oc_dcount_lesser_2_code, total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_lesser_2_code) 
    if len(idx_of_insufficent_door_width_with_oc_dcount_lesser_2_code) != 0:
        print('A minimum of two doors, as per {} code, are required for Occupancy greater than 50 persons.'. format(code))
    else:
        pass
    # print('*'*30)
    if len(idx_of_insufficent_door_width_with_oc_dcount_lesser_2_code) != 0:
        print('IMPORTANT- Please note that the addin does not take into account Doors from linked Revit files.\nPlease do take into account these doors, additionally in the mentioned Rooms.')
    else:
        pass
    print('*'*120)
    
    ###########################################################################################################################################################
    
    # Occupancy Analysis for Rooms with Occupancy lesser than 50 ppl
    
    idx_oc_count_lesser_50_ppl_code= filter_room_egress_capacity(room_oc_count_sublist_by_lvl_as_per_code, 'lesser', 50)
    
    clean_oc_count_lesser_50_code= clean_filter_list(idx_oc_count_lesser_50_ppl_code, rooms_sublist_by_lvl_as_per_code, room_oc_count_sublist_by_lvl_as_per_code)
    flat_rooms_with_oc_count_lesser_50_code= clean_oc_count_lesser_50_code[0]
    filtered_rnames_as_oc_count_lesser_50_code= clean_oc_count_lesser_50_code[1]
    filtered_rnums_as_oc_count_lesser_50_code= clean_oc_count_lesser_50_code[2]
    filtered_room_oc_count_lesser_50_code= clean_oc_count_lesser_50_code[3]
 
    filter_doors_as_per_oc_count_lesser_50_code= lookup_doors_in_rooms_as_oc_count_filter(flat_rooms_with_oc_count_lesser_50_code, filtered_rnames_as_oc_count_lesser_50_code, filtered_rnums_as_oc_count_lesser_50_code, filtered_room_oc_count_lesser_50_code, door_room_nums, doors)
    filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_lesser_50_code= filter_doors_as_per_oc_count_lesser_50_code[0]
    rnums_with_doors_and_oc_as_count_lesser_50_code= filter_doors_as_per_oc_count_lesser_50_code[1]
    rnames_with_doors_and_oc_as_count_lesser_50_code= filter_doors_as_per_oc_count_lesser_50_code[2]
    rooms_with_doors_and_oc_as_count_lesser_50_code= filter_doors_as_per_oc_count_lesser_50_code[3]
    room_oc_count_for_rooms_with_doors_and_count_lesser_50_code= filter_doors_as_per_oc_count_lesser_50_code[4]
    
    # For occupant count lesser than 50 ppl and having one or more than one door
    
    idx_door_count_greater_0_on_dwidths_code= idx_filter_door_count_on_dwidths(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_lesser_50_code, 'greater', 0)
    
    filtered_rooms_as_per_oc_lesser_50_dcount_greater_0_code= room_info_filter_as_per_dcount_filter(idx_door_count_greater_0_on_dwidths_code, rnums_with_doors_and_oc_as_count_lesser_50_code,rnames_with_doors_and_oc_as_count_lesser_50_code, rooms_with_doors_and_oc_as_count_lesser_50_code, room_oc_count_for_rooms_with_doors_and_count_lesser_50_code)
     
    rnums_with_oc_lesser_50_and_dcount_greater_0_code= filtered_rooms_as_per_oc_lesser_50_dcount_greater_0_code[0]
    rnames_with_oc_lesser_50_and_dcount_greater_0_code= filtered_rooms_as_per_oc_lesser_50_dcount_greater_0_code[1] 
    rooms_with_oc_lesser_50_and_dcount_greater_0_code= filtered_rooms_as_per_oc_lesser_50_dcount_greater_0_code[2]
    room_oc_count_lesser_50_and_dcount_greater_0_code= filtered_rooms_as_per_oc_lesser_50_dcount_greater_0_code[3]    
    
    filtered_door_widths_as_per_oc_and_dcount_greater_0_code= door_widths_for_doors_in_rooms_with_oc_filter_dcount_filter(filtered_sublist_of_dwidth_of_doors_in_rooms_with_oc_lesser_50_code, idx_door_count_greater_0_on_dwidths_code, room_oc_count_lesser_50_and_dcount_greater_0_code)
    total_egress_width_for_doors_in_rooms_with_oc_dcount_greater_0_code= filtered_door_widths_as_per_oc_and_dcount_greater_0_code[0]
    total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_greater_0_code= filtered_door_widths_as_per_oc_and_dcount_greater_0_code[1]
    idx_of_insufficent_door_width_with_oc_dcount_greater_0_code = filtered_door_widths_as_per_oc_and_dcount_greater_0_code[2]
    print("Analysis of Rooms, as per {} code with Occupancy lesser than 50 persons & have one or more than one doors.".format(code))
    print('*'*30)  
    egress_width_analysis_code= output_analysis_for_door_widths(idx_of_insufficent_door_width_with_oc_dcount_greater_0_code, rnums_with_oc_lesser_50_and_dcount_greater_0_code, rnames_with_oc_lesser_50_and_dcount_greater_0_code, total_egress_width_for_doors_in_rooms_with_oc_dcount_greater_0_code, total_egress_width_reqd_for_doors_in_rooms_with_oc_dcount_greater_0_code) 
    if len(idx_of_insufficent_door_width_with_oc_dcount_greater_0_code) != 0:
        print('Please note that the addin does not take into account Doors from linked files.\nPlease do take into account these doors, additionally in the mentioned Rooms.')
    else:
        pass
    print('*'*120)   
  
####################################################################################################################
from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 

####################################################################################################################    

userInputcategory = SelectFromList('Select Fire Code to analyse for the Building.', ['01.NBC', '02.SBC', '03.IBC', '04.NFPA', '05.DCD', '06.BS', '07.FN'])
userInputcategory = str(userInputcategory)

######################################################################################################################
if userInputcategory == '01.NBC':

    occupancy_calculation_as_per_NBC = occupant_count_calculation(0)
    process_NBC_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_NBC, 'NBC')
  
######################################################################################################################
elif userInputcategory == '02.SBC':
    occupancy_calculation_as_per_SBC = occupant_count_calculation(1)
    process_SBC_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_SBC, 'SBC')
    
######################################################################################################################   
elif userInputcategory == '03.IBC':
    occupancy_calculation_as_per_IBC = occupant_count_calculation(2)
    process_IBC_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_IBC, 'IBC')
 
#####################################################################################################################
elif userInputcategory == '04.NFPA':
    occupancy_calculation_as_per_NFPA = occupant_count_calculation(3)
    process_NFPA_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_NFPA, 'NFPA')

######################################################################################################################
elif userInputcategory == '05.DCD':
    occupancy_calculation_as_per_DCD = occupant_count_calculation(4)
    process_DCD_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_DCD, 'DCD')
 
######################################################################################################################
elif userInputcategory == '06.BS':
    occupancy_calculation_as_per_BS = occupant_count_calculation(5)
    process_BS_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_BS, 'BS')
    
######################################################################################################################
elif userInputcategory == '07.FN':
    occupancy_calculation_as_per_FN = occupant_count_calculation(6)
    process_FN_calculations = process_occupant_count_calc_as_per_sel_code(occupancy_calculation_as_per_FN, 'FN')
      
######################################################################################################################
else:
    pass

#####################################################################################################################
 
