"""Door Detail Parameters"""

__title__ = "Door Detail Parameters"
__author__= "J K Roshan\nKerketta"

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from pyrevit import HOST_APP
from pyrevit import revit, DB
from itertools import chain
from itertools import islice
from pyrevit import framework

out = script.get_output()
out.add_style('body{font-family: CenturyGothic; font-size: 12pt; }')

####################################################################################################################

def format_length(length_value, doc = None):
    doc = doc or HOST_APP.doc
    return DB.UnitFormatUtils.Format(units = doc.GetUnits(), unitType = DB.UnitType.UT_Length, value = length_value, maxAccuracy = False, forEditing =False)

####################################################################################################################

import itertools
import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

####################################################################################################################

# Select Excel File from Folder

logger = script.get_logger()
# if__name__ == '__main__':

source_file = forms.pick_file(file_ext='xlsx')

# Reading an excel file using Python 
import xlrd 
from xlrd import open_workbook 

# Give the location of the file 
loc = source_file
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

#####################################################################################################################
# Read Excel Parameters and Family Category

identifier_param_to_read = sheet.col_values(5)

# Column values in Excel File
function_param_to_read = sheet.col_values(5)
door_Leaf_Number = sheet.col_values(6)
door_equal_leaves = sheet.col_values(7)
door_Leaf_Width = sheet.col_values(8)
door_Leaf_Height = sheet.col_values(9)
door_Undercut = sheet.col_values(10)

door_fire_rating = sheet.col_values(22)
door_host_fire_rating = sheet.col_values(21)
door_acoustics_rating = sheet.col_values(23)
door_Leaf_Material = sheet.col_values(12)
door_Frame_Material = sheet.col_values(16)
door_Leaf_Face_Finish = sheet.col_values(14)
door_Frame_Face_Finish = sheet.col_values(18)
door_grills = sheet.col_values(24)

door_Leaf_Type = sheet.col_values(11)
door_Leaf_Construction = sheet.col_values(13)
door_Frame_Elevation = sheet.col_values(15)
door_Frame_Profile = sheet.col_values(17)
door_Saddle_Type = sheet.col_values(19)

door_function_dictionary = {z[0]:list(z[1:]) for z in zip(function_param_to_read, door_Leaf_Number, door_equal_leaves, door_Leaf_Width, door_Leaf_Height, door_Undercut, door_fire_rating, door_host_fire_rating, door_acoustics_rating, door_Leaf_Material, door_Leaf_Face_Finish, door_Frame_Material, door_Frame_Face_Finish, door_grills, door_Leaf_Type, door_Leaf_Construction, door_Frame_Elevation, door_Frame_Profile, door_Saddle_Type)}
# print(door_function_dictionary)

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
# Master Door Information
# Removed Glazed doors as they donot have sufficient information

doors = all_elements_of_category(BuiltInCategory.OST_Doors)
# print(doors)
door_comments = [d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString() for d in doors]
# print(door_comments)

exclusions = ["ROLLING SHUTTER", "ACCESS PANEL", "CLOSET DOOR", "GLASS DOOR" , "CURTAIN WALL DOOR"]
# exclusions = [ "ACCESS PANEL"]

indices_for_non_glazed_doors = [i for i, x in enumerate(door_comments) if x not in exclusions]
# print(indices_for_non_glazed_doors)

####################################################################################################################
# Master Room Information
 
rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
room_numbers = []
for r in rooms:
    temp = []
    try:
        temp = r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()
    except:
        temp = 'None'
    room_numbers.append(temp)   

room_Selections = [out.linkify(r.Id) for r in rooms]  

####################################################################################################################
# Master Door Information- after filtering Doors

doors = [doors[i] for i in indices_for_non_glazed_doors]
# print(doors)

door_numbers = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in doors]
# print(door_numbers)

indices_of_sorted_doors = sorted(range(len(door_numbers)), key=lambda k: door_numbers[k])

doors = [doors[i] for i in indices_of_sorted_doors]
door_numbers = [door_numbers[i] for i in indices_of_sorted_doors]
# print(door_numbers)

# Getting Room Numbers in Doors 
door_room_numbers = shared_parameter_values(doors, 'Room_Number')
# print(door_room_numbers)

door_param_empty_or_None = [None, '']

indices_of_doors_with_missing_door_room_numbers = [i for i, x in enumerate(door_room_numbers) if x in door_param_empty_or_None]
door_numbers_with_missing_door_room_numbers = [door_numbers[i] for i in indices_of_doors_with_missing_door_room_numbers]
doors_with_missing_door_room_numbers = [doors[i] for i in indices_of_doors_with_missing_door_room_numbers]
door_Selections_with_missing_door_room_numbers = [out.linkify(door.Id) for door in doors_with_missing_door_room_numbers]     

indices_of_doors_with_door_room_numbers = [i for i, x in enumerate(door_room_numbers) if x not in door_param_empty_or_None]
doors = [doors[i] for i in indices_of_doors_with_door_room_numbers]
door_numbers = [door_numbers[i] for i in indices_of_doors_with_door_room_numbers]
door_room_numbers = [door_room_numbers[i] for i in indices_of_doors_with_door_room_numbers]

# Getting Room Names in Doors 
door_room_names = shared_parameter_values(doors, 'Room_Name')
indices_of_doors_with_missing_door_room_names = [i for i, x in enumerate(door_room_names) if x in door_param_empty_or_None]
door_numbers_with_missing_door_room_names = [door_numbers[i] for i in indices_of_doors_with_missing_door_room_names]
doors_with_missing_door_room_names = [doors[i] for i in indices_of_doors_with_missing_door_room_names]
door_Selections_with_missing_door_room_names = [out.linkify(door.Id) for door in doors_with_missing_door_room_names]   

indices_of_doors_with_door_room_names = [i for i, x in enumerate(door_room_names) if x not in door_param_empty_or_None]
doors = [doors[i] for i in indices_of_doors_with_door_room_names]
door_numbers = [door_numbers[i] for i in indices_of_doors_with_door_room_names]
door_room_numbers = [door_room_numbers[i] for i in indices_of_doors_with_door_room_names]
door_room_names = [door_room_names[i] for i in indices_of_doors_with_door_room_names]
# print(door_numbers, door_room_numbers, door_room_names)

door_Selections = [out.linkify(door.Id) for door in doors]             

####################################################################################################################

# Phase dependent Door properties

def troom_froom_name_for_doors(doors_to_acquire = doors):
    phases = doc.Phases
    phase = phases[phases.Size - 1]
    troom = []
    froom = []

    for d in doors_to_acquire:
        temp = []
        try:
            temp = d.FromRoom[phase]
            froom.append(temp)
        except:
            temp = 'fail'
            froom.append(temp)
        temp1 = []
        try:
            temp1 = d.ToRoom[phase]
            troom.append(temp1)
        except:
            temp1 = 'fail'
            troom.append(temp1)
    
    door_param_empty_or_None = [None, '']
    
    filtered_from_rooms_index = [i for i, x in enumerate(froom) if x not in door_param_empty_or_None]
    # print(filtered_from_rooms_index)
    filtered_from_rooms = [froom[i] for i in filtered_from_rooms_index]
    # print(filtered_from_rooms)
    FromRoomName = [[r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in filtered_from_rooms]]
    # print(FromRoomName)
    iter_flat_FromRoomName_list =  itertools.chain.from_iterable
    flat_FromRoomName_list = list(iter_flat_FromRoomName_list(FromRoomName))
    # print(flat_FromRoomName_list)
    froom_list_length = (len(froom))
    from_room_name_list = ["None"] * froom_list_length
    # print(from_room_name_list)
    # print(len(from_room_name_list))
    for (index, replacements) in zip(filtered_from_rooms_index,flat_FromRoomName_list):
        from_room_name_list[index] = replacements
    # print(from_room_name_list)

    filtered_to_rooms_index = [i for i, x in enumerate(troom) if x not in door_param_empty_or_None]
    filtered_to_rooms = [troom[i] for i in filtered_to_rooms_index]
    # print(filtered_to_rooms)
    ToRoomName = [[r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in filtered_to_rooms]]
    # print(ToRoomName)
    iter_flat_ToRoomName_list =  itertools.chain.from_iterable
    flat_ToRoomName_list = list(iter_flat_ToRoomName_list(ToRoomName))
    # print(flat_ToRoomName_list)
    troom_list_length = (len(troom))
    to_room_name_list = ["None"] * troom_list_length
    # print(to_room_name_list)
    # print(len(to_room_name_list))
    for (index, replacements) in zip(filtered_to_rooms_index,flat_ToRoomName_list):
        to_room_name_list[index] = replacements
    # print(to_room_name_list)
    return(to_room_name_list, from_room_name_list)

####################################################################################################################
# Getting To Room & From Room Door Info
door_to_from_name_list = troom_froom_name_for_doors(doors)
    
door_to_room_name_list = door_to_from_name_list[0]
door_from_room_name_list = door_to_from_name_list[1]
# print(door_to_from_name_list)

####################################################################################################################
# Function for checking Family Type Door Parameters(AsInteger, AsDouble, AsString)

def all_elements_with_type_parameter_AsInteger(sample_doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in sample_doors:
        door_type = d.Symbol
        door_family_param = door_type.LookupParameter(door_family_type_parameter)
        temp = []
        if door_family_param:
            temp = door_family_param.AsInteger()
            door_family_test.append(temp)
        else:
            temp = 'fail'
            door_family_test.append(temp)
    return door_family_test

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

def all_elements_with_type_parameter_AsString(sample_doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in sample_doors:
        door_type = d.Symbol
        door_family_param = door_type.LookupParameter(door_family_type_parameter)
        temp = []
        if door_family_param:
            temp = door_family_param.AsString()
            door_family_test.append(temp)
        else:
            temp = 'fail'
            door_family_test.append(temp)
    return door_family_test

# Getting failed elements (Doors & Door Numbers)-using value from previous function for Family type test
def doors_with_family_param_failure(door_family_test,sample_doors, sample_door_numbers):
    index_of_doors_with_family_param_failure = [i for i, x in enumerate(door_family_test) if x == 'fail']
    doors_with_family_test_issues = [sample_doors[i] for i in index_of_doors_with_family_param_failure]
    door_numbers_with_family_test_issues = [sample_door_numbers[i] for i in index_of_doors_with_family_param_failure]        
    return (doors_with_family_test_issues, door_numbers_with_family_test_issues)
 
# Getting passed elements (Doors & Door Numbers)
def doors_with_family_param_pass(door_family_test,sample_doors, sample_door_numbers):
    index_of_doors_with_family_param_pass = [i for i, x in enumerate(door_family_test) if x != 'fail']
    doors_with_family_test_pass = [sample_doors[i] for i in index_of_doors_with_family_param_pass]
    door_numbers_with_family_test_pass = [sample_door_numbers[i] for i in index_of_doors_with_family_param_pass]
    return (doors_with_family_test_pass, door_numbers_with_family_test_pass)

####################################################################################################################
# Function for unit conversion

def unit_conversion(revit_value_in_feet):
    resultant_value_from_revit = [float(x) for x in revit_value_in_feet]
    resultant_value_unit_conversion = [format_length(x) for x in resultant_value_from_revit]
    resultant_value_converted_to_mm = [int(x) for x in resultant_value_unit_conversion]
    return(resultant_value_converted_to_mm)

####################################################################################################################
# Extract Shared Parameter values, returns index of valid and None values

def elem_param_values_test(elems, parameter_name):
    elem_param_values = shared_parameter_values(elems,parameter_name)
    elem_param_empty_or_None = [None, '']
    elem_param_None_index = [i for i, x in enumerate(elem_param_values) if x in elem_param_empty_or_None]
    elem_param_valid_index = [ i for i, x in enumerate(elem_param_values) if x not in elem_param_empty_or_None]
    return (elem_param_values, elem_param_valid_index, elem_param_None_index)

####################################################################################################################

######### IMPORTANT ################## IMPORTANT ###################### IMPORTANT ##################################
# Prior to running any scripts, please ensure Doors to have functions using below
 
door_function_values_with_index = elem_param_values_test(doors, "Room_Function")
# print(door_function_values_with_index)
door_function_values = door_function_values_with_index[0]
index_for_doors_with_functions_assigned = door_function_values_with_index[1]
index_for_doors_with_no_functions_assigned = door_function_values_with_index[2]

filtered_door_function_values = [door_function_values[i] for i in index_for_doors_with_functions_assigned]
# print(filtered_door_function_values)

doors_with_no_functions_assigned = [doors[i] for i in index_for_doors_with_no_functions_assigned]

doors_with_functions = [doors[i] for i in index_for_doors_with_functions_assigned]
door_numbers_with_functions = [door_numbers[i] for i in index_for_doors_with_functions_assigned]
door_room_numbers_with_functions = [door_room_numbers[i] for i in index_for_doors_with_functions_assigned]
door_room_names_with_functions = [door_room_names[i] for i in index_for_doors_with_functions_assigned]
door_to_room_names_with_functions = [door_to_room_name_list[i] for i in index_for_doors_with_functions_assigned]
door_from_room_names_with_functions = [door_from_room_name_list[i] for i in index_for_doors_with_functions_assigned]
door_Selections_with_functions = [door_Selections[i] for i in index_for_doors_with_functions_assigned]         

door_function_values_invalid = list((set(door_function_values).difference(identifier_param_to_read)))
index_of_invalid_door_functions = []    
for i in range(len(filtered_door_function_values)):
    if filtered_door_function_values[i] in door_function_values_invalid:
        index_of_invalid_door_functions.append(i)
# print(index_of_invalid_door_functions)  

doors_with_invalid_functions = [doors_with_functions[i] for i in index_of_invalid_door_functions]

set_index_of_invalid_door_functions = set(index_of_invalid_door_functions)
doors_with_valid_functions = [ e for i, e in enumerate(doors_with_functions) if i not in set_index_of_invalid_door_functions]
door_numbers_with_valid_functions = [ e for i, e in enumerate(door_numbers_with_functions) if i not in set_index_of_invalid_door_functions]
door_room_numbers_with_valid_functions = [ e for i, e in enumerate(door_room_numbers_with_functions) if i not in set_index_of_invalid_door_functions]
door_room_names_with_valid_functions = [ e for i, e in enumerate(door_room_names_with_functions) if i not in set_index_of_invalid_door_functions]
door_to_room_names_with_valid_functions = [ e for i, e in enumerate(door_to_room_names_with_functions) if i not in set_index_of_invalid_door_functions]
door_from_room_names_with_valid_functions = [ e for i, e in enumerate(door_from_room_names_with_functions) if i not in set_index_of_invalid_door_functions]
door_Selections_with_valid_functions = [ e for i, e in enumerate(door_Selections_with_functions) if i not in set_index_of_invalid_door_functions]           # test

# print(door_numbers_with_valid_functions)
filtered_door_function_valid_values = [e for i, e in enumerate(filtered_door_function_values) if i not in set_index_of_invalid_door_functions]
# print(filtered_door_function_valid_values)

####################################################################################################################
####################################################################################################################

def mismatch_index_for_door_parameters(values_filtered_from_dictionary,test_to_compare_door_dimensions):
    y = 0
    mismatch_index_for_door_parameter_to_assess = []
    for x in values_filtered_from_dictionary:
        if x != test_to_compare_door_dimensions[y]:
            mismatch_index_for_door_parameter_to_assess.append(y)
        y = y + 1
    return(mismatch_index_for_door_parameter_to_assess)

####################################################################################################################
####################################################################################################################

# Door Leaf Number

test_for_doors_with_leaves = all_elements_with_type_parameter_AsInteger(doors_with_valid_functions, 'Leaf_Number')

# print(test_for_doors_with_leaves)
test_for_doors_with_leaves = [float(x) for x in test_for_doors_with_leaves]
values_from_dict_leaf_number = [door_function_dictionary[x][0] for x in filtered_door_function_valid_values]     # value column index from dictionary for the key list
mismatch_index_for_door_leaf_number = mismatch_index_for_door_parameters(values_from_dict_leaf_number, test_for_doors_with_leaves)
# print(mismatch_index_for_door_leaf_number)

set_index_of_mismatch_door_leaf_number = set(mismatch_index_for_door_leaf_number)
doors_with_valid_leaf_number = [ e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_number]
door_numbers_with_valid_leaf_number = [ e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_number]
# print(door_numbers_with_valid_leaf_number)

filtered_door_leaf_valid_values = [e for i, e in enumerate(test_for_doors_with_leaves) if i not in set_index_of_mismatch_door_leaf_number]

####################################################################################################################
# Door Equal/Unequal Leaves

# Double Doors

index_of_doors_with_double_leaves = [ i for i, x in enumerate(filtered_door_leaf_valid_values) if x == 2]
doors_with_double_leaves = [doors_with_valid_leaf_number[i] for i in index_of_doors_with_double_leaves]
door_numbers_with_double_leaves = [door_numbers_with_valid_leaf_number[i] for i in index_of_doors_with_double_leaves]
# print(door_numbers_with_double_leaves)

####################################################################################################################
# Double Equal/Unequal Leaf Doors

test_for_double_doors_equal_unequal = all_elements_with_type_parameter_AsDouble(doors_with_double_leaves, 'Side Panel Width')
# print(test_for_double_doors_equal_unequal)

####################################################################################################################
# Double Unequal Leaf Doors

test_for_double_doors_unequal_pass = doors_with_family_param_pass(test_for_double_doors_equal_unequal,doors_with_double_leaves, door_numbers_with_double_leaves)
# print(test_for_double_doors_unequal_pass)

double_doors_with_unequal_leaves = test_for_double_doors_unequal_pass[0]
double_door_numbers_with_unequal_leaves = test_for_double_doors_unequal_pass[1]

test_for_double_doors_unequal = all_elements_with_type_parameter_AsInteger(double_doors_with_unequal_leaves, 'Equal_Leaves')
# print(test_for_double_doors_unequal)

door_function_for_doors_with_double_leaves_unequal = elem_param_values_test(double_doors_with_unequal_leaves, "Room_Function")
# print(door_function_for_doors_with_double_leaves_unequal)
door_function_values_for_doors_with_double_leaves_unequal = door_function_for_doors_with_double_leaves_unequal[0]

values_from_dict_equal_unequal_leaves = [door_function_dictionary[x][1] for x in door_function_values_for_doors_with_double_leaves_unequal]  
mismatch_index_for_door_with_unequal_leaves = mismatch_index_for_door_parameters(values_from_dict_equal_unequal_leaves, test_for_double_doors_unequal)

set_index_of_mismatch_door_with_unequal_leaves = set(mismatch_index_for_door_with_unequal_leaves)
doors_with_valid_unequal_leaves = [ e for i, e in enumerate(double_doors_with_unequal_leaves) if i not in set_index_of_mismatch_door_with_unequal_leaves]
door_numbers_with_valid_unequal_leaves = [ e for i, e in enumerate(double_door_numbers_with_unequal_leaves) if i not in set_index_of_mismatch_door_with_unequal_leaves]
# print(door_numbers_with_valid_unequal_leaves)

####################################################################################################################
# Double Equal Leaf Doors

test_for_double_doors_equal_leaves = doors_with_family_param_failure(test_for_double_doors_equal_unequal,doors_with_double_leaves, door_numbers_with_double_leaves)
# print(test_for_double_doors_equal_leaves)

double_doors_with_equal_leaves = test_for_double_doors_equal_leaves[0]
double_door_numbers_with_equal_leaves = test_for_double_doors_equal_leaves[1]

test_for_double_doors_equal = all_elements_with_type_parameter_AsInteger(double_doors_with_equal_leaves, 'Equal_Leaves')
# print(test_for_double_doors_equal)

door_function_for_doors_with_double_equal_leaves = elem_param_values_test(double_doors_with_equal_leaves, "Room_Function")
# print(door_function_for_doors_with_double_equal_leaves)
door_function_values_for_doors_with_double_equal_leaves = door_function_for_doors_with_double_equal_leaves[0]
values_from_dict_equal_leaves = [door_function_dictionary[x][1] for x in door_function_values_for_doors_with_double_equal_leaves]  
# print(values_from_dict_equal_leaves)

mismatch_index_for_door_with_equal_leaves = mismatch_index_for_door_parameters(values_from_dict_equal_leaves, test_for_double_doors_equal)
# print(mismatch_index_for_door_with_equal_leaves)

set_index_of_mismatch_door_with_equal_leaves = set(mismatch_index_for_door_with_equal_leaves)
doors_with_valid_equal_leaves = [ e for i, e in enumerate(double_doors_with_equal_leaves) if i not in set_index_of_mismatch_door_with_equal_leaves]
door_numbers_with_valid_equal_leaves = [ e for i, e in enumerate(double_door_numbers_with_equal_leaves) if i not in set_index_of_mismatch_door_with_equal_leaves]
# print(door_numbers_with_valid_equal_leaves)

####################################################################################################################
# Single Leaf Doors

index_of_doors_with_single_leaf = [ i for i, x in enumerate(filtered_door_leaf_valid_values) if x == 1]
doors_with_single_leaf = [doors_with_valid_leaf_number[i] for i in index_of_doors_with_single_leaf]
door_numbers_with_single_leaf = [door_numbers_with_valid_leaf_number[i] for i in index_of_doors_with_single_leaf]
# print(door_numbers_with_single_leaf)

test_for_single_doors_unequal = all_elements_with_type_parameter_AsInteger(doors_with_single_leaf, 'Equal_Leaves')
# print(test_for_single_doors_unequal)

door_function_for_doors_with_single_leaf_unequal = elem_param_values_test(doors_with_single_leaf, "Room_Function")
# print(door_function_for_doors_with_single_unequal)
door_function_values_for_doors_with_single_unequal = door_function_for_doors_with_single_leaf_unequal[0]
# print(door_function_values_for_doors_with_single_unequal)

values_from_dict_single_equal_unequal_leaf = [door_function_dictionary[x][1] for x in door_function_values_for_doors_with_single_unequal]  
# print(values_from_dict_single_equal_unequal_leaf)

mismatch_index_for_door_with_single_equal_unequal_leaf = mismatch_index_for_door_parameters(values_from_dict_single_equal_unequal_leaf, test_for_single_doors_unequal)
# print(mismatch_index_for_door_with_single_equal_unequal_leaf)

set_index_of_mismatch_door_with_single_equal_unequal_leaf = set(mismatch_index_for_door_with_single_equal_unequal_leaf)
doors_with_valid_single_equal_leaf = [ e for i, e in enumerate(doors_with_single_leaf) if i not in set_index_of_mismatch_door_with_single_equal_unequal_leaf]
door_numbers_with_valid_single_equal_leaf = [ e for i, e in enumerate(door_numbers_with_single_leaf) if i not in set_index_of_mismatch_door_with_single_equal_unequal_leaf]
# print(door_numbers_with_valid_single_equal_leaf)

###################################################################################################################
###################################################################################################################
# Index of mismatching door sizes

# Equal Doors

def test_for_door_dimensions(filtered_doors, param, sheet_col_val):
    test_for_door_dimensions = all_elements_with_type_parameter_AsDouble(filtered_doors, param)
    test_for_door_dimension_unit_convert = unit_conversion(test_for_door_dimensions)
    #print(test_for_door_dimension_unit_convert)
    
    door_function_for_doors_with_tested_dimensions = elem_param_values_test(filtered_doors, 'Room_Function')
    door_function_values_for_doors_with_tested_dimensions = door_function_for_doors_with_tested_dimensions[0]
    # print(door_function_values_for_doors_with_tested_dimensions)

    values_from_dict_for_filtered_doors = [door_function_dictionary[x][sheet_col_val] for x in door_function_values_for_doors_with_tested_dimensions]
    values_from_dict_for_filtered_doors = [int(x) for x in values_from_dict_for_filtered_doors]

    mismatch_index_values_for_door_parameters_in_assessment = mismatch_index_for_door_parameters(values_from_dict_for_filtered_doors, test_for_door_dimension_unit_convert)
    return(mismatch_index_values_for_door_parameters_in_assessment)        

# Unequal Doors- Widths

def test_for_unequal_door_dimensions(filtered_doors, param, sheet_col_val):
    test_for_door_dimensions = all_elements_with_type_parameter_AsDouble(filtered_doors, param)
    test_for_door_dimension_unit_convert = unit_conversion(test_for_door_dimensions)
    #print(test_for_door_dimension_unit_convert)
    
    door_function_for_doors_with_tested_dimensions = elem_param_values_test(filtered_doors, 'Room_Function')
    door_function_values_for_doors_with_tested_dimensions = door_function_for_doors_with_tested_dimensions[0]
    # print(door_function_values_for_doors_with_tested_dimensions)

    values_from_dict_for_filtered_doors = [door_function_dictionary[x][sheet_col_val] for x in door_function_values_for_doors_with_tested_dimensions]
    split_val_dict = [x.split("+") for x in values_from_dict_for_filtered_doors]
    
    main_panel_width = [panel[0] for panel in split_val_dict]
    side_panel_width = [panel[1] for panel in split_val_dict]
    
    if param == 'Main Panel Width':
        values_to_assess = main_panel_width
    else:
        values_to_assess = side_panel_width
 
    values_to_asess = [int(x) for x in values_to_assess]

    y = 0
    mismatch_index_for_unequal_door_parameter_to_assess = []
    for x in values_to_asess:
        if x != test_for_door_dimension_unit_convert [y]:
            mismatch_index_for_unequal_door_parameter_to_assess.append(y)
        y = y + 1
    return(mismatch_index_for_unequal_door_parameter_to_assess)
   
    mismatch_index_values_for_door_parameters_in_assessment = mismatch_index_for_unequal_door_parameters(values_to_assess, test_for_door_dimension_unit_convert)
    return(mismatch_index_values_for_door_parameters_in_assessment)       

###################################################################################################################
####################################################################################################################
# Leaf Widths
# Single Leaf Doors

test_index_for_single_doors_width = test_for_door_dimensions(doors_with_valid_single_equal_leaf, 'Leaf_Width', 2)
# print(test_index_for_single_doors_width)
set_index_of_mismatch_doors_with_single_leaf_width = set(test_index_for_single_doors_width)
doors_with_valid_single_leaf_width = [ e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i not in set_index_of_mismatch_doors_with_single_leaf_width]
door_numbers_with_valid_single_leaf_width = [ e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i not in set_index_of_mismatch_doors_with_single_leaf_width]

# Double Equal Leaf Doors

test_index_for_double_equal_doors_width = test_for_door_dimensions(doors_with_valid_equal_leaves, 'Leaf_Width', 2)
# print(test_index_for_double_equal_doors_width)
set_index_of_mismatch_doors_with_double_equal_leaves_width = set(test_index_for_double_equal_doors_width)
doors_with_valid_double_equal_leaves_width = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_double_equal_leaves_width]
door_numbers_with_valid_double_equal_leaves_width = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_double_equal_leaves_width]

# Double Unequal Leaf Doors
# Main Panel Width

test_index_for_double_unequal_doors_main_panel_width = test_for_unequal_door_dimensions(doors_with_valid_unequal_leaves, 'Main Panel Width', 2)
# print(test_index_for_double_unequal_doors_main_panel_width)
set_index_of_mismatch_doors_with_unequal_main_panel_width = set(test_index_for_double_unequal_doors_main_panel_width)
doors_with_valid_unequal_leaves_main_panel_width = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_unequal_main_panel_width]
door_numbers_with_valid_unequal_leaves_main_panel_width = [ e for i, e in enumerate(door_numbers_with_valid_unequal_leaves) if i not in set_index_of_mismatch_doors_with_unequal_main_panel_width]

# Side Panel Width

test_index_for_double_unequal_doors_side_panel_width = test_for_unequal_door_dimensions(doors_with_valid_unequal_leaves, 'Side Panel Width', 2)
# print(test_index_for_double_unequal_doors_side_panel_width)
set_index_of_mismatch_doors_with_unequal_side_panel_width = set(test_index_for_double_unequal_doors_side_panel_width)
doors_with_valid_unequal_leaves_side_panel_width = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_unequal_side_panel_width]
door_numbers_with_valid_unequal_leaves_side_panel_width = [ e for i, e in enumerate(door_numbers_with_valid_unequal_leaves) if i not in set_index_of_mismatch_doors_with_unequal_side_panel_width]

####################################################################################################################
####################################################################################################################
# Leaf Height
# Single Leaf Doors

test_index_for_single_doors_height = test_for_door_dimensions(doors_with_valid_single_equal_leaf, 'Leaf_Height', 3)
# print(test_for_single_doors_height_unit_convert)

set_index_of_mismatch_doors_with_single_leaf_height = set(test_index_for_single_doors_height)
doors_with_valid_single_leaf_height = [ e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i not in set_index_of_mismatch_doors_with_single_leaf_height]
door_numbers_with_valid_single_leaf_height = [ e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i not in set_index_of_mismatch_doors_with_single_leaf_height]

####################################################################################################################
# Double Equal Leaf Doors

test_index_for_double_equal_doors_height = test_for_door_dimensions(doors_with_valid_equal_leaves, 'Leaf_Height', 3)
# print(test_index_for_double_equal_doors_height_unit_convert)

set_index_of_mismatch_doors_with_double_equal_leaves_height = set(test_index_for_double_equal_doors_height)
doors_with_valid_double_equal_leaves_height = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_double_equal_leaves_height]
door_numbers_with_valid_double_equal_leaves_height = [ e for i, e in enumerate(doors_with_valid_equal_leaves) if i not in set_index_of_mismatch_doors_with_double_equal_leaves_height]

####################################################################################################################
# Double Unqual Leaf Doors

test_index_for_double_unequal_doors_height = test_for_door_dimensions(doors_with_valid_unequal_leaves, 'Leaf_Height', 3)
# print(test_index_for_double_unequal_doors_height_unit_convert)

set_index_of_mismatch_doors_with_double_unequal_leaves_height = set(test_index_for_double_unequal_doors_height)
doors_with_valid_double_unequal_leaves_height = [ e for i, e in enumerate(doors_with_valid_unequal_leaves) if i not in set_index_of_mismatch_doors_with_double_unequal_leaves_height]
door_numbers_with_valid_double_equal_leaves_height = [ e for i, e in enumerate(doors_with_valid_unequal_leaves) if i not in set_index_of_mismatch_doors_with_double_unequal_leaves_height]

####################################################################################################################
####################################################################################################################
# Door Fire Rating
# Door Leaf Height, Width, Equal/Unequal Single don't matter for Door Fire Rating so directly accessing doors after fixing door numbers, room names/numbers, etc.

fire_rating_for_doors_with_index = elem_param_values_test(doors_with_valid_functions, 'Fire_Rating')
# print(fire_rating_for_doors_with_index)

fire_rating_values = fire_rating_for_doors_with_index[0]
index_for_doors_with_fire_rating_assigned = fire_rating_for_doors_with_index[1]
index_for_doors_with_no_fire_rating_assigned = fire_rating_for_doors_with_index[2]

filtered_door_fire_rating_values = [fire_rating_values[i] for i in index_for_doors_with_fire_rating_assigned]
filtered_door_fire_rating_values = [int(x) for x in filtered_door_fire_rating_values]
# print(filtered_door_fire_rating_values)

####################################################################################################################
# Doors with no Fire rating assigned

doors_with_no_fire_rating_assigned = [doors_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]

doors_with_fire_rating = [doors_with_valid_functions[i] for i in index_for_doors_with_fire_rating_assigned]
door_numbers_with_fire_rating = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_fire_rating_assigned]

door_function_for_doors_with_fire_rating = elem_param_values_test(doors_with_fire_rating, "Room_Function")
# print(door_function_for_doors_with_fire_rating)
door_function_values_for_doors_with_fire_rating = door_function_for_doors_with_fire_rating[0]
# print(door_function_values_for_doors_with_fire_rating)
values_from_dict_doors_with_fire_rating = [door_function_dictionary[x][5] for x in door_function_values_for_doors_with_fire_rating]
# values_from_dict_doors_with_fire_rating = [int(x) for x in values_from_dict_doors_with_fire_rating]
# print(values_from_dict_doors_with_fire_rating)

####################################################################################################################
# Doors with mismatch Fire rating assigned

mismatch_index_for_doors_with_fire_rating = mismatch_index_for_door_parameters(values_from_dict_doors_with_fire_rating, filtered_door_fire_rating_values)
# print(mismatch_index_for_doors_with_fire_rating)

set_index_of_mismatch_door_with_fire_rating = set(mismatch_index_for_doors_with_fire_rating)
doors_with_invalid_fire_rating = [e for i, e in enumerate(doors_with_fire_rating) if i in set_index_of_mismatch_door_with_fire_rating]

####################################################################################################################
# Doors with valid matching Fire rating assigned

doors_with_valid_fire_rating = [e for i, e in enumerate(doors_with_fire_rating) if i not in set_index_of_mismatch_door_with_fire_rating]
door_numbers_with_valid_fire_rating = [e for i, e in enumerate(door_numbers_with_fire_rating) if i not in set_index_of_mismatch_door_with_fire_rating]
# print(door_numbers_with_valid_fire_rating)

wall_host_for_fire_doors = []
for d in doors_with_valid_fire_rating :
    temp = []
    wallId = d.Host.Id
        
    temp = doc.GetElement(wallId)
    wall_host_for_fire_doors.append(temp)
# print(wall_host_for_fire_doors)

wall_fire_rating = []
for w in wall_host_for_fire_doors:
    for param in w.Parameters:
        if param.IsShared and param.Definition.Name == 'Fire_Rating':
            paramValue = w.get_Parameter(param.GUID)
            wall_fire_rating.append(paramValue.AsString())
  
# print(wall_fire_rating)

errors = [None, ""]

####################################################################################################################
# Doors with Fire Rating but no Wall Rating

index_of_fire_rated_doors_with_no_wall_fire_rating = [i for i, x in enumerate(wall_fire_rating) if x in errors]
doors_with_fire_rating_but_no_wall_fire_rating = [doors_with_valid_fire_rating[i] for i in index_of_fire_rated_doors_with_no_wall_fire_rating]
# print(doors_with_fire_rating_but_no_wall_fire_rating)

index_of_fire_rated_doors_with_wall_fire_rating = [i for i, x in enumerate(wall_fire_rating) if x not in errors]
fire_rated_walls_with_doors = [wall_host_for_fire_doors[i] for i in index_of_fire_rated_doors_with_wall_fire_rating]
fire_rated_wall_ratings_for_doors_with_fire_ratings = [wall_fire_rating[i] for i in index_of_fire_rated_doors_with_wall_fire_rating]
fire_rated_wall_ratings_for_doors_with_fire_ratings = [int(x) for x in fire_rated_wall_ratings_for_doors_with_fire_ratings]
# print(fire_rated_wall_ratings_for_doors_with_fire_ratings)

doors_with_fire_rating_and_wall_rating = [doors_with_valid_fire_rating[i] for i in index_of_fire_rated_doors_with_wall_fire_rating]
door_numbers_with_fire_rating_and_wall_rating = [door_numbers_with_valid_fire_rating[i] for i in index_of_fire_rated_doors_with_wall_fire_rating]
door_fire_rating_values_with_fire_rated_walls = shared_parameter_values(doors_with_fire_rating_and_wall_rating , 'Fire_Rating')
door_fire_rating_values_with_fire_rated_walls = [int(x) for x in door_fire_rating_values_with_fire_rated_walls]
# print(door_fire_rating_values_with_fire_rated_walls)

expected_door_ratings_as_per_wall_fire_ratings = [(0.75 * x) for x in fire_rated_wall_ratings_for_doors_with_fire_ratings]

mismatch_index_for_doors_against_wall_ratings = mismatch_index_for_door_parameters(expected_door_ratings_as_per_wall_fire_ratings, door_fire_rating_values_with_fire_rated_walls)
# print(mismatch_index_for_doors_against_wall_ratings)

set_index_of_mismatch_doors_fire_rating_against_wall_ratings= set(mismatch_index_for_doors_against_wall_ratings)
doors_with_walls_with_invalid_fire_ratings = [e for i, e in enumerate(doors_with_fire_rating_and_wall_rating) if i in set_index_of_mismatch_doors_fire_rating_against_wall_ratings]

doors_with_walls_with_valid_fire_ratings = [e for i, e in enumerate(doors_with_fire_rating_and_wall_rating) if i not in set_index_of_mismatch_doors_fire_rating_against_wall_ratings]
door_numbers_with_walls_with_valid_fire_ratings = [e for i, e in enumerate(door_numbers_with_fire_rating_and_wall_rating) if i not in set_index_of_mismatch_doors_fire_rating_against_wall_ratings]

####################################################################################################################
####################################################################################################################
# Door Acoustic Rating
# Door Leaf Height, Width, Equal/Unequal Single don't matter for Door Acoustic Rating so directly accessing doors after fixing door numbers, room names/numbers, etc.

acoustic_rating_for_doors_with_index = elem_param_values_test(doors_with_valid_functions, 'STC_Rating')
# print(acoustic_rating_for_doors_with_index)

acoustic_rating_values = acoustic_rating_for_doors_with_index[0]
index_for_doors_with_acoustic_rating_assigned = acoustic_rating_for_doors_with_index[1]
index_for_doors_with_no_acoustic_rating_assigned = acoustic_rating_for_doors_with_index[2]

filtered_door_acoustic_rating_values = [acoustic_rating_values[i] for i in index_for_doors_with_acoustic_rating_assigned]
filtered_door_acoustic_rating_values = [s.replace(".","") for s in filtered_door_acoustic_rating_values]
filtered_door_acoustic_rating_values = [int(x) for x in filtered_door_acoustic_rating_values]
# print(filtered_door_acoustic_rating_values)

####################################################################################################################
# Doors with no acoustic rating assigned

doors_with_no_acoustic_rating_assigned = [doors_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]

doors_with_acoustic_rating = [doors_with_valid_functions[i] for i in index_for_doors_with_acoustic_rating_assigned]
door_numbers_with_acoustic_rating = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_acoustic_rating_assigned]

door_function_for_doors_with_acoustic_rating = elem_param_values_test(doors_with_acoustic_rating, "Room_Function")
# print(door_function_for_doors_with_acoustic_rating)
door_function_values_for_doors_with_acoustic_rating = door_function_for_doors_with_acoustic_rating[0]
# print(door_function_values_for_doors_with_acoustic_rating)
values_from_dict_doors_with_acoustic_rating = [door_function_dictionary[x][7] for x in door_function_values_for_doors_with_acoustic_rating]
values_from_dict_doors_with_acoustic_rating = [int(x) for x in values_from_dict_doors_with_acoustic_rating]
# print(values_from_dict_doors_with_acoustic_rating)

####################################################################################################################
# Doors with mismatch Acoustic rating assigned

mismatch_index_for_doors_with_acoustic_rating = mismatch_index_for_door_parameters(values_from_dict_doors_with_acoustic_rating, filtered_door_acoustic_rating_values)
# print(mismatch_index_for_doors_with_acoustic_rating)

set_index_of_mismatch_door_with_acoustic_rating = set(mismatch_index_for_doors_with_acoustic_rating)
doors_with_invalid_acoustic_rating = [e for i, e in enumerate(doors_with_acoustic_rating) if i in set_index_of_mismatch_door_with_acoustic_rating]

####################################################################################################################
# Doors with valid matching Acoustic rating assigned

doors_with_valid_acoustic_rating = [e for i, e in enumerate(doors_with_acoustic_rating) if i not in set_index_of_mismatch_door_with_acoustic_rating]
door_numbers_with_valid_acoustic_rating = [e for i, e in enumerate(door_numbers_with_acoustic_rating) if i not in set_index_of_mismatch_door_with_acoustic_rating]
# print(door_numbers_with_valid_acoustic_rating)

wall_host_for_acoustic_doors = []
for d in doors_with_valid_acoustic_rating :
    temp = []
    wallId = d.Host.Id
        
    temp = doc.GetElement(wallId)
    wall_host_for_acoustic_doors.append(temp)
# print(wall_host_for_acoustic_doors)

wall_acoustic_rating = []
for w in wall_host_for_acoustic_doors:
    for param in w.Parameters:
        if param.IsShared and param.Definition.Name == 'STC_Rating':
            paramValue = w.get_Parameter(param.GUID)
            wall_acoustic_rating.append(paramValue.AsString())
  
# print(wall_acoustic_rating)

errors = [None, ""]

####################################################################################################################
# Doors with Acoustic Rating but no Wall Rating

index_of_acoustic_rated_doors_with_no_wall_acoustic_rating = [i for i, x in enumerate(wall_acoustic_rating) if x in errors]
doors_with_acoustic_rating_but_no_wall_acoustic_rating = [doors_with_valid_acoustic_rating[i] for i in index_of_acoustic_rated_doors_with_no_wall_acoustic_rating]
# print(doors_with_acoustic_rating_but_no_wall_acoustic_rating)

index_of_acoustic_rated_doors_with_wall_acoustic_rating = [i for i, x in enumerate(wall_acoustic_rating) if x not in errors]
acoustic_rated_walls_with_doors = [wall_host_for_acoustic_doors[i] for i in index_of_acoustic_rated_doors_with_wall_acoustic_rating]
acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings = [wall_acoustic_rating[i] for i in index_of_acoustic_rated_doors_with_wall_acoustic_rating]
acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings = [s.replace(".","") for s in acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings]
acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings = [int(x) for x in acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings]
# print(acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings)

doors_with_acoustic_rating_and_wall_rating = [doors_with_valid_acoustic_rating[i] for i in index_of_acoustic_rated_doors_with_wall_acoustic_rating]
door_numbers_with_acoustic_rating_and_wall_rating = [door_numbers_with_valid_acoustic_rating[i] for i in index_of_acoustic_rated_doors_with_wall_acoustic_rating]
door_acoustic_rating_values_with_acoustic_rated_walls = shared_parameter_values(doors_with_acoustic_rating_and_wall_rating , 'STC_Rating')
door_acoustic_rating_values_with_acoustic_rated_walls = [int(x) for x in door_acoustic_rating_values_with_acoustic_rated_walls]
# print(door_acoustic_rating_values_with_acoustic_rated_walls)

expected_door_ratings_as_per_wall_acoustic_ratings = [(x - 15) for x in acoustic_rated_wall_ratings_for_doors_with_acoustic_ratings]

mismatch_index_for_doors_against_wall_ratings = mismatch_index_for_door_parameters(expected_door_ratings_as_per_wall_acoustic_ratings, door_acoustic_rating_values_with_acoustic_rated_walls)
# print(mismatch_index_for_doors_against_wall_ratings)

set_index_of_mismatch_doors_acoustic_rating_against_wall_ratings= set(mismatch_index_for_doors_against_wall_ratings)
doors_with_walls_with_invalid_acoustic_ratings = [e for i, e in enumerate(doors_with_acoustic_rating_and_wall_rating) if i in set_index_of_mismatch_doors_acoustic_rating_against_wall_ratings]

doors_with_walls_with_valid_acoustic_ratings = [e for i, e in enumerate(doors_with_acoustic_rating_and_wall_rating) if i not in set_index_of_mismatch_doors_acoustic_rating_against_wall_ratings]
door_numbers_with_walls_with_valid_acoustic_ratings = [e for i, e in enumerate(door_numbers_with_acoustic_rating_and_wall_rating) if i not in set_index_of_mismatch_doors_acoustic_rating_against_wall_ratings]

####################################################################################################################
####################################################################################################################

def leaf_frame_material_finishes_type_mismatch_index(material_or_finish_param, doors_to_check, sheet_col_to_check):
    test_for_doors_with_material_or_finish = all_elements_with_type_parameter_AsString(doors_to_check, material_or_finish_param)
    door_function_for_doors_with_material_or_finish = elem_param_values_test(doors_to_check, 'Room_Function') 
    door_function_values_for_doors_with_material_or_finish = door_function_for_doors_with_material_or_finish[0]
    values_from_dict_material_or_finish = [door_function_dictionary[x][sheet_col_to_check] for x in door_function_values_for_doors_with_material_or_finish]
    values_dict_split_with_multi_elements = [x.split("/") for x in values_from_dict_material_or_finish]
    mismatch_index_for_door_material_or_finish = [ i for i, (a,b) in enumerate(zip(test_for_doors_with_material_or_finish, values_dict_split_with_multi_elements)) if not a in b]
    return(mismatch_index_for_door_material_or_finish)

####################################################################################################################
# Leaf Material

mismatch_index_for_doors_leaf_material = leaf_frame_material_finishes_type_mismatch_index('Leaf_Material', doors_with_valid_functions, 8)
set_index_of_mismatch_doors_leaf_material= set(mismatch_index_for_doors_leaf_material)
doors_with_invalid_leaf_material = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_doors_leaf_material]

doors_with_valid_leaf_material = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_doors_leaf_material]
door_numbers_with_valid_leaf_material = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_doors_leaf_material]
# print(door_numbers_with_valid_leaf_material)

####################################################################################################################
# Leaf Finish

mismatch_index_for_doors_leaf_finish = leaf_frame_material_finishes_type_mismatch_index('Leaf_Face_Finish', doors_with_valid_functions, 9)
set_index_of_mismatch_doors_leaf_finish = set(mismatch_index_for_doors_leaf_finish)
doors_with_invalid_leaf_finish = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_doors_leaf_finish]

doors_with_valid_leaf_finish = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_doors_leaf_finish]
door_numbers_with_valid_leaf_finish = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_doors_leaf_finish]
# print(door_numbers_with_valid_leaf_finish)

####################################################################################################################
# Frame Material

mismatch_index_for_doors_frame_material = leaf_frame_material_finishes_type_mismatch_index('Frame_Material', doors_with_valid_functions, 10)
set_index_of_mismatch_doors_frame_material= set(mismatch_index_for_doors_frame_material)
doors_with_invalid_frame_material = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_doors_frame_material]

doors_with_valid_frame_material = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_doors_frame_material]
door_numbers_with_valid_frame_material = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_doors_frame_material]
# print(door_numbers_with_valid_frame_material)

####################################################################################################################
# Frame Finish

mismatch_index_for_doors_frame_finish = leaf_frame_material_finishes_type_mismatch_index('Frame_Face_Finish', doors_with_valid_functions, 11)
set_index_of_mismatch_doors_frame_finish = set(mismatch_index_for_doors_frame_finish)
doors_with_invalid_frame_finish = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_doors_frame_finish]

doors_with_valid_frame_finish = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_doors_frame_finish]
door_numbers_with_valid_frame_finish = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_doors_frame_finish]
# print(door_numbers_with_valid_frame_finish)

###################################################################################################################
###################################################################################################################
# Undercut

test_index_for_doors_undercut = test_for_door_dimensions(doors_with_valid_functions, 'Undercut', 4)
# print(test_index_for_doors_undercut)

set_index_of_mismatch_doors_with_undercut = set(test_index_for_doors_undercut)
doors_with_invalid_undercut = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_doors_with_undercut]

doors_with_valid_undercut = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_doors_with_undercut]
door_numbers_with_valid_undercut = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_doors_with_undercut]

###################################################################################################################
# Grilled Doors

test_for_leaf_elevation_doors = all_elements_with_type_parameter_AsString(doors_with_valid_functions, 'Leaf_Elevation')
# print(test_for_leaf_elevation_doors)

test_for_leaf_elevation_doors_failure = doors_with_family_param_failure(test_for_leaf_elevation_doors, doors_with_valid_functions, door_numbers_with_valid_functions)
# print(test_for_leaf_elevation_doors_failure )

test_for_leaf_elevation_doors_pass = doors_with_family_param_pass(test_for_leaf_elevation_doors, doors_with_valid_functions, door_numbers_with_valid_functions)
# print(test_for_leaf_elevation_doors_pass)

doors_with_leaf_elevation = test_for_leaf_elevation_doors_pass[0]
door_numbers_with_leaf_elevation = test_for_leaf_elevation_doors_pass[1]

filtered_leaf_elevation_values_for_doors = all_elements_with_type_parameter_AsString(doors_with_leaf_elevation, 'Leaf_Elevation')
# print(filtered_leaf_elevation_values_for_doors)

index_of_doors_with_grilled_doors = [ i for i, x in enumerate(filtered_leaf_elevation_values_for_doors ) if x == 'Grill']
doors_with_grills = [e for i, e in enumerate(doors_with_leaf_elevation) if i in index_of_doors_with_grilled_doors]
door_numbers_with_grills = [e for i, e in enumerate(door_numbers_with_leaf_elevation) if i in index_of_doors_with_grilled_doors]

fire_rating_for_doors_with_grills = shared_parameter_values(doors_with_grills, 'Fire_Rating')
index_of_doors_with_fire_rated_grill_doors = [i for i, x in enumerate(fire_rating_for_doors_with_grills) if x != '0']
# print(index_of_doors_with_fire_rated_grill_doors)

doors_with_grills_and_fire_rated = [e for i, e in enumerate(doors_with_grills) if i in index_of_doors_with_fire_rated_grill_doors]
door_numbers_with_grills_and_fire_rated = [e for i, e in enumerate(door_numbers_with_grills) if i in index_of_doors_with_fire_rated_grill_doors]

acoustic_rating_for_doors_with_grills = shared_parameter_values(doors_with_grills, 'STC_Rating')
index_of_doors_with_acoustic_rated_grill_doors = [i for i, x in enumerate(acoustic_rating_for_doors_with_grills) if x != '0']
# print(index_of_doors_with_acoustic_rated_grill_doors)

doors_with_grills_and_acoustic_rated = [e for i, e in enumerate(doors_with_grills) if i in index_of_doors_with_acoustic_rated_grill_doors]
door_numbers_with_grills_and_acoustic_rated = [e for i, e in enumerate(door_numbers_with_grills) if i in index_of_doors_with_acoustic_rated_grill_doors]

####################################################################################################################
# Speciality Items
####################################################################################################################
# Door Leaf Type

mismatch_index_for_doors_leaf_type = leaf_frame_material_finishes_type_mismatch_index('Type Comments', doors_with_valid_functions, 13)
set_index_of_mismatch_door_leaf_type = set(mismatch_index_for_doors_leaf_type)
doors_with_invalid_leaf_type = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_door_leaf_type]

doors_with_valid_leaf_type = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_type]
door_numbers_with_valid_leaf_type = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_type]
# print(door_numbers_with_valid_leaf_type)

####################################################################################################################
# Door Leaf Construction 

mismatch_index_for_doors_leaf_construction = leaf_frame_material_finishes_type_mismatch_index('Construction', doors_with_valid_functions, 14)
set_index_of_mismatch_door_leaf_construction = set(mismatch_index_for_doors_leaf_construction)
doors_with_invalid_leaf_construction = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_door_leaf_construction]

doors_with_valid_leaf_construction = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_construction]
door_numbers_with_valid_leaf_construction = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_door_leaf_construction]
# print(door_numbers_with_valid_leaf_construction )

####################################################################################################################
# Door Frame Elevation

mismatch_index_for_doors_frame_elevation = leaf_frame_material_finishes_type_mismatch_index('Frame_Elevation', doors_with_valid_functions, 15)
set_index_of_mismatch_door_frame_elevation = set(mismatch_index_for_doors_frame_elevation)
doors_with_invalid_frame_elevation = [e for i, e in enumerate(doors_with_valid_functions) if i in set_index_of_mismatch_door_frame_elevation]

doors_with_valid_frame_elevation = [e for i, e in enumerate(doors_with_valid_functions) if i not in set_index_of_mismatch_door_frame_elevation]
door_numbers_with_valid_frame_elevation = [e for i, e in enumerate(door_numbers_with_valid_functions) if i not in set_index_of_mismatch_door_frame_elevation]
# print(door_numbers_with_valid_frame_elevation)


####################################################################################################################
####################################################################################################################
# Door Frame Profile

frame_profile_for_doors_with_index = elem_param_values_test(doors_with_valid_functions, 'Frame_Profile')
# print(frame_profile_for_doors_with_index)

frame_profile_values = frame_profile_for_doors_with_index[0]
index_for_doors_with_frame_profile_assigned = frame_profile_for_doors_with_index[1]
index_for_doors_with_no_frame_profile_assigned = frame_profile_for_doors_with_index[2]

filtered_door_frame_profile_values = [frame_profile_values[i] for i in index_for_doors_with_frame_profile_assigned]
# print(filtered_door_frame_profile_values)

# ####################################################################################################################
# # Doors with no Frame Profile assigned

doors_with_no_frame_profile_assigned = [doors_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]

doors_with_frame_profile = [doors_with_valid_functions[i] for i in index_for_doors_with_frame_profile_assigned]
door_numbers_with_frame_profile = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_frame_profile_assigned]

door_function_for_doors_with_frame_profile = elem_param_values_test(doors_with_frame_profile, "Room_Function")
# print(door_function_for_doors_with_frame_profile)
door_function_values_for_doors_with_frame_profile = door_function_for_doors_with_frame_profile[0]
# print(door_function_values_for_doors_with_frame_profile)
values_from_dict_doors_with_frame_profile = [door_function_dictionary[x][16] for x in door_function_values_for_doors_with_frame_profile]
# print(values_from_dict_doors_with_frame_profile)

# ####################################################################################################################
# # Doors with mismatch Frame Profile assigned

mismatch_index_for_doors_with_frame_profile = mismatch_index_for_door_parameters(values_from_dict_doors_with_frame_profile, filtered_door_frame_profile_values)
# print(mismatch_index_for_doors_with_frame_profile)

set_index_of_mismatch_door_with_frame_profile = set(mismatch_index_for_doors_with_frame_profile)
doors_with_invalid_frame_profile = [e for i, e in enumerate(doors_with_frame_profile) if i in set_index_of_mismatch_door_with_frame_profile]
# print(doors_with_invalid_frame_profile)


####################################################################################################################
####################################################################################################################
# Door Saddle Type

saddle_type_for_doors_with_index = elem_param_values_test(doors_with_valid_functions, 'Saddle Type')
# print(saddle_type_for_doors_with_index)

saddle_type_values = saddle_type_for_doors_with_index[0]
index_for_doors_with_saddle_type_assigned = saddle_type_for_doors_with_index[1]
index_for_doors_with_no_saddle_type_assigned = saddle_type_for_doors_with_index[2]

filtered_door_saddle_type_values = [saddle_type_values[i] for i in index_for_doors_with_saddle_type_assigned]
# print(filtered_door_saddle_type_values)

####################################################################################################################
# Doors with no Saddle Type assigned

doors_with_no_saddle_type_assigned = [doors_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]

doors_with_saddle_type = [doors_with_valid_functions[i] for i in index_for_doors_with_saddle_type_assigned]
door_numbers_with_saddle_type = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_saddle_type_assigned]

door_function_for_doors_with_saddle_type = elem_param_values_test(doors_with_saddle_type, "Room_Function")
# print(door_function_for_doors_with_saddle_type)
door_function_values_for_doors_with_saddle_type = door_function_for_doors_with_saddle_type[0]
# print(door_function_values_for_doors_with_saddle_type)
values_from_dict_doors_with_saddle_type = [door_function_dictionary[x][17] for x in door_function_values_for_doors_with_saddle_type]
# print(values_from_dict_doors_with_saddle_type)

####################################################################################################################
# Doors with mismatch Saddle Type assigned

mismatch_index_for_doors_with_saddle_type = mismatch_index_for_door_parameters(values_from_dict_doors_with_saddle_type, filtered_door_saddle_type_values)
# print(mismatch_index_for_doors_with_saddle_type)

set_index_of_mismatch_door_with_saddle_type = set(mismatch_index_for_doors_with_saddle_type)
doors_with_invalid_saddle_type = [e for i, e in enumerate(doors_with_saddle_type) if i in set_index_of_mismatch_door_with_saddle_type]
# print(doors_with_invalid_saddle_type)

####################################################################################################################

####################################################################################################################
# Generates Output Statement with Door Number, Room Number, Room Name, To Room & From Room in the format 

def output_statement(sample_door_num_with_mismatch, sample_room_num_with_mismatch, sample_room_name_with_mismatch, sample_to_room_with_mismatch, sample_from_room_with_mismatch, sample_door_Selection_with_mismatch):
    sample_test_issues = [zip(sample_door_Selection_with_mismatch, sample_door_num_with_mismatch, sample_room_num_with_mismatch, sample_room_name_with_mismatch, sample_to_room_with_mismatch, sample_from_room_with_mismatch)]
    
    for issues in sample_test_issues:
        out.print_table(table_data = issues, title = 'DOOR CHECKING TABLE', columns = ['Element ID','Door Number', 'Room Number', 'Room Name', 'To Room', 'From Room'], formats = ['','','','','','' ])
        
####################################################################################################################
################### LIST OF ALL DOOR REQUIREMENTS TO VERIFY ########################################################
####################################################################################################################

# All elements of category- UserInput

from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 

userInputcategory = SelectFromList('Select Parameter to Check', ['01.Door Number against Room Number & Room Names', '02.Multiple Doors in Single Room', '03.Function', '04.Leaf Number', '05.Single/Equal/Unequal Leaves', '06.Leaf Width', '07.Leaf Height', '08.Fire Rating of Doors and against Wall Fire Ratings', '09.Acoustic Rating of Doors and against Wall Acoustic Ratings','10.Leaf Material & Finishes', '11.Frame Material & Finishes', '12.Undercut', '13.Fire Rated/Acoustically Treated Door with Grill', '14.Leaf Type', '15.Leaf Construction', '16.Frame Elevation', '17.Frame Profile', '18.Saddle Type'])
userInputcategory = str(userInputcategory)

####################################################################################################################

if userInputcategory == '01.Door Number against Room Number & Room Names':

    out.print_md('**DOOR ROOM NUMBERS CHECK- PRESENT/MISSING**')
    if len(door_numbers_with_missing_door_room_numbers) == 0:
        print('\nDoor Room Numbers are present in the Revit Model for included Doors.')
    else:
        print('\nThe following Doors have missing Door Room Numbers.\nPlease add Room Numbers to the Doors.')
        missing_door_room_numbers_issues = [zip(door_Selections_with_missing_door_room_numbers, door_numbers_with_missing_door_room_numbers)]
        for issues in missing_door_room_numbers_issues:
            out.print_table(table_data = issues, title = 'DOOR CHECKING TABLE', columns = ['Element ID','Door Number'], formats = ['','' ])
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR ROOM NAMES CHECK- PRESENT/MISSING**')
    if len(door_numbers_with_missing_door_room_names) == 0:
        print('\nDoor Room Names are present in Revit for all included Doors.')
        print('\n ')
    else:
        print('\nThe following Doors have missing Door Room Names.\nPlease add Room Names to the Doors. ')
        missing_door_room_names_issues = [zip(door_Selections_with_missing_door_room_names, door_numbers_with_missing_door_room_names)]
        for issues in missing_door_room_names_issues:
            out.print_table(table_data = issues, title = 'DOOR CHECKING TABLE', columns = ['Element ID','Door Number'], formats = ['','' ])
    print('\n ')
    print('*'*216)
    
    #############################################################################################################################################
    
    # Creating list of alphabets to verify
    test_list = []
    alpha = 'a'
    for i in range(0,26):
        test_list.append(alpha)
        alpha = chr(ord(alpha) + 1)
    
    # Getting door numbers with last character as alphabet
    last_alpha = [dnm[-1] for dnm in door_numbers]
    # print(last_alpha)    
    
    # Getting index of Doors with alphabets
    door_index_with_alpha = []
    i = 0
    while (i < len(last_alpha)):
        if (test_list.count(last_alpha[i]) > 0):
            door_index_with_alpha.append(i)
        i += 1
    # print(door_index_with_alpha)
    
    # Get all door num with alphabets
    door_num_with_alpha = [door_numbers[i] for i in door_index_with_alpha]
    
    # Removing last character from every string
    door_num_alpha_remove = [a[:-1] for a in door_num_with_alpha]
    # print(door_num_alpha_remove)
    
    # Replacing door numbers with removed alphabets
    door_num_dict = dict(zip(door_index_with_alpha, door_num_alpha_remove))
    door_num_without_alpha_list = [door_num_dict.get(i,j) for i,j in enumerate(door_numbers)]
    # print(door_num_without_alpha_list)
    
    # Checking Door Numbers against Room Numbers
    
    out.print_md('**DOOR NUMBERS CHECK AGAINST ROOM NUMBERS- MATCH/MISMATCH**')
    if door_num_without_alpha_list == door_room_numbers:
       print('\nDoor Numbers provided for Doors match the Door Room Numbers. ')

    else:
        print('\nDoor Numbers provided for Doors do not match the Door Room Numbers.\n Please find table below to check in Revit Model')
        # Boolean comparision of list of Door numbers against Room numbers
        bool_list_compare = (list(i[0] == i[1] for i in zip(door_room_numbers, door_num_without_alpha_list)))   
        # print(bool_list_compare)
    
        # Index of mismatching Door numbers
        index_of_failure_door_num = [i for i, x in enumerate(bool_list_compare) if not x]
        # print(index_of_failure_door_num)
    
        # List of mismatching doors for user
        door_num_with_mismatch_room_num = [door_numbers[i] for i in index_of_failure_door_num]
        room_num_with_mismatch_door_num = [door_room_numbers[i] for i in index_of_failure_door_num]
        room_name_with_mismatch_door_num = [door_room_names[i] for i in index_of_failure_door_num]
        to_room_name_with_mismatch_door_num = [door_to_room_name_list[i] for i in index_of_failure_door_num]
        from_room_name_with_mismatch_door_num = [door_from_room_name_list[i] for i in index_of_failure_door_num]
        door_Selection_with_mismatch_door_num = [door_Selections[i] for i in index_of_failure_door_num]
        # door_Function_with_mismatch_door_num = 
        # List Output for mismatching Door Numbers aginst Room Numbers
        
        door_num_mismatch_issues = output_statement(door_num_with_mismatch_room_num, room_num_with_mismatch_door_num, room_name_with_mismatch_door_num, to_room_name_with_mismatch_door_num, from_room_name_with_mismatch_door_num, door_Selection_with_mismatch_door_num)
    print('\n ')
    print('*'*216)
 
####################################################################################################################

elif userInputcategory == '02.Multiple Doors in Single Room':

    # Creating list of alphabets to verify
    test_list = []
    alpha = 'a'
    for i in range(0,26):
        test_list.append(alpha)
        alpha = chr(ord(alpha) + 1)
    
    # Getting door numbers with last character as alphabet
    last_alpha = [dnm[-1] for dnm in door_numbers]
    # print(last_alpha)    
    
    # Getting index of Doors with alphabets
    door_index_with_alpha = []
    i = 0
    while (i < len(last_alpha)):
        if (test_list.count(last_alpha[i]) > 0):
            door_index_with_alpha.append(i)
        i += 1
    # print(door_index_with_alpha)  

    # Get all door num with alphabets
    door_num_with_alpha = [door_numbers[i] for i in door_index_with_alpha]
    
    # Removing last character from every string
    door_num_alpha_remove = [a[:-1] for a in door_num_with_alpha]
    # print(door_num_alpha_remove)
       
    # Replacing door numbers with removed alphabets
    door_num_dict = dict(zip(door_index_with_alpha, door_num_alpha_remove))
    door_num_without_alpha_list = [door_num_dict.get(i,j) for i,j in enumerate(door_numbers)]
    # print(door_num_without_alpha_list)
    
    # Creating Self Door Number Dictionary with index number
    door_num_dict = {}
    index = 0
    for item in door_num_without_alpha_list:
        if item in door_num_dict:
            door_num_dict[item] += [index]
            index += 1
        else:
            door_num_dict[item] = [index]
            index += 1
    # print(door_num_dict)
    
    # Creating Door number dicitionary to count occurences
    dict_door_num_with_occurences = {k:v for (k,v) in door_num_dict.items() if (len(v)>1)}
    door_num_with_occurences = list(dict_door_num_with_occurences.keys())
    # print(door_num_with_occurences)
    door_num_occurences = list(dict_door_num_with_occurences.values())
    # print(door_num_occurences)
    # print(dict_door_num_with_occurences)
    
    # Length of nested lists of occurences
    length_of_nested_door_occurences = [len(x) for x in door_num_occurences]
    # print(length_of_nested_door_occurences)
    
    # Flattened list of occurences index
    door_num_occurences_unnested = [item for sublist in door_num_occurences for item in sublist]
    # print(door_num_occurences_unnested)

    #  Getting item at index from Door Number List
    door_num_from_main_list = [door_numbers[i] for i in door_num_occurences_unnested]
    # print(door_num_from_main_list)
    
    # Nesting Door Number Values for checking
    door_num_from_main_list_iter = iter(door_num_from_main_list)
    door_num_nested = [list(islice(door_num_from_main_list_iter, elem)) for elem in length_of_nested_door_occurences]
    # print(door_num_nested)
    
    # Acquiring last characted of nested item in list
    last_alpha_nested = []
    for list in door_num_nested:
        temp = []
        temp = [element[-1] for element in list]
        last_alpha_nested.append(temp)
    # print(last_alpha_nested)
    
    # Sorting last characted of nested item in list(a,b,c..)   
    test_for_inconsistent_door_numbers = []
    for list in last_alpha_nested:
        temp = []
        temp = sorted(list)
        test_for_inconsistent_door_numbers.append(temp)
    # print(test_for_inconsistent_door_numbers)
    
    # Combining list of characters to string(abc,def,ghi,....)
    combine_chars_to_string = []
    for list in test_for_inconsistent_door_numbers:
        def convert(s):
            str1 = ""
            return(str1.join(s))
        temp = []
        temp = convert(list)
        combine_chars_to_string.append(temp)
    # print(combine_chars_to_string)
    
    # Function to check continuity of string combined in list
    def check_continuity_of_string(s):
        l = len(s)
        s = ''.join(sorted(s))
        for i in range(1,l):
            if ord(s[i]) -ord(s[i-1]) != 1:
                return False
        return True
    
    string_continuity_bool = []
    for str in combine_chars_to_string:
        if __name__ == "__main__":
            temp = []
            if check_continuity_of_string(str):
                temp = True
            else:
                temp = False
            string_continuity_bool.append(temp)
    # print(string_continuity_bool)
    
    # Index of Multiple Doors in Rooms with issues
    index_of_failure_door_room_num = [i for i, x in enumerate(string_continuity_bool) if not x]
    # print(index_of_failure_door_roon_num)
    
    # List of mismatching doors for user
    identify_room_num_from_door_with_multiple_doors_issues = [door_num_with_occurences[i] for i in index_of_failure_door_room_num]
    index_of_room_nums_with_issues = [i for i, x in enumerate(room_numbers) if x in identify_room_num_from_door_with_multiple_doors_issues]
    rooms_nums_with_multiple_door_issues = [room_numbers[i] for i in index_of_room_nums_with_issues]
    rooms_with_multiple_door_issues = [rooms[i] for i in index_of_room_nums_with_issues]
    room_Select_with_multiple_door_issues = [room_Selections[i] for i in index_of_room_nums_with_issues]
    
    len_of_multi_door_issues_list = len(identify_room_num_from_door_with_multiple_doors_issues )
    
    output_for_multiple_door_issues = [zip(room_Select_with_multiple_door_issues, identify_room_num_from_door_with_multiple_doors_issues)] 
    out.print_md('**DOOR NUMBERING SEQUENCE CHECK- ISSUES/NO ISSUES**')
    if (len_of_multi_door_issues_list == 0):
        print("\nDoor Number sequencing for the Rooms in Model have no issues")
    else:
        print("\nDoor Number sequencing for the following Rooms have issues.\n Please find below Room numbers assigned to Doors below to check in Revit Model.")
        for issues in output_for_multiple_door_issues:
            out.print_table(table_data = issues, title = 'DOOR CHECKING TABLE', columns = ['Element ID','Room Number'], formats = ['','' ])

####################################################################################################################

elif userInputcategory == '03.Function':
    out.print_md('**DOOR ROOM FUNCTIONS CHECK- ASSIGNED/NOT ASSIGNED**')
    if len(doors_with_no_functions_assigned) == 0:
        print("\nDoor Functions are assigned to all Doors")

    else:
        print("\nDoor Functions are not assigned for the following doors.")
        door_nums_with_no_functions_assigned = [door_numbers[i] for i in index_for_doors_with_no_functions_assigned]
        door_room_numbers_with_no_function_assigned = [door_room_numbers[i] for i in index_for_doors_with_no_functions_assigned]
        door_room_names_with_no_function_assigned = [door_room_names[i] for i in index_for_doors_with_no_functions_assigned]
        door_to_room_names_with_no_function_assigned = [door_to_room_name_list[i] for i in index_for_doors_with_no_functions_assigned]
        doors_from_room_names_with_no_function_assigned = [door_from_room_name_list[i] for i in index_for_doors_with_no_functions_assigned]
        door_Selections_with_no_function_assigned = [door_Selections[i] for i in index_for_doors_with_no_functions_assigned]
        # List of Doors with missing Functions
        door_functions_missing = output_statement(door_nums_with_no_functions_assigned, door_room_numbers_with_no_function_assigned, door_room_names_with_no_function_assigned, door_to_room_names_with_no_function_assigned, doors_from_room_names_with_no_function_assigned, door_Selections_with_no_function_assigned )
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR ROOM FUNCTIONS CHECK- VALID/NOT VALID**')    
    if len(doors_with_invalid_functions) == 0:
        print("\nDoor Functions assigned to doors are valid")
    else:
        print('\nDoor Functions are assigned to the doors but are invalid.\nPlease verify the Functions for the Doors in the table below, against the Door Template for the project. ')
        door_numbers_with_invalid_functions = [door_numbers_with_functions[i] for i in index_of_invalid_door_functions]
        door_room_numbers_with_invalid_functions = [door_room_numbers_with_functions[i] for i in index_of_invalid_door_functions]
        door_room_names_with_invalid_functions = [door_room_names_with_functions[i] for i in index_of_invalid_door_functions]
        door_to_room_names_with_invalid_functions = [door_to_room_names_with_functions[i] for i in index_of_invalid_door_functions]
        door_from_room_names_with_invalid_functions = [door_from_room_names_with_functions[i] for i in index_of_invalid_door_functions]
        door_Selections_with_invalid_functions = [door_Selections[i] for i in index_of_invalid_door_functions]
        
        # List of Doors with invalid Functions
        door_functions_invalid = output_statement(door_numbers_with_invalid_functions,door_room_numbers_with_invalid_functions, door_room_names_with_invalid_functions, door_to_room_names_with_invalid_functions, door_from_room_names_with_invalid_functions,door_Selections_with_invalid_functions)
    print('\n ')
    print('*'*216)
    
####################################################################################################################

elif userInputcategory == '04.Leaf Number':
    out.print_md('**DOOR LEAF NUMBER CHECK- ASSIGNED/NOT ASSIGNED**')
    filter_doors_with_leaf_number_param_fail = doors_with_family_param_failure(test_for_doors_with_leaves, doors_with_valid_functions,door_numbers_with_valid_functions)
    # print(filter_doors_with_leaf_number_param_pass)
    filtered_doors_leaf_test_fail = filter_doors_with_leaf_number_param_fail[0]
    # print(filtered_doors_leaf_test_fail)
    filtered_door_nums_leaf_test_fail = filter_doors_with_leaf_number_param_fail[1]
    # print(filtered_door_nums_leaf_test_fail)
    if len(filtered_door_nums_leaf_test_fail) == 0:
        print("\nDoors having valid Room Functions, have Leaf Numbers assigned to them. ")
    else:
        print("\nDoors having valid Room Functions, have Leaf Numbers unassigned to them. ")
    print('\n ')   
    print('*'*216)  
    
    out.print_md('**DOOR LEAF NUMBER CHECK- VALID/INVALID**')   
    if len(mismatch_index_for_door_leaf_number) == 0:
        print("\nDoors having valid Room Functions, have valid Leaf numbers. ")
    else:
        print("\nDoors have valid Room functions, but have invalid Leaf numbers.\nPlease verify the Leaf Number for the Doors in the table below, against the Door Template for the project.")
        doors_with_mismatch_leaf_number = [doors_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_numbers_with_mismatch_leaf_number = [door_numbers_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_room_numbers_with_mismatch_leaf_number = [door_room_numbers_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_room_names_with_mismatch_leaf_number = [door_room_names_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_to_room_names_with_mismatch_leaf_number = [door_to_room_names_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_from_room_names_with_mismatch_leaf_number = [door_from_room_names_with_valid_functions[i] for i in mismatch_index_for_door_leaf_number]
        door_Selections_with_mismatch_leaf_number = [door_Selections[i] for i in mismatch_index_for_door_leaf_number]
        
        door_leaf_number_mismatch = output_statement(door_numbers_with_mismatch_leaf_number, door_room_numbers_with_mismatch_leaf_number, door_room_names_with_mismatch_leaf_number, door_to_room_names_with_mismatch_leaf_number, door_from_room_names_with_mismatch_leaf_number, door_Selections_with_mismatch_leaf_number)
    print('\n ') 
    print('*'*216)
    
####################################################################################################################

elif userInputcategory == '05.Single/Equal/Unequal Leaves':
    
    # Double Unequal leaves Failure
    out.print_md('**DOUBLE DOOR UNEQUAL LEAVES CHECK- VALID/INVALID**')
    if len(mismatch_index_for_door_with_unequal_leaves) == 0:
        print('\nDoors with Unequal Leaves have valid (Equal/Unequal Parameter) values assigned as -"FALSE".')
    else:
        print('\nDoors with Unequal Leaves have invalid (Equal/Unequal Parameter) values assigned as - "TRUE".\nPlease verify the Equal/Unequal Leaves parameter for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_unequal_leaves_invalid =  [ e for i, e in enumerate(double_doors_with_unequal_leaves) if i in set_index_of_mismatch_door_with_unequal_leaves]
        filter_door_numbers_with_unequal_leaves_invalid = [ e for i, e in enumerate(double_door_numbers_with_unequal_leaves) if i in set_index_of_mismatch_door_with_unequal_leaves]
        filter_door_room_numbers_with_unequal_leaves_invalid = shared_parameter_values(filter_doors_with_unequal_leaves_invalid, 'Room_Number')
        filter_door_room_names_with_unequal_leaves_invalid = shared_parameter_values(filter_doors_with_unequal_leaves_invalid,'Room_Name')
        filter_door_to_from_room_names_with_unequal_leaves_invalid = troom_froom_name_for_doors(filter_doors_with_unequal_leaves_invalid)
        filter_door_to_room_names_with_unequal_leaves_invalid = filter_door_to_from_room_names_with_unequal_leaves_invalid[0]
        filter_door_from_room_names_with_unequal_leaves_invalid = filter_door_to_from_room_names_with_unequal_leaves_invalid[1]
        filter_door_Selections_with_unequal_leaves_invalid = [out.linkify(door.Id) for door in filter_doors_with_unequal_leaves_invalid]
        
             
        double_door_unequal_mismatch = output_statement(filter_door_numbers_with_unequal_leaves_invalid, filter_door_room_numbers_with_unequal_leaves_invalid, filter_door_room_names_with_unequal_leaves_invalid, filter_door_to_room_names_with_unequal_leaves_invalid, filter_door_from_room_names_with_unequal_leaves_invalid, filter_door_Selections_with_unequal_leaves_invalid )
    print('\n ')
    print('*'*216)
        
    # Double Equal Leaves Failure
    out.print_md('**DOUBLE DOOR EQUAL LEAVES CHECK- VALID/INVALID**')
    if len(mismatch_index_for_door_with_equal_leaves) == 0:
        print('\nDoors with Double Equal Leaves have valid (Equal/Unequal Parameter) values as- "TRUE". ')
    else:
        print('\nDoors with Double Equal Leaves have invalid (Equal/Unequal Parameter) values assigned as - "FALSE".\nPlease verify the Equal/Unequal Leaves parameter for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_equal_leaves_invalid =  [ e for i, e in enumerate(double_doors_with_equal_leaves) if i in set_index_of_mismatch_door_with_equal_leaves]
        filter_door_numbers_with_equal_leaves_invalid = [ e for i, e in enumerate(double_door_numbers_with_equal_leaves) if i in set_index_of_mismatch_door_with_equal_leaves]
        filter_door_room_numbers_with_equal_leaves_invalid = shared_parameter_values(filter_doors_with_equal_leaves_invalid, 'Room_Number')
        filter_door_room_names_with_equal_leaves_invalid = shared_parameter_values(filter_doors_with_equal_leaves_invalid,'Room_Name')
        filter_door_to_from_room_names_with_equal_leaves_invalid = troom_froom_name_for_doors(filter_doors_with_equal_leaves_invalid)
        filter_door_to_room_names_with_equal_leaves_invalid = filter_door_to_from_room_names_with_equal_leaves_invalid[0]
        filter_door_from_room_names_with_equal_leaves_invalid = filter_door_to_from_room_names_with_equal_leaves_invalid[1]
        filter_door_Selections_with_equal_leaves_invalid = [out.linkify(door.Id) for door in filter_doors_with_equal_leaves_invalid]
        
        double_door_equal_mismatch = output_statement(filter_door_numbers_with_equal_leaves_invalid, filter_door_room_numbers_with_equal_leaves_invalid, filter_door_room_names_with_equal_leaves_invalid, filter_door_to_room_names_with_equal_leaves_invalid, filter_door_from_room_names_with_equal_leaves_invalid, filter_door_Selections_with_equal_leaves_invalid )
    print('\n ')
    print('*'*216)
        
    # Single Equal Leaves Failure
    out.print_md('**SINGLE DOOR LEAF CHECK- VALID/INVALID**')
    if len(mismatch_index_for_door_with_single_equal_unequal_leaf) == 0:
        print('\nDoors with Single Leaf have valid (Equal/Unequal Parameter) values as- "TRUE". ')
    else:
        print('\nDoors with Single Leaf have invalid (Equal/Unequal Parameter) values assigned as - "FALSE".\nPlease verify the Equal/Unequal Leaves parameter for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_single_leaf_invalid = [ e for i, e in enumerate(doors_with_single_leaf) if i in set_index_of_mismatch_door_with_single_equal_unequal_leaf]
        filter_door_numbers_with_single_leaf_invalid = [ e for i, e in enumerate(door_numbers_with_single_leaf) if i in set_index_of_mismatch_door_with_single_equal_unequal_leaf]
        filter_door_room_numbers_with_single_leaf_invalid = shared_parameter_values(filter_doors_with_single_leaf_invalid, 'Room_Number')
        filter_door_room_names_with_single_leaf_invalid = shared_parameter_values(filter_doors_with_single_leaf_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_single_leaf_invalid = troom_froom_name_for_doors(filter_doors_with_single_leaf_invalid)
        filter_door_to_room_names_with_single_leaf_invalid = filter_door_to_from_room_names_with_single_leaf_invalid[0]
        filter_door_from_room_names_with_single_leaf_invalid = filter_door_to_from_room_names_with_single_leaf_invalid[1]        
        filter_door_Selections_with_single_leaf_invalid = [out.linkify(door.Id) for door in filter_doors_with_single_leaf_invalid]
    
        single_door_equal_mismatch = output_statement(filter_door_numbers_with_single_leaf_invalid, filter_door_room_numbers_with_single_leaf_invalid, filter_door_room_names_with_single_leaf_invalid, filter_door_to_room_names_with_single_leaf_invalid, filter_door_from_room_names_with_single_leaf_invalid, filter_door_Selections_with_single_leaf_invalid )
    print('\n ')
    print('*'*216)    
                
####################################################################################################################

elif userInputcategory == '06.Leaf Width':
    
    # Single Door Widths
    out.print_md('**SINGLE DOOR LEAF WIDTH CHECK- VALID/INVALID**')
    if len(test_index_for_single_doors_width ) == 0:
        print('\nLeaf Width for Single Leaf Doors match the Design Requirements.')
    else:
        print('\nLeaf Widths for Single Leaf Doors do not match the Design Requirements.\nPlease verify the Leaf Width for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_single_leaf_width_invalid = [e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i in set_index_of_mismatch_doors_with_single_leaf_width]
        filter_door_numbers_with_single_leaf_width_invalid = [e for i, e in enumerate(door_numbers_with_valid_single_equal_leaf) if i in set_index_of_mismatch_doors_with_single_leaf_width]
        filter_door_room_numbers_with_single_leaf_width_invalid = shared_parameter_values(filter_doors_with_single_leaf_width_invalid, 'Room_Number')
        filter_door_room_names_with_single_leaf_width_invalid = shared_parameter_values(filter_doors_with_single_leaf_width_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_single_leaf_width_invalid = troom_froom_name_for_doors(filter_doors_with_single_leaf_width_invalid)
        filter_door_to_room_names_with_single_leaf_width_invalid = filter_door_to_from_room_names_with_single_leaf_width_invalid[0]
        filter_door_from_room_names_with_single_leaf_width_invalid = filter_door_to_from_room_names_with_single_leaf_width_invalid[1]
        filter_door_Selections_with_single_leaf_width_invalid = [out.linkify(door.Id) for door in filter_doors_with_single_leaf_width_invalid]
        
        single_doors_leaf_width_invalid = output_statement(filter_door_numbers_with_single_leaf_width_invalid ,filter_door_room_numbers_with_single_leaf_width_invalid, filter_door_room_names_with_single_leaf_width_invalid, filter_door_to_room_names_with_single_leaf_width_invalid, filter_door_from_room_names_with_single_leaf_width_invalid, filter_door_Selections_with_single_leaf_width_invalid )
    print('\n ')
    print('*'*216)
    
    # Double Door Widths
    out.print_md('**DOUBLE EQUAL LEAVES DOOR LEAF WIDTH CHECK- VALID/INVALID**')
    if len(test_index_for_double_equal_doors_width) == 0:
        print('\nLeaf Width for Double Equal Leaves Doors match the Design Requirements.')
    else:
        print('\nLeaf Widths for Double Equal Leaves Doors do not match the Design Requirements.\nPlease verify the Leaf Width for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_double_equal_leaves_width_invalid = [e for i, e in enumerate(doors_with_valid_equal_leaves) if i in set_index_of_mismatch_doors_with_double_equal_leaves_width]
        filter_door_numbers_with_double_equal_leaves_width_invalid = [e for i, e in enumerate(door_numbers_with_valid_equal_leaves) if i in set_index_of_mismatch_doors_with_double_equal_leaves_width]
        filter_door_room_numbers_with_double_equal_leaves_width_invalid = shared_parameter_values(filter_doors_with_double_equal_leaves_width_invalid, 'Room_Number')
        filter_door_room_names_with_double_equal_leaves_width_invalid = shared_parameter_values(filter_doors_with_double_equal_leaves_width_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_double_equal_leaves_width_invalid = troom_froom_name_for_doors(filter_doors_with_double_equal_leaves_width_invalid)
        filter_door_to_room_names_with_double_equal_leaves_width_invalid = filter_door_to_from_room_names_with_double_equal_leaves_width_invalid[0]
        filter_door_from_room_names_with_double_equal_leaves_width_invalid = filter_door_to_from_room_names_with_double_equal_leaves_width_invalid[1]
        filter_door_Selections_with_double_equal_leaves_width_invalid = [out.linkify(door.Id) for door in filter_doors_with_double_equal_leaves_width_invalid]
     
        double_equal_leaves_door_width_invalid =  output_statement(filter_door_numbers_with_double_equal_leaves_width_invalid ,filter_door_room_numbers_with_double_equal_leaves_width_invalid, filter_door_room_names_with_double_equal_leaves_width_invalid, filter_door_to_room_names_with_double_equal_leaves_width_invalid, filter_door_from_room_names_with_double_equal_leaves_width_invalid, filter_door_Selections_with_double_equal_leaves_width_invalid )
    print('\n ') 
    print('*'*216)
     
    # Double Door Unequal - Main Panel Widths
    out.print_md('**DOUBLE UNEQUAL LEAVES DOOR MAIN PANEL LEAF WIDTH CHECK- VALID/INVALID**')    
    if len(test_index_for_double_unequal_doors_main_panel_width) == 0:
        print('\nMain Panel Leaf Width for Double Unequal Leaf Doors match the Design Requirements.')
    else:
        print('\nMain Panel Leaf Widths for Double Unequal Leaf Doors do not match the Design Requirements.\nPlease verify the Main Panel Width for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_unequal_leaves_main_panel_width_invalid = [e for i, e in enumerate(doors_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_unequal_main_panel_width]
        filter_door_numbers_with_unequal_leaves_main_panel_width_invalid = [e for i, e in enumerate(door_numbers_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_unequal_main_panel_width]
        filter_door_room_numbers_with_unequal_leaves_main_panel_width_invalid= shared_parameter_values(filter_doors_with_unequal_leaves_main_panel_width_invalid, 'Room_Number')
        filter_door_room_names_with_unequal_leaves_main_panel_width_invalid = shared_parameter_values(filter_doors_with_unequal_leaves_main_panel_width_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_unequal_leaves_main_panel_width_invalid = troom_froom_name_for_doors(filter_doors_with_unequal_leaves_main_panel_width_invalid)
        filter_door_to_room_names_with_unequal_leaves_main_panel_width_invalid = filter_door_to_from_room_names_with_unequal_leaves_main_panel_width_invalid[0]
        filter_door_from_room_names_with_unequal_leaves_main_panel_width_invalid = filter_door_to_from_room_names_with_unequal_leaves_main_panel_width_invalid[1]
        filter_door_Selections_with_unequal_leaves_main_panel_widths_invalid = [out.linkify(door.Id) for door in filter_doors_with_unequal_leaves_main_panel_width_invalid]
        
        unequal_doors_main_width_invalid = output_statement(filter_door_numbers_with_unequal_leaves_main_panel_width_invalid ,filter_door_room_numbers_with_unequal_leaves_main_panel_width_invalid, filter_door_room_names_with_unequal_leaves_main_panel_width_invalid, filter_door_to_room_names_with_unequal_leaves_main_panel_width_invalid, filter_door_from_room_names_with_unequal_leaves_main_panel_width_invalid, filter_door_Selections_with_unequal_leaves_main_panel_widths_invalid )
    print('\n ')
    print('*'*216)
    
    # Double Door Unequal - Side Panel Widths
    out.print_md('**DOUBLE UNEQUAL LEAVES DOOR SIDE PANEL LEAF WIDTH CHECK- VALID/INVALID**')      
    if len(test_index_for_double_unequal_doors_side_panel_width) == 0:
        print('\nSide Panel Leaf Width for Double Unequal Leaf Doors match the Design Requirements.')
    else:
        print('\nSide Panel Leaf Widths for Double Unequal Leaf Doors do not match the Design Requirements.\nPlease verify the Main Panel Width for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_unequal_leaves_side_panel_width_invalid = [e for i, e in enumerate(doors_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_unequal_side_panel_width]
        filter_door_numbers_with_unequal_leaves_side_panel_width_invalid = [e for i, e in enumerate(door_numbers_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_unequal_side_panel_width]
        filter_door_room_numbers_with_unequal_leaves_side_panel_width_invalid= shared_parameter_values(filter_doors_with_unequal_leaves_side_panel_width_invalid, 'Room_Number')
        filter_door_room_names_with_unequal_leaves_side_panel_width_invalid = shared_parameter_values(filter_doors_with_unequal_leaves_side_panel_width_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_unequal_leaves_side_panel_width_invalid = troom_froom_name_for_doors(filter_doors_with_unequal_leaves_side_panel_width_invalid)
        filter_door_to_room_names_with_unequal_leaves_side_panel_width_invalid = filter_door_to_from_room_names_with_unequal_leaves_side_panel_width_invalid[0]
        filter_door_from_room_names_with_unequal_leaves_side_panel_width_invalid = filter_door_to_from_room_names_with_unequal_leaves_side_panel_width_invalid[1]
        filter_door_Selections_with_unequal_leaves_side_panel_widths_invalid = [out.linkify(door.Id) for door in filter_doors_with_unequal_leaves_side_panel_width_invalid]
        
        unequal_doors_side_width_invalid = output_statement(filter_door_numbers_with_unequal_leaves_side_panel_width_invalid ,filter_door_room_numbers_with_unequal_leaves_side_panel_width_invalid, filter_door_room_names_with_unequal_leaves_main_panel_width_invalid, filter_door_to_room_names_with_unequal_leaves_side_panel_width_invalid, filter_door_from_room_names_with_unequal_leaves_side_panel_width_invalid, filter_door_Selections_with_unequal_leaves_side_panel_widths_invalid  )
    print('\n ')
    print('*'*216)

####################################################################################################################

elif userInputcategory == '07.Leaf Height':
       
    # Single Door Heights
    out.print_md('**SINGLE DOOR LEAF HEIGHT CHECK- VALID/INVALID**')   
    if len(test_index_for_single_doors_height) == 0:
        print('\nLeaf Height for Single Leaf Doors match the Design Requirements.')
    else:
        print('\nLeaf Height for Single Leaf Doors do not match the Design Requirements.\nPlease verify the Leaf Height for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_single_leaf_height_invalid = [e for i, e in enumerate(doors_with_valid_single_equal_leaf) if i in set_index_of_mismatch_doors_with_single_leaf_height]
        filter_door_numbers_with_single_leaf_height_invalid = [e for i, e in enumerate(door_numbers_with_valid_single_equal_leaf) if i in set_index_of_mismatch_doors_with_single_leaf_height]
        filter_door_room_numbers_with_single_leaf_height_invalid = shared_parameter_values(filter_doors_with_single_leaf_height_invalid, 'Room_Number')
        filter_door_room_names_with_single_leaf_height_invalid = shared_parameter_values(filter_doors_with_single_leaf_height_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_single_leaf_height_invalid = troom_froom_name_for_doors(filter_doors_with_single_leaf_height_invalid)
        filter_door_to_room_names_with_single_leaf_height_invalid = filter_door_to_from_room_names_with_single_leaf_height_invalid[0]
        filter_door_from_room_names_with_single_leaf_height_invalid = filter_door_to_from_room_names_with_single_leaf_height_invalid[1]
        filter_door_Selections_with_single_leaf_height_invalid = [out.linkify(door.Id) for door in filter_doors_with_single_leaf_height_invalid]
     
        single_doors_leaf_height_invalid = output_statement(filter_door_numbers_with_single_leaf_height_invalid ,filter_door_room_numbers_with_single_leaf_height_invalid, filter_door_room_names_with_single_leaf_height_invalid, filter_door_to_room_names_with_single_leaf_height_invalid, filter_door_from_room_names_with_single_leaf_height_invalid, filter_door_Selections_with_single_leaf_height_invalid  )
    print('\n ')
    print('*'*216)
    
    # Double Equal Leaf Door Heights
    out.print_md('**DOUBLE EQUAL LEAVES DOOR LEAF HEIGHT CHECK- VALID/INVALID**')  
    if len(test_index_for_double_equal_doors_height) == 0:
        print('\nLeaf Height for Double Equal Leaf Doors match the Design Requirements.')
    else:
        print('\nLeaf Height for Double Equal Leaf Doors do not match the Design Requirements.\nPlease verify the Leaf Height for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_double_equal_leaves_height_invalid = [e for i, e in enumerate(doors_with_valid_equal_leaves) if i in set_index_of_mismatch_doors_with_double_equal_leaves_height]
        filter_door_numbers_with_double_equal_leaves_height_invalid = [e for i, e in enumerate(door_numbers_with_valid_equal_leaves) if i in set_index_of_mismatch_doors_with_double_equal_leaves_height]
        filter_door_room_numbers_with_double_equal_leaves_height_invalid = shared_parameter_values(filter_doors_with_double_equal_leaves_height_invalid, 'Room_Number')
        filter_door_room_names_with_double_equal_leaves_height_invalid = shared_parameter_values(filter_doors_with_double_equal_leaves_height_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_double_equal_leaves_height_invalid = troom_froom_name_for_doors(filter_doors_with_double_equal_leaves_height_invalid)
        filter_door_to_room_names_with_double_equal_leaves_height_invalid = filter_door_to_from_room_names_with_double_equal_leaves_height_invalid[0]
        filter_door_from_room_names_with_double_equal_leaves_height_invalid = filter_door_to_from_room_names_with_double_equal_leaves_height_invalid[1]
        filter_door_Selections_with_double_equal_leaves_height_invalid = [out.linkify(door.Id) for door in filter_doors_with_double_equal_leaves_height_invalid ]
     
        double_equal_leaves_door_height_invalid =  output_statement(filter_door_numbers_with_double_equal_leaves_height_invalid ,filter_door_room_numbers_with_double_equal_leaves_height_invalid, filter_door_room_names_with_double_equal_leaves_height_invalid, filter_door_to_room_names_with_double_equal_leaves_height_invalid, filter_door_from_room_names_with_double_equal_leaves_height_invalid, filter_door_Selections_with_double_equal_leaves_height_invalid )
    print('\n ') 
    print('*'*216)

    # Double Unequal Leaf Door Heights
    out.print_md('**DOUBLE UNEQUAL LEAVES DOOR LEAF HEIGHT CHECK- VALID/INVALID**')  
    if len(test_index_for_double_unequal_doors_height) == 0:
        print('\nLeaf Height for Double Unqual Leaf Doors match the Design Requirements.')
    else:
        print('\nLeaf Height for Double Unequal Leaf Doors do not match the Design Requirements.\nPlease verify the Leaf Height for the Doors in the table below, against the Door Template for the project.')
        filter_doors_with_double_unequal_leaves_height_invalid = [e for i, e in enumerate(doors_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_double_unequal_leaves_height]
        filter_door_numbers_with_double_unequal_leaves_height_invalid = [e for i, e in enumerate(door_numbers_with_valid_unequal_leaves) if i in set_index_of_mismatch_doors_with_double_unequal_leaves_height]
        filter_door_room_numbers_with_double_unequal_leaves_height_invalid = shared_parameter_values(filter_doors_with_double_unequal_leaves_height_invalid, 'Room_Number')
        filter_door_room_names_with_double_unequal_leaves_height_invalid = shared_parameter_values(filter_doors_with_double_unequal_leaves_height_invalid, 'Room_Name')
        filter_door_to_from_room_names_with_double_unequal_leaves_height_invalid = troom_froom_name_for_doors(filter_doors_with_double_unequal_leaves_height_invalid)
        filter_door_to_room_names_with_double_unequal_leaves_height_invalid = filter_door_to_from_room_names_with_double_unequal_leaves_height_invalid[0]
        filter_door_from_room_names_with_double_unequal_leaves_height_invalid = filter_door_to_from_room_names_with_double_unequal_leaves_height_invalid[1]
        filter_door_Selections_with_double_unequal_leaves_height_invalid = [out.linkify(door.Id) for door in filter_doors_with_double_unequal_leaves_height_invalid]
     
        double_unequal_leaves_door_height_invalid =  output_statement(filter_door_numbers_with_double_unequal_leaves_height_invalid ,filter_door_room_numbers_with_double_unequal_leaves_height_invalid, filter_door_room_names_with_double_unequal_leaves_height_invalid, filter_door_to_room_names_with_double_unequal_leaves_height_invalid, filter_door_from_room_names_with_double_unequal_leaves_height_invalid, filter_door_Selections_with_double_unequal_leaves_height_invalid )
    print('\n ')
    print('*'*216)

####################################################################################################################

elif userInputcategory == '08.Fire Rating of Doors and against Wall Fire Ratings':
    out.print_md('**DOOR FIRE RATING CHECK- ASSIGNED/NOT ASSIGNED**')  
    if len(doors_with_no_fire_rating_assigned) == 0:
        print('\nFire Rating has been assigned to all Doors. ')
    else:
        print('\nFire Rating for the following Doors have not been assigned.\nPlease add "0" in case of Doors with no Fire Rating, for the Doors in the table below. ')
        door_numbers_with_no_fire_rating_assigned = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]
        door_room_numbers_with_no_fire_rating_assigned = [door_room_numbers_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]
        door_room_names_with_no_fire_rating_assigned = [door_room_names_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]
        door_to_room_names_with_no_fire_rating_assigned = [door_to_room_names_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]
        door_from_room_names_with_no_fire_rating_assigned = [door_from_room_names_with_valid_functions[i] for i in index_for_doors_with_no_fire_rating_assigned]
        door_Selections_with_no_fire_rating_assigned = [out.linkify(door.Id) for door in doors_with_no_fire_rating_assigned]
        
        doors_with_no_fire_rating_assigned = output_statement(door_numbers_with_no_fire_rating_assigned, door_room_numbers_with_no_fire_rating_assigned, door_room_names_with_no_fire_rating_assigned, door_to_room_names_with_no_fire_rating_assigned, door_from_room_names_with_no_fire_rating_assigned, door_Selections_with_no_fire_rating_assigned)    
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR FIRE RATING CHECK- VALID/INVALID**')  
    if len(doors_with_invalid_fire_rating) == 0:
        print("\nFire Rating assigned to the Doors are valid and as per Design Requirements.")
    else:
        print('\nFire Rating assigned to the Doors do not match the Design Requirements.\nPlease verify the Fire Rating for the Doors in the table below, against the Door Template for the project.')
        door_numbers_with_invalid_fire_rating = [e for i, e in enumerate(door_numbers_with_fire_rating) if i in set_index_of_mismatch_door_with_fire_rating]
        door_room_numbers_with_invalid_fire_rating = shared_parameter_values(doors_with_invalid_fire_rating, 'Room_Number')
        door_room_names_with_invalid_fire_rating = shared_parameter_values(doors_with_invalid_fire_rating, 'Room_Name')
        door_to_from_room_names_with_invalid_fire_rating = troom_froom_name_for_doors(doors_with_invalid_fire_rating)
        door_to_room_names_with_invalid_fire_rating = door_to_from_room_names_with_invalid_fire_rating[0]
        door_from_room_names_with_invalid_fire_rating = door_to_from_room_names_with_invalid_fire_rating[1]
        door_Selections_with_invalid_fire_rating = [out.linkify(door.Id) for door in doors_with_invalid_fire_rating]
        
        doors_with_invalid_fire_rating_assigned = output_statement(door_numbers_with_invalid_fire_rating, door_room_numbers_with_invalid_fire_rating, door_room_names_with_invalid_fire_rating, door_to_room_names_with_invalid_fire_rating, door_from_room_names_with_invalid_fire_rating, door_Selections_with_invalid_fire_rating)
    print('\n ')
    print('*'*216)
    
    out.print_md('**WALL FIRE RATING,FOR DOORS WITH FIRE RATING CHECK- ASSIGNED/NOT ASSIGNED**')  
    if len(index_of_fire_rated_doors_with_no_wall_fire_rating) == 0:
        print("\nFire Rating has been assigned to all Walls, for Doors with Fire Rating. ")
    else:
        print('\nFire Rating has not been assigned to Walls, for Doors with Fire Rating.\nPlease add Fire Rating to the Walls, on which the following Doors are hosted.\nIn case of Doors with "0" Fire Rating. Please add "0" for the Wall Fire Rating.')

        door_numbers_with_fire_rating_but_no_wall_fire_rating  = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in doors_with_fire_rating_but_no_wall_fire_rating]
        door_room_numbers_with_fire_rating_but_no_wall_fire_rating = shared_parameter_values(doors_with_fire_rating_but_no_wall_fire_rating, 'Room_Number')
        door_room_names_with_fire_rating_but_no_wall_fire_rating = shared_parameter_values(doors_with_fire_rating_but_no_wall_fire_rating, 'Room_Name')
        door_to_from_room_names_with_fire_rating_but_no_wall_fire_rating = troom_froom_name_for_doors(doors_with_fire_rating_but_no_wall_fire_rating)
        door_to_room_names_with_fire_rating_but_no_wall_fire_rating  = door_to_from_room_names_with_fire_rating_but_no_wall_fire_rating [0]
        door_from_room_names_with_fire_rating_but_no_wall_fire_rating  = door_to_from_room_names_with_fire_rating_but_no_wall_fire_rating [1]
        door_Selections_with_invalid_fire_rating_but_no_wall_fire_rating = [out.linkify(door.Id) for door in doors_with_fire_rating_but_no_wall_fire_rating]
        
        doors_with_fire_rating_but_no_wall_rating_assigned = output_statement(door_numbers_with_fire_rating_but_no_wall_fire_rating, door_room_numbers_with_fire_rating_but_no_wall_fire_rating, door_room_names_with_fire_rating_but_no_wall_fire_rating, door_to_room_names_with_fire_rating_but_no_wall_fire_rating , door_from_room_names_with_fire_rating_but_no_wall_fire_rating, door_Selections_with_invalid_fire_rating_but_no_wall_fire_rating )
    print('\n ')
    print('*'*216)
    
    out.print_md('**WALL FIRE RATING,FOR DOORS WITH FIRE RATING CHECK- VALID/INVALID**')      
    if len(doors_with_walls_with_invalid_fire_ratings) == 0:
        print('\nFire Rating assigned to Walls, for Doors with Fire Rating are valid. ')
    else:
        print('\nFire Ratings assigned to Doors are not as per the Wall Fire Ratings and are invalid.\nPlease update the following Doors to have Fire ratings as per the formula below:\n\tDoor Fire Rating = Wall Fire Rating * 0.75.')
        door_numbers_with_walls_with_invalid_fire_ratings = [e for i, e in enumerate(door_numbers_with_fire_rating_and_wall_rating) if i in set_index_of_mismatch_doors_fire_rating_against_wall_ratings]
        door_room_numbers_with_walls_with_invalid_fire_ratings = shared_parameter_values(doors_with_walls_with_invalid_fire_ratings, 'Room_Number')
        door_room_names_with_walls_with_invalid_fire_ratings = shared_parameter_values(doors_with_walls_with_invalid_fire_ratings, 'Room_Name')
        door_to_from_room_names_with_walls_with_invalid_fire_ratings = troom_froom_name_for_doors(doors_with_walls_with_invalid_fire_ratings)
        door_to_room_names_with_walls_with_invalid_fire_ratings = door_to_from_room_names_with_walls_with_invalid_fire_ratings[0]
        door_from_room_names_with_walls_with_invalid_fire_ratings = door_to_from_room_names_with_walls_with_invalid_fire_ratings[1]
        door_Selections_with_walls_with_invalid_fire_ratings = [out.linkify(door.Id) for door in doors_with_walls_with_invalid_fire_ratings]
        
        doors_with_fire_rating_but_invalid_wall_fire_rating_assigned = output_statement(door_numbers_with_walls_with_invalid_fire_ratings,door_room_numbers_with_walls_with_invalid_fire_ratings, door_room_names_with_walls_with_invalid_fire_ratings, door_to_room_names_with_walls_with_invalid_fire_ratings, door_from_room_names_with_walls_with_invalid_fire_ratings, door_Selections_with_walls_with_invalid_fire_ratings)
    print('\n ')
    print('*'*216)    
      
####################################################################################################################

elif userInputcategory == '09.Acoustic Rating of Doors and against Wall Acoustic Ratings':
    
    out.print_md('**DOOR ACOUSTIC/STC RATING CHECK- ASSIGNED/NOT ASSIGNED**') 
    if len(doors_with_no_acoustic_rating_assigned) == 0:
        print('\nAcoustic/STC Rating has been assigned to all Doors. ')
    else:
        print('\nAcoustic/STC Rating for the following Doors have not been assigned.\nPlease add "0" in case of Doors with no Acoustic/STC Rating, for the Doors in the table below. ')
        door_numbers_with_no_acoustic_rating_assigned = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]
        door_room_numbers_with_no_acoustic_rating_assigned = [door_room_numbers_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]
        door_room_names_with_no_acoustic_rating_assigned = [door_room_names_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]
        door_to_room_names_with_no_acoustic_rating_assigned = [door_to_room_names_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]
        door_from_room_names_with_no_acoustic_rating_assigned = [door_from_room_names_with_valid_functions[i] for i in index_for_doors_with_no_acoustic_rating_assigned]
        door_Selections_with_no_acoustic_rating_assigned = [out.linkify(door.Id) for door in doors_with_no_acoustic_rating_assigned]
        
        doors_with_no_acoustic_rating_assigned = output_statement(door_numbers_with_no_acoustic_rating_assigned, door_room_numbers_with_no_acoustic_rating_assigned, door_room_names_with_no_acoustic_rating_assigned, door_to_room_names_with_no_acoustic_rating_assigned, door_from_room_names_with_no_acoustic_rating_assigned, door_Selections_with_no_acoustic_rating_assigned )    
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR ACOUSTIC/STC RATING CHECK- VALID/INVALID**')  
    if len(doors_with_invalid_acoustic_rating) == 0:
        print("\nAcoustic/STC Rating assigned to the Doors are valid and as per Design Requirements.")
    else:
        print('\nAcoustic/STC Rating assigned to the Doors do not match the Design Requirements.\nPlease verify the Acoustic/STC Rating for the Doors in the table below, against the Door Template for the project.')
        
        door_numbers_with_invalid_acoustic_rating = [e for i, e in enumerate(door_numbers_with_acoustic_rating) if i in set_index_of_mismatch_door_with_acoustic_rating]
        door_room_numbers_with_invalid_acoustic_rating = shared_parameter_values(doors_with_invalid_acoustic_rating, 'Room_Number')
        door_room_names_with_invalid_acoustic_rating = shared_parameter_values(doors_with_invalid_acoustic_rating, 'Room_Name')
        door_to_from_room_names_with_invalid_acoustic_rating = troom_froom_name_for_doors(doors_with_invalid_acoustic_rating)
        door_to_room_names_with_invalid_acoustic_rating = door_to_from_room_names_with_invalid_acoustic_rating[0]
        door_from_room_names_with_invalid_acoustic_rating = door_to_from_room_names_with_invalid_acoustic_rating[1]
        door_Selections_with_invalid_acoustic_rating = [out.linkify(door.Id) for door in doors_with_invalid_acoustic_rating]
        
        doors_with_invalid_acoustic_rating_assigned = output_statement(door_numbers_with_invalid_acoustic_rating, door_room_numbers_with_invalid_acoustic_rating, door_room_names_with_invalid_acoustic_rating, door_to_room_names_with_invalid_acoustic_rating, door_from_room_names_with_invalid_acoustic_rating, door_Selections_with_invalid_acoustic_rating)
    print('\n ')
    print('*'*216)
    
    out.print_md('**\nWALL ACOUSTIC/STC RATING,FOR DOORS WITH ACOUSTIC RATING CHECK- ASSIGNED/NOT ASSIGNED**')  
    if len(index_of_acoustic_rated_doors_with_no_wall_acoustic_rating) == 0:
        print("\nAcoustic/STC Rating has been assigned to all Walls, for Doors with Acoustic/STC Rating. ")
    else:
        print('\nAcoustic/STC Rating has not been assigned to Walls, for Doors with Acoustic/STC Rating.\nPlease add Acoustic/STC Rating to the Walls, on which the following Doors are hosted.\nIn case of Doors with "0" Acoustic/STC Rating, Please add "0" for the Wall Acoustic/STC Rating.')

        door_numbers_with_acoustic_rating_but_no_wall_acoustic_rating  = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in doors_with_acoustic_rating_but_no_wall_acoustic_rating]
        door_room_numbers_with_acoustic_rating_but_no_wall_acoustic_rating = shared_parameter_values(doors_with_acoustic_rating_but_no_wall_acoustic_rating, 'Room_Number')
        door_room_names_with_acoustic_rating_but_no_wall_acoustic_rating = shared_parameter_values(doors_with_acoustic_rating_but_no_wall_acoustic_rating, 'Room_Name')
        door_to_from_room_names_with_acoustic_rating_but_no_wall_acoustic_rating = troom_froom_name_for_doors(doors_with_acoustic_rating_but_no_wall_acoustic_rating)
        door_to_room_names_with_acoustic_rating_but_no_wall_acoustic_rating  = door_to_from_room_names_with_acoustic_rating_but_no_wall_acoustic_rating [0]
        door_from_room_names_with_acoustic_rating_but_no_wall_acoustic_rating  = door_to_from_room_names_with_acoustic_rating_but_no_wall_acoustic_rating [1]
        door_Selections_with_acoustic_rating_but_no_wall_acoustic_rating = [out.linkify(door.Id) for door in doors_with_acoustic_rating_but_no_wall_acoustic_rating]
                
        doors_with_acoustic_rating_but_no_wall_rating_assigned = output_statement(door_numbers_with_acoustic_rating_but_no_wall_acoustic_rating, door_room_numbers_with_acoustic_rating_but_no_wall_acoustic_rating, door_room_names_with_acoustic_rating_but_no_wall_acoustic_rating, door_to_room_names_with_acoustic_rating_but_no_wall_acoustic_rating , door_from_room_names_with_acoustic_rating_but_no_wall_acoustic_rating, door_Selections_with_acoustic_rating_but_no_wall_acoustic_rating )
    print('\n ')
    print('*'*216)
    
    out.print_md('**\nWALL ACOUSTIC/STC RATING,FOR DOORS WITH ACOUSITC RATING CHECK- VALID/INVALID**')     
    if len(doors_with_walls_with_invalid_acoustic_ratings) == 0:
        print('All Doors have Acoustic Ratings as per Wall Ratings,i.e. Door Rating = (Wall Rating - 15)')
    else:
        print('\nAcoustic/STC Ratings assigned to Doors are not as per the Wall Acoustic/STC Ratings and are invalid.\nPlease update the following Doors to have Acoustic ratings as per the formula below:-\n\tDoor Acoustic/STC Rating = Wall Acoustic Rating -15. ')
        door_numbers_with_walls_with_invalid_acoustic_ratings = [e for i, e in enumerate(door_numbers_with_acoustic_rating_and_wall_rating) if i in set_index_of_mismatch_doors_acoustic_rating_against_wall_ratings]
        door_room_numbers_with_walls_with_invalid_acoustic_ratings = shared_parameter_values(doors_with_walls_with_invalid_acoustic_ratings, 'Room_Number')
        door_room_names_with_walls_with_invalid_acoustic_ratings = shared_parameter_values(doors_with_walls_with_invalid_acoustic_ratings, 'Room_Name')
        door_to_from_room_names_with_walls_with_invalid_acoustic_ratings = troom_froom_name_for_doors(doors_with_walls_with_invalid_acoustic_ratings)
        door_to_room_names_with_walls_with_invalid_acoustic_ratings = door_to_from_room_names_with_walls_with_invalid_acoustic_ratings[0]
        door_from_room_names_with_walls_with_invalid_acoustic_ratings = door_to_from_room_names_with_walls_with_invalid_acoustic_ratings[1]
        door_Selections_with_walls_with_invalid_acoustic_ratings = [out.linkify(door.Id) for door in doors_with_walls_with_invalid_acoustic_ratings]
        
        doors_with_acoustic_rating_but_invalid_wall_acoustic_rating_assigned = output_statement(door_numbers_with_walls_with_invalid_acoustic_ratings,door_room_numbers_with_walls_with_invalid_acoustic_ratings, door_room_names_with_walls_with_invalid_acoustic_ratings, door_to_room_names_with_walls_with_invalid_acoustic_ratings, door_from_room_names_with_walls_with_invalid_acoustic_ratings, door_Selections_with_walls_with_invalid_acoustic_ratings)
    print('\n ')
    print('*'*216)    

####################################################################################################################

elif userInputcategory == '10.Leaf Material & Finishes':
    
    out.print_md('**DOOR LEAF MATERIAL CHECK- VALID/INVALID**')     
    if len(doors_with_invalid_leaf_material) == 0:
        print('\nLeaf Material for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nLeaf Material for the following Doors with valid Functions are invalid.\nPlease update the Leaf Material for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_leaf_material = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_doors_leaf_material]
        door_room_numbers_with_invalid_leaf_material = shared_parameter_values(doors_with_invalid_leaf_material, 'Room_Number')
        door_room_names_with_invalid_leaf_material = shared_parameter_values(doors_with_invalid_leaf_material, 'Room_Name')
        door_to_from_room_names_with_invalid_leaf_material =  troom_froom_name_for_doors(doors_with_invalid_leaf_material)
        door_to_room_names_with_invalid_leaf_material = door_to_from_room_names_with_invalid_leaf_material[0]
        door_from_room_names_with_invalid_leaf_material = door_to_from_room_names_with_invalid_leaf_material[1]
        door_Selections_with_invalid_leaf_material = [out.linkify(door.Id) for door in doors_with_invalid_leaf_material]
        
        doors_with_invalid_leaf_material_assigned = output_statement(door_numbers_with_invalid_leaf_material, door_room_numbers_with_invalid_leaf_material, door_room_names_with_invalid_leaf_material, door_to_room_names_with_invalid_leaf_material, door_from_room_names_with_invalid_leaf_material, door_Selections_with_invalid_leaf_material)
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR LEAF FINISH CHECK- VALID/INVALID**') 
    if len(doors_with_invalid_leaf_finish) == 0:
        print('\nLeaf Finishes for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nLeaf Finishes for the following Doors with valid Functions are invalid.\nPlease update the Leaf Finish for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_leaf_finish = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_doors_leaf_finish]
        door_room_numbers_with_invalid_leaf_finish = shared_parameter_values(doors_with_invalid_leaf_finish, 'Room_Number')
        door_room_names_with_invalid_leaf_finish = shared_parameter_values(doors_with_invalid_leaf_finish, 'Room_Name')
        door_to_from_room_names_with_invalid_leaf_finish =  troom_froom_name_for_doors(doors_with_invalid_leaf_finish)
        door_to_room_names_with_invalid_leaf_finish = door_to_from_room_names_with_invalid_leaf_finish[0]
        door_from_room_names_with_invalid_leaf_finish = door_to_from_room_names_with_invalid_leaf_finish[1]
        door_Selections_with_invalid_leaf_finish = [out.linkify(door.Id) for door in doors_with_invalid_leaf_finish]
        
        doors_with_invalid_leaf_finish_assigned = output_statement(door_numbers_with_invalid_leaf_finish, door_room_numbers_with_invalid_leaf_finish, door_room_names_with_invalid_leaf_finish, door_to_room_names_with_invalid_leaf_finish, door_from_room_names_with_invalid_leaf_finish, door_Selections_with_invalid_leaf_finish)
    print('\n ')
    print('*'*216)

##################################################################################################################

elif userInputcategory == '11.Frame Material & Finishes':
    
    out.print_md('**DOOR FRAME MATERIAL CHECK- VALID/INVALID**')  
    if len(doors_with_invalid_frame_material) == 0:
        print('\nFrame Material for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nFrame Material for the following Doors with valid Functions are invalid.\nPlease update the Frame Material for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_frame_material = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_doors_frame_material]
        door_room_numbers_with_invalid_frame_material = shared_parameter_values(doors_with_invalid_frame_material, 'Room_Number')
        door_room_names_with_invalid_frame_material = shared_parameter_values(doors_with_invalid_frame_material, 'Room_Name')
        door_to_from_room_names_with_invalid_frame_material =  troom_froom_name_for_doors(doors_with_invalid_frame_material)
        door_to_room_names_with_invalid_frame_material = door_to_from_room_names_with_invalid_frame_material[0]
        door_from_room_names_with_invalid_frame_material = door_to_from_room_names_with_invalid_frame_material[1]
        door_Selections_with_invalid_frame_material = [out.linkify(door.Id) for door in doors_with_invalid_frame_material]
        
        doors_with_invalid_frame_material_assigned = output_statement(door_numbers_with_invalid_frame_material, door_room_numbers_with_invalid_frame_material, door_room_names_with_invalid_frame_material, door_to_room_names_with_invalid_frame_material, door_from_room_names_with_invalid_frame_material, door_Selections_with_invalid_frame_material)
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR FRAME FINISH CHECK- VALID/INVALID**')
    if len(doors_with_invalid_frame_finish) == 0:
        print('\nFrame Finishes for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nFrame Finishes for the following Doors with valid Functions are invalid.\nPlease update the Leaf Finish for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_frame_finish = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_doors_frame_finish]
        door_room_numbers_with_invalid_frame_finish = shared_parameter_values(doors_with_invalid_frame_finish, 'Room_Number')
        door_room_names_with_invalid_frame_finish = shared_parameter_values(doors_with_invalid_frame_finish, 'Room_Name')
        door_to_from_room_names_with_invalid_frame_finish =  troom_froom_name_for_doors(doors_with_invalid_frame_finish)
        door_to_room_names_with_invalid_frame_finish = door_to_from_room_names_with_invalid_frame_finish[0]
        door_from_room_names_with_invalid_frame_finish = door_to_from_room_names_with_invalid_frame_finish[1]
        door_Selections_with_invalid_frame_finish = [out.linkify(door.Id) for door in doors_with_invalid_frame_finish]
        
        doors_with_invalid_frame_finish_assigned = output_statement(door_numbers_with_invalid_frame_finish, door_room_numbers_with_invalid_frame_finish, door_room_names_with_invalid_frame_finish, door_to_room_names_with_invalid_frame_finish, door_from_room_names_with_invalid_frame_finish, door_Selections_with_invalid_frame_finish)
    print('\n ')       
    print('*'*216)    
  
####################################################################################################################

elif userInputcategory == '12.Undercut':
    
    out.print_md('**DOOR UNDERCUT CHECK- VALID/INVALID**') 
    if len(doors_with_invalid_undercut) == 0:
        print('\nUndercut for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nUndercut for the following Doors with valid Functions are invalid.\nPlease update the Undercut for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_undercut = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_doors_with_undercut]
        door_room_numbers_with_invalid_undercut = shared_parameter_values(doors_with_invalid_undercut, 'Room_Number')
        door_room_names_with_invalid_undercut = shared_parameter_values(doors_with_invalid_undercut, 'Room_Name')
        door_to_from_room_names_with_invalid_undercut =  troom_froom_name_for_doors(doors_with_invalid_undercut)
        door_to_room_names_with_invalid_undercut = door_to_from_room_names_with_invalid_undercut[0]
        door_from_room_names_with_invalid_undercut = door_to_from_room_names_with_invalid_undercut[1]
        door_Selections_with_invalid_undercut = [out.linkify(door.Id) for door in doors_with_invalid_undercut]
        
        doors_with_invalid_undercut = output_statement(door_numbers_with_invalid_undercut, door_room_numbers_with_invalid_undercut, door_room_names_with_invalid_undercut, door_to_room_names_with_invalid_undercut, door_from_room_names_with_invalid_undercut, door_Selections_with_invalid_undercut)
    print('\n ') 
    print('*'*216)
    
####################################################################################################################

elif userInputcategory == '13.Fire Rated/Acoustically Treated Door with Grill':
    
    out.print_md('**DOOR GRILLS FOR FIRE RATED DOORS CHECK- ADDED/NOT ADDED**') 
    if len(doors_with_grills_and_fire_rated) == 0:
        print('\nDoor Grills have not been added, to any Doors with Fire Rating. ')
    else:
        print('\nDoor Grills have been provided to the following Fire Rated Doors.\nPlease check against the Design requirements, if sufficient hardware is being provided to the following Doors.')
              
        door_numbers_with_grills_and_fire_rated = [e for i, e in enumerate(door_numbers_with_grills) if i in index_of_doors_with_fire_rated_grill_doors]
        door_room_numbers_with_grills_and_fire_rated = shared_parameter_values(doors_with_grills_and_fire_rated, 'Room_Number')    
        door_room_names_with_grills_and_fire_rated = shared_parameter_values(doors_with_grills_and_fire_rated, 'Room_Name')
        door_to_from_room_names_with_grills_and_fire_rated = troom_froom_name_for_doors(doors_with_grills_and_fire_rated)
        door_to_room_names_with_grills_and_fire_rated = door_to_from_room_names_with_grills_and_fire_rated[0]
        door_from_room_names_with_grills_and_fire_rated = door_to_from_room_names_with_grills_and_fire_rated[1]
        door_Selections_with_grills_and_fire_rated = [out.linkify(door.Id) for door in doors_with_grills_and_fire_rated]
        
        doors_with_fire_rating_and_door_grills = output_statement(door_numbers_with_grills_and_fire_rated,  door_room_numbers_with_grills_and_fire_rated, door_room_names_with_grills_and_fire_rated,  door_to_room_names_with_grills_and_fire_rated,  door_from_room_names_with_grills_and_fire_rated, door_Selections_with_grills_and_fire_rated)   
    print('\n ')  
    print('*'*216)
    
    out.print_md('**DOOR GRILLS FOR ACOUSTIC/STC RATED DOORS CHECK- ADDED/NOT ADDED**') 
    if len(doors_with_grills_and_acoustic_rated) == 0:
        print('\nDoor Grills have not been added, to any Doors with Acoustic/STC Rating. ')
    else:
        print('\nDoor Grills have been provided to the following Acoustic/STC Rated Doors.\nPlease check against the Design requirements, if sufficient hardware is being provided to the following Doors.')
              
        door_numbers_with_grills_and_acoustic_rated = [e for i, e in enumerate(door_numbers_with_grills) if i in index_of_doors_with_acoustic_rated_grill_doors]
        door_room_numbers_with_grills_and_acoustic_rated = shared_parameter_values(doors_with_grills_and_acoustic_rated, 'Room_Number')    
        door_room_names_with_grills_and_acoustic_rated = shared_parameter_values(doors_with_grills_and_acoustic_rated, 'Room_Name')
        door_to_from_room_names_with_grills_and_acoustic_rated = troom_froom_name_for_doors(doors_with_grills_and_acoustic_rated)
        door_to_room_names_with_grills_and_acoustic_rated = door_to_from_room_names_with_grills_and_acoustic_rated[0]
        door_from_room_names_with_grills_and_acoustic_rated = door_to_from_room_names_with_grills_and_acoustic_rated[1]
        door_Selections_with_grills_and_acoustic_rated = [out.linkify(door.Id) for door in doors_with_grills_and_acoustic_rated]
        
        doors_with_acoustic_rating_and_door_grills = output_statement(door_numbers_with_grills_and_acoustic_rated,  door_room_numbers_with_grills_and_acoustic_rated, door_room_names_with_grills_and_acoustic_rated,  door_to_room_names_with_grills_and_acoustic_rated,  door_from_room_names_with_grills_and_acoustic_rated, door_Selections_with_grills_and_acoustic_rated)   
    print('\n ') 
    print('*'*216)
   
####################################################################################################################

elif userInputcategory == '14.Leaf Type':
    
    out.print_md('**DOOR LEAF TYPE CHECK- VALID/INVALID**')     
    if len(doors_with_invalid_leaf_type) == 0:
        print('\nLeaf Type for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nLeaf Type for the following Doors with valid Functions are invalid.\nPlease update the Leaf Type for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_leaf_type = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_door_leaf_type]
        door_room_numbers_with_invalid_leaf_type = shared_parameter_values(doors_with_invalid_leaf_type, 'Room_Number')
        door_room_names_with_invalid_leaf_type = shared_parameter_values(doors_with_invalid_leaf_type, 'Room_Name')
        door_to_from_room_names_with_invalid_leaf_type =  troom_froom_name_for_doors(doors_with_invalid_leaf_type)
        door_to_room_names_with_invalid_leaf_type = door_to_from_room_names_with_invalid_leaf_type[0]
        door_from_room_names_with_invalid_leaf_type = door_to_from_room_names_with_invalid_leaf_type[1]
        door_Selections_with_invalid_leaf_type = [out.linkify(door.Id) for door in doors_with_invalid_leaf_type]
        
        doors_with_invalid_leaf_type_assigned = output_statement(door_numbers_with_invalid_leaf_type, door_room_numbers_with_invalid_leaf_type, door_room_names_with_invalid_leaf_type, door_to_room_names_with_invalid_leaf_type, door_from_room_names_with_invalid_leaf_type, door_Selections_with_invalid_leaf_type)
    print('\n ')
    print('*'*216)

####################################################################################################################

elif userInputcategory == '15.Leaf Construction':
    
    out.print_md('**DOOR LEAF CONSTRUCTION CHECK- VALID/INVALID**')     
    if len(doors_with_invalid_leaf_construction) == 0:
        print('\nLeaf Construction for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nLeaf Construction for the following Doors with valid Functions are invalid.\nPlease update the Leaf Construction for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_leaf_construction = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_door_leaf_construction]
        door_room_numbers_with_invalid_leaf_construction = shared_parameter_values(doors_with_invalid_leaf_construction, 'Room_Number')
        door_room_names_with_invalid_leaf_construction = shared_parameter_values(doors_with_invalid_leaf_construction, 'Room_Name')
        door_to_from_room_names_with_invalid_leaf_construction =  troom_froom_name_for_doors(doors_with_invalid_leaf_construction)
        door_to_room_names_with_invalid_leaf_construction = door_to_from_room_names_with_invalid_leaf_construction[0]
        door_from_room_names_with_invalid_leaf_construction = door_to_from_room_names_with_invalid_leaf_construction[1]
        door_Selections_with_invalid_leaf_construction = [out.linkify(door.Id) for door in doors_with_invalid_leaf_construction]
        
        doors_with_invalid_leaf_construction_type_assigned = output_statement(door_numbers_with_invalid_leaf_construction, door_room_numbers_with_invalid_leaf_construction, door_room_names_with_invalid_leaf_construction, door_to_room_names_with_invalid_leaf_construction, door_from_room_names_with_invalid_leaf_construction, door_Selections_with_invalid_leaf_construction)
    print('\n ')
    print('*'*216)  

####################################################################################################################

elif userInputcategory == '16.Frame Elevation':

    out.print_md('**DOOR FRAME ELEVATION CHECK- VALID/INVALID**')     
    if len(doors_with_invalid_frame_elevation) == 0:
        print('\nFrame Elevation for Doors with valid Functions are valid and meet the Design Requirements. ')
    else:
        print('\nFrame Elevation for the following Doors with valid Functions are invalid.\nPlease update the Frame Elevation for the following Doors as per Design Requirements. ')
        door_numbers_with_invalid_frame_elevation = [e for i, e in enumerate(door_numbers_with_valid_functions) if i in set_index_of_mismatch_door_frame_elevation]
        door_room_numbers_with_invalid_frame_elevation = shared_parameter_values(doors_with_invalid_frame_elevation, 'Room_Number')
        door_room_names_with_invalid_frame_elevation = shared_parameter_values(doors_with_invalid_frame_elevation, 'Room_Name')
        door_to_from_room_names_with_invalid_frame_elevation =  troom_froom_name_for_doors(doors_with_invalid_frame_elevation)
        door_to_room_names_with_invalid_frame_elevation = door_to_from_room_names_with_invalid_frame_elevation[0]
        door_from_room_names_with_invalid_frame_elevation = door_to_from_room_names_with_invalid_frame_elevation[1]
        door_Selections_with_invalid_frame_elevation = [out.linkify(door.Id) for door in doors_with_invalid_frame_elevation]
        
        doors_with_invalid_frame_elevation_assigned = output_statement(door_numbers_with_invalid_frame_elevation, door_room_numbers_with_invalid_frame_elevation, door_room_names_with_invalid_frame_elevation, door_to_room_names_with_invalid_frame_elevation, door_from_room_names_with_invalid_frame_elevation, door_Selections_with_invalid_frame_elevation)
    print('\n ')
    print('*'*216) 
        
####################################################################################################################

elif userInputcategory == '17.Frame Profile':

    out.print_md('**DOOR FRAME PROFILE CHECK- ASSIGNED/NOT ASSIGNED**')  
    if len(doors_with_no_frame_profile_assigned) == 0:
        print('\nFrame Profile has been assigned to all Doors. ')
    else:
        print('\nFrame Profile for the following Doors have not been assigned. ')
        door_numbers_with_no_frame_profile_assigned = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]
        door_room_numbers_with_no_frame_profile_assigned = [door_room_numbers_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]
        door_room_names_with_no_frame_profile_assigned = [door_room_names_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]
        door_to_room_names_with_no_frame_profile_assigned = [door_to_room_names_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]
        door_from_room_names_with_no_frame_profile_assigned = [door_from_room_names_with_valid_functions[i] for i in index_for_doors_with_no_frame_profile_assigned]
        door_Selections_with_no_frame_profile_assigned = [out.linkify(door.Id) for door in doors_with_no_frame_profile_assigned]
        
        doors_with_no_frame_profile_assigned = output_statement(door_numbers_with_no_frame_profile_assigned, door_room_numbers_with_no_frame_profile_assigned, door_room_names_with_no_frame_profile_assigned, door_to_room_names_with_no_frame_profile_assigned, door_from_room_names_with_no_frame_profile_assigned, door_Selections_with_no_frame_profile_assigned)    
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR FRAME PROFILE CHECK- VALID/INVALID**')  
    if len(doors_with_invalid_frame_profile) == 0:
        print("\nFrame Profile assigned to the Doors are valid and as per Design Requirements.")
    else:
        print('\nFrame Profile assigned to the Doors do not match the Design Requirements.\nPlease verify the Frame Profile for the Doors in the table below, against the Door Template for the project.')
        door_numbers_with_invalid_frame_profile = [e for i, e in enumerate(door_numbers_with_frame_profile) if i in set_index_of_mismatch_door_with_frame_profile]
        door_room_numbers_with_invalid_frame_profile = shared_parameter_values(doors_with_invalid_frame_profile, 'Room_Number')
        door_room_names_with_invalid_frame_profile = shared_parameter_values(doors_with_invalid_frame_profile, 'Room_Name')
        door_to_from_room_names_with_invalid_frame_profile = troom_froom_name_for_doors(doors_with_invalid_frame_profile)
        door_to_room_names_with_invalid_frame_profile = door_to_from_room_names_with_invalid_frame_profile[0]
        door_from_room_names_with_invalid_frame_profile = door_to_from_room_names_with_invalid_frame_profile[1]
        door_Selections_with_invalid_frame_profile = [out.linkify(door.Id) for door in doors_with_invalid_frame_profile]
        
        doors_with_invalid_frame_profile_assigned = output_statement(door_numbers_with_invalid_frame_profile, door_room_numbers_with_invalid_frame_profile, door_room_names_with_invalid_frame_profile, door_to_room_names_with_invalid_frame_profile, door_from_room_names_with_invalid_frame_profile, door_Selections_with_invalid_frame_profile)
    print('\n ')
    print('*'*216)

####################################################################################################################

elif userInputcategory == '18.Saddle Type':

    out.print_md('**DOOR SADDLE TYPE CHECK- ASSIGNED/NOT ASSIGNED**')  
    if len(doors_with_no_saddle_type_assigned) == 0:
        print('\nSaddle Type has been assigned to all Doors. ')
    else:
        print('\nSaddle Type for the following Doors have not been assigned. ')
        door_numbers_with_no_saddle_type_assigned = [door_numbers_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]
        door_room_numbers_with_no_saddle_type_assigned = [door_room_numbers_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]
        door_room_names_with_no_saddle_type_assigned = [door_room_names_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]
        door_to_room_names_with_no_saddle_type_assigned = [door_to_room_names_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]
        door_from_room_names_with_no_saddle_type_assigned = [door_from_room_names_with_valid_functions[i] for i in index_for_doors_with_no_saddle_type_assigned]
        door_Selections_with_no_saddle_type_assigned = [out.linkify(door.Id) for door in doors_with_no_saddle_type_assigned]
        
        doors_with_no_saddle_type_assigned = output_statement(door_numbers_with_no_saddle_type_assigned, door_room_numbers_with_no_saddle_type_assigned, door_room_names_with_no_saddle_type_assigned, door_to_room_names_with_no_saddle_type_assigned, door_from_room_names_with_no_saddle_type_assigned, door_Selections_with_no_saddle_type_assigned)    
    print('\n ')
    print('*'*216)
    
    out.print_md('**DOOR SADDLE TYPE CHECK- VALID/INVALID**')  
    if len(doors_with_invalid_saddle_type) == 0:
        print("\nSaddle Type assigned to the Doors are valid and as per Design Requirements.")
    else:
        print('\nSaddle Type assigned to the Doors do not match the Design Requirements.\nPlease verify the Saddle Type for the Doors in the table below, against the Door Template for the project.')
        door_numbers_with_invalid_saddle_type = [e for i, e in enumerate(door_numbers_with_saddle_type) if i in set_index_of_mismatch_door_with_saddle_type]
        door_room_numbers_with_invalid_saddle_type = shared_parameter_values(doors_with_invalid_saddle_type, 'Room_Number')
        door_room_names_with_invalid_saddle_type = shared_parameter_values(doors_with_invalid_saddle_type, 'Room_Name')
        door_to_from_room_names_with_invalid_saddle_type = troom_froom_name_for_doors(doors_with_invalid_saddle_type)
        door_to_room_names_with_invalid_saddle_type = door_to_from_room_names_with_invalid_saddle_type[0]
        door_from_room_names_with_invalid_saddle_type = door_to_from_room_names_with_invalid_saddle_type[1]
        door_Selections_with_invalid_saddle_type = [out.linkify(door.Id) for door in doors_with_invalid_saddle_type]
        
        doors_with_invalid_saddle_type_assigned = output_statement(door_numbers_with_invalid_saddle_type, door_room_numbers_with_invalid_saddle_type, door_room_names_with_invalid_saddle_type, door_to_room_names_with_invalid_saddle_type, door_from_room_names_with_invalid_saddle_type, door_Selections_with_invalid_saddle_type)
    print('\n ')
    print('*'*216)
    pass

####################################################################################################################

else:
    pass

####################################################################################################################



