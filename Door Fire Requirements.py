"""Fire Code Compatibility"""

__title__ = "Fire Code\nCompatibility"
__author__= "J K Roshan\nKerketta"

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from itertools import chain
from itertools import islice

out = script.get_output()
out.add_style('body{font-family: CenturyGothic; font-size: 12pt; }')

####################################################################################################################

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

####################################################################################################################

from pyrevit import HOST_APP
from pyrevit import revit, DB
import math

####################################################################################################################

def format_length(length_value, doc = None):
    doc = doc or HOST_APP.doc
    return DB.UnitFormatUtils.Format(units = doc.GetUnits(), unitType = DB.UnitType.UT_Length, value = length_value, maxAccuracy = False, forEditing =False)

####################################################################################################################
# Function to acquire all elements of category & get parameter value by name 

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()

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

doors = all_elements_of_category(BuiltInCategory.OST_Doors)
# print(doors)
door_comments = [d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsString() for d in doors]
# print(door_comments)

exclusions = ["ROLLING SHUTTER", "ACCESS PANEL", "CLOSET DOOR", "GLASS DOOR" , "CURTAIN WALL DOOR"]

indices_for_non_glazed_doors = [i for i, x in enumerate(door_comments) if x not in exclusions]
doors = [doors[i] for i in indices_for_non_glazed_doors]
door_numbers = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in doors]


#  Sorted Doors by Door Number

indices_of_sorted_doors = sorted(range(len(door_numbers)), key=lambda k: door_numbers[k])

doors = [doors[i] for i in indices_of_sorted_doors]
door_numbers = [door_numbers[i] for i in indices_of_sorted_doors]
# print(door_numbers)
# Getting Room Numbers in Doors 
door_room_numbers = shared_parameter_values(doors, 'Room_Number')
# print(door_room_numbers)

# Getting Room Numbers in Doors 
door_room_names = shared_parameter_values(doors, 'Room_Name')
# print(door_room_names)

# Getting Door Selections
door_Selections = [out.linkify(d.Id) for d in doors]

####################################################################################################################
# Function for checking Family Type Door Parameters(AsInteger, AsDouble, AsString)

def all_elements_with_type_parameter_AsInteger(doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in doors:
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

def all_elements_with_type_parameter_AsDouble(doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in doors:
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

def all_elements_with_type_parameter_AsString(doors, door_family_type_parameter):
    door_family_test = []
    door_family_param = []
    
    for d in doors:
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

####################################################################################################################

# Getting failed elements (Doors & Door Numbers)
def doors_with_family_param_failure(sample_door_family_test,sample_doors, sample_door_nums):
    index_of_doors_with_family_param_failure = [i for i, x in enumerate(sample_door_family_test) if x == 'fail']
    doors_with_family_test_issues = [sample_doors[i] for i in index_of_doors_with_family_param_failure]
    door_numbers_with_family_test_issues = [sample_door_nums[i] for i in index_of_doors_with_family_param_failure]        
    return (doors_with_family_test_issues, door_numbers_with_family_test_issues)

# Getting passed elements (Doors & Door Numbers)
def doors_with_family_param_pass(sample_door_family_test,sample_doors, sample_door_nums):
    index_of_doors_with_family_param_pass = [i for i, x in enumerate(sample_door_family_test) if x != 'fail']
    doors_with_family_test_pass = [sample_doors[i] for i in index_of_doors_with_family_param_pass]
    door_numbers_with_family_test_pass = [sample_door_nums[i] for i in index_of_doors_with_family_param_pass]
    return (doors_with_family_test_pass, door_numbers_with_family_test_pass)

####################################################################################################################
# Getting Leaf Number
test_for_doors_with_leaves = all_elements_with_type_parameter_AsInteger(doors, 'Leaf_Number')
# print(test_for_doors_with_leaves)
filter_doors_with_leaf_number_param_pass = doors_with_family_param_pass(test_for_doors_with_leaves, doors, door_numbers)
# print(filter_doors_with_leaf_number_param_pass)
filtered_doors = filter_doors_with_leaf_number_param_pass[0]
# print(filtered_doors)
filtered_door_nums = filter_doors_with_leaf_number_param_pass[1]
# print(filtered_door_nums)

# Single Doors
index_of_doors_with_single_leaf = [ i for i, x in enumerate(test_for_doors_with_leaves) if x == 1]
doors_with_single_leaf = [doors[i] for i in index_of_doors_with_single_leaf]
door_numbers_for_doors_with_single_leaf = [door_numbers[i] for i in index_of_doors_with_single_leaf]
door_room_numbers_for_doors_with_single_leaf = [door_room_numbers[i] for i in index_of_doors_with_single_leaf]
door_room_names_for_doors_with_single_leaf = [door_room_names[i] for i in index_of_doors_with_single_leaf]
door_Selections_for_doors_with_single_leaf = [door_Selections[i] for i in index_of_doors_with_single_leaf]
    
# Double Doors(Unequal & Equal)
index_of_doors_with_double_leaves= [ i for i, x in enumerate(test_for_doors_with_leaves) if x == 2]
doors_with_double_leaves = [doors[i] for i in index_of_doors_with_double_leaves]
door_numbers_for_doors_with_double_leaves = [door_numbers[i] for i in index_of_doors_with_double_leaves]
door_room_numbers_for_doors_with_double_leaves = [door_room_numbers[i] for i in index_of_doors_with_double_leaves]
door_room_names_for_doors_with_double_leaves = [door_room_names[i] for i in index_of_doors_with_double_leaves]
door_Selections_for_doors_with_double_leaves = [door_Selections[i] for i in index_of_doors_with_double_leaves]

####################################################################################################################

# Filtering doors with Equal & Unequal Leaves
test_for_double_leaf_doors = all_elements_with_type_parameter_AsDouble(doors_with_double_leaves,'Side Panel Width')
# print(test_for_double_leaf_doors) 

# Doors with Unequal Leaves
filter_doors_with_unequal_leaves_pass = doors_with_family_param_pass(test_for_double_leaf_doors, doors_with_double_leaves, door_numbers_for_doors_with_double_leaves)
filtered_unequal_leaf_doors = filter_doors_with_unequal_leaves_pass[0]
filtered_unequal_leaf_door_nums = [d.get_Parameter(BuiltInParameter.DOOR_NUMBER).AsString() for d in filtered_unequal_leaf_doors]
# print(filtered_unequal_leaf_door_nums)
filtered_unequal_leaf_door_room_nums = shared_parameter_values(filtered_unequal_leaf_doors, 'Room_Number')
filtered_unequal_leaf_door_room_names = shared_parameter_values(filtered_unequal_leaf_doors, 'Room_Name')
filtered_unequal_leaf_door_Selections = [out.linkify(d.Id) for d in filtered_unequal_leaf_doors]

# Doors with Equal Leaves
filter_doors_with_unequal_leaves_fail = doors_with_family_param_failure(test_for_double_leaf_doors, doors_with_double_leaves, door_numbers_for_doors_with_double_leaves)
filtered_equal_leaf_doors = filter_doors_with_unequal_leaves_fail[0]
filtered_equal_leaf_door_nums = filter_doors_with_unequal_leaves_fail[1]
# print(filter_doors_with_unequal_leaves_fail)
filtered_equal_leaf_door_room_nums = shared_parameter_values(filtered_equal_leaf_doors, 'Room_Number')
filtered_equal_leaf_door_room_names = shared_parameter_values(filtered_equal_leaf_doors, 'Room_Name')
filtered_equal_leaf_door_Selections = [out.linkify(d.Id) for d in filtered_equal_leaf_doors]

####################################################################################################################
# Leaf Height for Doors

clear_height_for_doors = all_elements_with_type_parameter_AsDouble(doors, 'Leaf_Height')
# print(clear_height_for_doors)

# Doors with Leaf Height Parameter
filter_doors_with_clear_height_pass = doors_with_family_param_pass(clear_height_for_doors, doors, door_numbers)
filtered_doors_with_clear_height = filter_doors_with_clear_height_pass[0]
filtered_door_nums_with_clear_height = filter_doors_with_clear_height_pass[1]
filtered_door_room_nums_with_clear_height = shared_parameter_values(filtered_doors_with_clear_height, 'Room_Number')
filtered_door_room_names_with_clear_height = shared_parameter_values(filtered_doors_with_clear_height, 'Room_Name')
filtered_door_Selections_with_clear_height = [out.linkify(d.Id) for d in filtered_doors_with_clear_height]

# Doors with no Leaf Height Parameter
filter_doors_with_clear_height_fail = doors_with_family_param_failure(clear_height_for_doors, doors, door_numbers)
filtered_doors_with_no_leaf_height_parameter = filter_doors_with_clear_height_fail[0]
filtered_door_nums_with_no_leaf_height_param = filter_doors_with_clear_height_fail[1]

####################################################################################################################

# Function for unit conversion
def unit_conversion(revit_value_in_feet):
    resultant_value_from_revit = [float(x) for x in revit_value_in_feet]
    resultant_value_unit_conversion = [format_length(x) for x in resultant_value_from_revit]
    resultant_value_converted_to_mm = [int(x) for x in resultant_value_unit_conversion]
    return(resultant_value_converted_to_mm)

def output_statement_for_door_sizes(sample_door_Selections_with_issues, sample_door_nums_with_issues, sample_door_room_nums_with_issues, sample_door_room_names_with_issues):
    output_for_door_size_issues = [zip(sample_door_Selections_with_issues, sample_door_nums_with_issues, sample_door_room_nums_with_issues, sample_door_room_names_with_issues)]
    for output in output_for_door_size_issues:
        out.print_table(table_data = output, title = 'DOOR CHECKING TABLE', columns = ['Element ID','Door Number', 'Room Number', 'Room Name'], formats = ['','','',''])
    
##############################################################################
# Check Single Leaf Door Width

def single_leaf_door_width(sample_code, minimum_single_leaf_width, maximum_single_leaf_width, sample_doors_with_single_leaf = doors_with_single_leaf, sample_door_numbers_for_doors_with_single_leaf = door_numbers_for_doors_with_single_leaf, sample_door_room_numbers_for_doors_with_single_leaf = door_room_numbers_for_doors_with_single_leaf, sample_door_room_names_for_doors_with_single_leaf = door_room_names_for_doors_with_single_leaf, sample_door_Selections_for_doors_with_single_leaf = door_Selections_for_doors_with_single_leaf):
    out.print_md('**{} CODE- MINIMUM CLEAR WIDTH- SINGLE LEAF DOORS**'.format(sample_code))
    sample_single_leaf_doors_width = all_elements_with_type_parameter_AsDouble(sample_doors_with_single_leaf, 'Leaf_Width')
    sample_single_leaf_doors_width_convert = unit_conversion(sample_single_leaf_doors_width )
    
    # Check minimum dimensions for single leaf as per code
    sample_index_of_failure_single_door_minimum_sizes = [i for i, x in enumerate(sample_single_leaf_doors_width_convert) if x < minimum_single_leaf_width]
    
    # Check maximum dimensions for single leaf as per code
    sample_index_of_failure_single_door_maximum_sizes = [i for i, x in enumerate(sample_single_leaf_doors_width_convert) if x > maximum_single_leaf_width]

    if (len(sample_index_of_failure_single_door_minimum_sizes) == 0):
        print('\Single Leaf Door Width meet the minimum size of {} mm as per {} requirements. '.format(minimum_single_leaf_width, sample_code))
    else:
        test_doors_with_single_leaf_lesser_than_permissible_sizes = [sample_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_minimum_sizes]
        test_door_numbers_with_single_leaf_lesser_than_permissible_sizes = [sample_door_numbers_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_minimum_sizes]
        test_door_room_numbers_with_single_leaf_lesser_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_minimum_sizes]
        test_door_room_names_with_single_leaf_lesser_than_permissible_sizes = [sample_door_room_names_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_minimum_sizes]  
        test_door_Selections_with_single_leaf_lesser_than_permissible_sizes = [sample_door_Selections_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_minimum_sizes]
        print("\nThe Leaf Width of the following Single Leaf Doors need to be updated to meet {} Code requirements,\nof minimum Leaf Size, i.e. greater than {} mm: -".format(sample_code, minimum_single_leaf_width))
        output_for_doors_with_single_leaf_lesser_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_single_leaf_lesser_than_permissible_sizes, test_door_numbers_with_single_leaf_lesser_than_permissible_sizes, test_door_room_numbers_with_single_leaf_lesser_than_permissible_sizes, test_door_room_names_with_single_leaf_lesser_than_permissible_sizes)
    print(' \n')
    print('*'*216) 
    
    out.print_md('**{} CODE- MAXIMUM CLEAR WIDTH- SINGLE LEAF DOORS**'.format(sample_code))


    if (len(sample_index_of_failure_single_door_maximum_sizes) == 0):
        print('\nSingle Leaf Door Width meet the maximum size of {} mm as per {} requirements. '.format(maximum_single_leaf_width, sample_code))
    else:
        test_doors_with_single_leaf_greater_than_permissible_sizes = [sample_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_maximum_sizes]
        test_door_numbers_with_single_leaf_greater_than_permissible_sizes = [sample_door_numbers_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_maximum_sizes]
        test_door_room_numbers_with_single_leaf_greater_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_maximum_sizes]
        test_door_room_names_with_single_leaf_greater_than_permissible_sizes = [sample_door_room_names_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_maximum_sizes]  
        test_door_Selections_with_single_leaf_greater_than_permissible_sizes = [sample_door_Selections_for_doors_with_single_leaf[i] for i in sample_index_of_failure_single_door_maximum_sizes]
        print("\nThe Leaf Width of the following Single Leaf Doors need to be updated to meet {} Code requirements,\nof maximum Leaf Size, i.e. less than {} mm:-".format(sample_code, maximum_single_leaf_width))
        output_for_doors_with_single_leaf_greater_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_single_leaf_greater_than_permissible_sizes, test_door_numbers_with_single_leaf_greater_than_permissible_sizes, test_door_room_numbers_with_single_leaf_greater_than_permissible_sizes, test_door_room_names_with_single_leaf_greater_than_permissible_sizes)
    print(' \n')
    print('*'*216)    
   
    
def unequal_leaf_door_width(sample_code, minimum_side_panel_width, maximum_side_panel_width, minimum_main_panel_width, maximum_main_panel_width, sample_doors_with_unequal_leaf = filtered_unequal_leaf_doors, sample_door_numbers_for_doors_with_unequal_leaf = filtered_unequal_leaf_door_nums, sample_door_room_numbers_for_doors_with_unequal_leaf = filtered_unequal_leaf_door_room_nums, sample_door_room_names_for_doors_with_unequal_leaf = filtered_unequal_leaf_door_room_names, sample_door_Selections_for_doors_with_unequal_leaf = filtered_unequal_leaf_door_Selections):
    out.print_md('**{} CODE- MINIMUM SIDE PANEL WIDTH- DOUBLE UNEQUAL LEAF DOORS**'.format(sample_code))
    sample_unequal_leaf_doors_side_panel_width = all_elements_with_type_parameter_AsDouble(sample_doors_with_unequal_leaf, 'Side Panel Width')
    sample_unequal_leaf_doors_side_panel_width_convert = unit_conversion(sample_unequal_leaf_doors_side_panel_width )
    
    # Check minimum dimensions for Unequal Leaf Door -Side Panel Minimum size
    sample_index_of_failure_unequal_door_side_panel_minimum_sizes = [i for i, x in enumerate(sample_unequal_leaf_doors_side_panel_width_convert) if minimum_side_panel_width < x < 600]
    # Check maximum dimensions for Unequal Leaf Door- Side Panel Maximum size
    sample_index_of_failure_unequal_door_side_panel_maximum_sizes = [i for i, x in enumerate(sample_unequal_leaf_doors_side_panel_width_convert) if x > maximum_side_panel_width]
    # Check minimum dimensions for Unequal Leaf Door -Main Panel Minimum size
    sample_index_of_failure_unequal_door_main_panel_minimum_sizes = [i for i, x in enumerate(sample_unequal_leaf_doors_side_panel_width_convert) if x < minimum_side_panel_width]
    # Check maximum dimensions for Unequal Leaf Door- Main Panel Maximum size
    sample_index_of_failure_unequal_door_main_panel_maximum_sizes = [i for i, x in enumerate(sample_unequal_leaf_doors_side_panel_width_convert) if x > maximum_side_panel_width]

    if (len(sample_index_of_failure_unequal_door_side_panel_minimum_sizes) == 0):
        print('\nUnequal Leaf Doors Side Panel Widths meet the minimum size of {} mm & less than 600 mm as per {} requirements. '.format(minimum_side_panel_width, sample_code))
    else:
        test_doors_with_side_panel_lesser_than_permissible_sizes = [sample_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_minimum_sizes]
        test_door_numbers_with_side_panel_lesser_than_permissible_sizes = [sample_door_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_minimum_sizes]
        test_door_room_numbers_with_side_panel_lesser_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_minimum_sizes]
        test_door_room_names_with_side_panel_lesser_than_permissible_sizes = [sample_door_room_names_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_minimum_sizes]  
        test_door_Selections_with_side_panel_lesser_than_permissible_sizes = [sample_door_Selections_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_minimum_sizes]
        print("\nThe Side Panel Width of the following Unequal Leaf Doors need to be updated to meet {} Code requirements,\nof minimum Side Panel Size, i.e. greater than {} mm, but lesser than 600 mm: -".format(sample_code, minimum_side_panel_width))
        output_for_doors_with_unequal_side_panel_lesser_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_side_panel_lesser_than_permissible_sizes, test_door_numbers_with_side_panel_lesser_than_permissible_sizes, test_door_room_numbers_with_side_panel_lesser_than_permissible_sizes, test_door_room_names_with_side_panel_lesser_than_permissible_sizes)
    print(' \n')
    print('*'*216) 
   
    out.print_md('**{} CODE- MAXIMUM SIDE PANEL WIDTH- UNEQUAL LEAF DOORS**'.format(sample_code))

    if (len(sample_index_of_failure_unequal_door_side_panel_maximum_sizes) == 0):
        print('\nUnequal Leaf Door Side Panel Width meet the maximum size of {} mm as per {} requirements. '.format(maximum_side_panel_width, sample_code))
    else:
        test_doors_with_side_panel_greater_than_permissible_sizes = [sample_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_maximum_sizes]
        test_door_numbers_with_side_panel_greater_than_permissible_sizes = [sample_door_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_maximum_sizes]
        test_door_room_numbers_with_side_panel_greater_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_maximum_sizes]
        test_door_room_names_with_side_panel_greater_than_permissible_sizes = [sample_door_room_names_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_maximum_sizes]  
        test_door_Selections_with_side_panel_greater_than_permissible_sizes = [sample_door_Selections_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_side_panel_maximum_sizes]
        print("\nThe Side Panel Width of the following Unequal Leaf Doors need to be updated to meet {} Code requirements,\nof Side Panel Size, i.e. lesser than {} mm: -".format(sample_code, maximum_side_panel_width))
        output_for_doors_with_unequal_side_panel_greater_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_side_panel_greater_than_permissible_sizes, test_door_numbers_with_side_panel_greater_than_permissible_sizes, test_door_room_numbers_with_side_panel_greater_than_permissible_sizes, test_door_room_names_with_side_panel_greater_than_permissible_sizes)
    print(' \n')
    print('*'*216)

    if (len(sample_index_of_failure_unequal_door_main_panel_minimum_sizes) == 0):
        print('\nUnequal Leaf Door Main Panel Width meet the minimum size of {} mm as per {} requirements. '.format(minimum_main_panel_width, sample_code))
    else:
        test_doors_with_main_panel_lesser_than_permissible_sizes = [sample_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_minimum_sizes]
        test_door_numbers_with_main_panel_lesser_than_permissible_sizes = [sample_door_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_minimum_sizes]
        test_door_room_numbers_with_main_panel_lesser_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_minimum_sizes]
        test_door_room_names_with_main_panel_lesser_than_permissible_sizes = [sample_door_room_names_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_minimum_sizes]  
        test_door_Selections_with_main_panel_lesser_than_permissible_sizes = [sample_door_Selections_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_minimum_sizes]
        print("\nThe Main Panel Width of the following Unequal Leaf Doors need to be updated to meet {} Code requirements,\nof Main Panel Size, i.e. greater than {} mm: -".format(sample_code, minimum_main_panel_width))
        output_for_doors_with_unequal_main_panel_lesser_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_main_panel_lesser_than_permissible_sizes, test_door_numbers_with_main_panel_lesser_than_permissible_sizes, test_door_room_numbers_with_main_panel_lesser_than_permissible_sizes, test_door_room_names_with_main_panel_lesser_than_permissible_sizes)
    print(' \n')
    print('*'*216) 
    
    out.print_md('**{} CODE -MAXIMUM MAIN PANEL WIDTH- UNEQUAL LEAF DOORS**'.format(sample_code))

    if (len(sample_index_of_failure_unequal_door_main_panel_maximum_sizes) == 0):
        print('\nUnequal Leaf Door Main Panel Width meet the maximum size of {} mm as per {} requirements. '.format(maximum_main_panel_width, sample_code))
    else:
        test_doors_with_main_panel_greater_than_permissible_sizes = [sample_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_maximum_sizes]
        test_door_numbers_with_main_panel_greater_than_permissible_sizes = [sample_door_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_maximum_sizes]
        test_door_room_numbers_with_main_panel_greater_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_maximum_sizes]
        test_door_room_names_with_main_panel_greater_than_permissible_sizes = [sample_door_room_names_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_maximum_sizes]  
        test_door_Selections_with_main_panel_greater_than_permissible_sizes = [sample_door_Selections_for_doors_with_unequal_leaf[i] for i in sample_index_of_failure_unequal_door_main_panel_maximum_sizes]
        print("\nThe Main Panel Width of the following Unequal Leaf Doors need to be updated to meet {} Code requirements,\nof Main Panel Size, i.e. lesser than {} mm: -".format(sample_code, maximum_main_panel_width))
        output_for_doors_with_unequal_main_panel_greater_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_main_panel_greater_than_permissible_sizes, test_door_numbers_with_main_panel_greater_than_permissible_sizes, test_door_room_numbers_with_main_panel_greater_than_permissible_sizes, test_door_room_names_with_main_panel_greater_than_permissible_sizes)
    print(' \n')
    print('*'*216)


def double_equal_leaf_door_width(sample_code, minimum_double_equal_leaf_width, maximum_double_equal_leaf_width, sample_doors_with_double_equal_leaf = filtered_equal_leaf_doors, sample_door_numbers_for_doors_with_double_equal_leaf = filtered_equal_leaf_door_nums, sample_door_room_numbers_for_doors_with_double_equal_leaf = filtered_equal_leaf_door_room_nums, sample_door_room_names_for_doors_with_double_equal_leaf = filtered_equal_leaf_door_room_names, sample_door_Selections_for_doors_with_double_equal_leaf = filtered_equal_leaf_door_Selections):
    out.print_md('**{} CODE- MINIMUM CLEAR WIDTH- DOUBLE EQUAL LEAF DOORS**'.format(sample_code))
    sample_double_equal_leaf_doors_width = all_elements_with_type_parameter_AsDouble(sample_doors_with_double_equal_leaf, 'Leaf_Width')
    sample_double_equal_leaf_doors_width_convert = unit_conversion(sample_double_equal_leaf_doors_width )
    
    # Check minimum dimensions for double_equal leaf as per code
    sample_index_of_failure_double_equal_door_minimum_sizes = [i for i, x in enumerate(sample_double_equal_leaf_doors_width_convert) if x/2 < minimum_double_equal_leaf_width]
    # Check maximum dimensions for double_equal leaf as per code
    sample_index_of_failure_double_equal_door_maximum_sizes = [i for i, x in enumerate(sample_double_equal_leaf_doors_width_convert) if x/2 > maximum_double_equal_leaf_width]

    if (len(sample_index_of_failure_double_equal_door_minimum_sizes) == 0):
        print('\nDouble Leaf Door Width meet the minimum size of {} mm as per {} requirements. '.format(minimum_double_equal_leaf_width, sample_code))
    else:
        test_doors_with_double_equal_leaf_lesser_than_permissible_sizes = [sample_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_minimum_sizes]
        test_door_numbers_with_double_equal_leaf_lesser_than_permissible_sizes = [sample_door_numbers_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_minimum_sizes]
        test_door_room_numbers_with_double_equal_leaf_lesser_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_minimum_sizes]
        test_door_room_names_with_double_equal_leaf_lesser_than_permissible_sizes = [sample_door_room_names_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_minimum_sizes]  
        test_door_Selections_with_double_equal_leaf_lesser_than_permissible_sizes = [sample_door_Selections_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_minimum_sizes]
        print("\nThe Leaf Width of the following Double Equal Leaf Doors need to be updated to meet {} Code requirements,\nof each Leaf Size, i.e. greater than {} mm: -".format(sample_code, minimum_double_equal_leaf_width))
        output_for_doors_with_double_equal_leaf_lesser_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_double_equal_leaf_lesser_than_permissible_sizes, test_door_numbers_with_double_equal_leaf_lesser_than_permissible_sizes, test_door_room_numbers_with_double_equal_leaf_lesser_than_permissible_sizes, test_door_room_names_with_double_equal_leaf_lesser_than_permissible_sizes)
    print(' \n')
    print('*'*216) 
    
    out.print_md('**{} CODE- MAXIMUM CLEAR WIDTH- DOUBLE EQUAL LEAF DOORS**'.format(sample_code))


    if (len(sample_index_of_failure_double_equal_door_maximum_sizes) == 0):
        print('\Double Equal Leaf Door Width meet the maximum size of {} mm as per {} requirements. '.format(maximum_double_equal_leaf_width, sample_code))
    else:
        test_doors_with_double_equal_leaf_greater_than_permissible_sizes = [sample_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_maximum_sizes]
        test_door_numbers_with_double_equal_leaf_greater_than_permissible_sizes = [sample_door_numbers_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_maximum_sizes]
        test_door_room_numbers_with_double_equal_leaf_greater_than_permissible_sizes = [sample_door_room_numbers_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_maximum_sizes]
        test_door_room_names_with_double_equal_leaf_greater_than_permissible_sizes = [sample_door_room_names_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_maximum_sizes]  
        test_door_Selections_with_double_equal_leaf_greater_than_permissible_sizes = [sample_door_Selections_for_doors_with_double_equal_leaf[i] for i in sample_index_of_failure_double_equal_door_maximum_sizes]
        print("\nThe Leaf Width of the following Double Equal Leaf Doors need to be updated to meet {} Code requirements,\nof each Leaf Size, i.e. lesser than {} mm: -".format(sample_code, maximum_double_equal_leaf_width))
        output_for_doors_with_double_equal_leaf_greater_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_double_equal_leaf_greater_than_permissible_sizes, test_door_numbers_with_double_equal_leaf_greater_than_permissible_sizes, test_door_room_numbers_with_double_equal_leaf_greater_than_permissible_sizes, test_door_room_names_with_double_equal_leaf_greater_than_permissible_sizes)
    print(' \n')
    print('*'*216)    


def clear_height_for_doors(sample_code, minimum_height, sample_doors_to_check_clear_height = filtered_doors_with_clear_height, sample_door_nums_with_clear_height = filtered_door_nums_with_clear_height, sample_door_room_nums_with_clear_height = filtered_door_room_nums_with_clear_height, sample_door_room_names_with_clear_height = filtered_door_room_names_with_clear_height, sample_door_Selections_with_clear_height = filtered_door_Selections_with_clear_height):
    out.print_md('**{} CODE- MINIMUM CLEAR HEIGHT- FOR ALL DOORS**'.format(sample_code))
  
    sample_doors_height = all_elements_with_type_parameter_AsDouble(filtered_doors_with_clear_height, 'Leaf_Height')
    sample_doors_height_convert = unit_conversion(sample_doors_height)
    sample_index_of_failure_door_clear_height = [i for i, x in enumerate(sample_doors_height_convert) if x < minimum_height]

    if (len(sample_index_of_failure_door_clear_height) == 0):
        print("\nClear Height for Doors meet the Minimum Height of {} mm as per {} requirements. ".format(minimum_height, sample_code))
    else:
        test_doors_with_height_lesser_than_permissible_sizes = [sample_doors_to_check_clear_height[i] for i in sample_index_of_failure_door_clear_height]
        test_door_nums_with_height_lesser_than_permissible_sizes = [sample_door_nums_with_clear_height[i] for i in  sample_index_of_failure_door_clear_height]
        test_door_room_nums_with_height_lesser_than_permissible_sizes = [sample_door_room_nums_with_clear_height[i] for i in  sample_index_of_failure_door_clear_height]
        test_door_room_names_with_height_lesser_than_permissible_sizes = [sample_door_room_names_with_clear_height[i] for i in  sample_index_of_failure_door_clear_height]
        test_door_Selections_with_height_lesser_than_permissible_sizes = [sample_door_Selections_with_clear_height[i] for i in sample_index_of_failure_door_clear_height] 
        print('\nThe Leaf Height of the following Doors needs to be updated to meet {} Code requirements,\n of Leaf Height greater than {} mm :-'. format(sample_code, minimum_height))
        output_for_doors_with_height_lesser_than_permissible_sizes = output_statement_for_door_sizes(test_door_Selections_with_height_lesser_than_permissible_sizes, test_door_nums_with_height_lesser_than_permissible_sizes, test_door_room_nums_with_height_lesser_than_permissible_sizes, test_door_room_names_with_height_lesser_than_permissible_sizes)
    print(' \n')
    print('*'*216) 

#####################################################################################################################

from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 

userInputcategory = SelectFromList('Select Fire Standard for Door Review', ['00.NFPA','01.FRENCH CODE', '02.IBC', '03.BS-EN', '04.SBC', '05.NBC', '06.DCD'])
userInputcategory = str(userInputcategory)

#####################################################################################################################
     
if userInputcategory == '00.NFPA':
    
    NFPA_single_door_width = single_leaf_door_width('NFPA', 810, 1200)
    NFPA_unequal_door_width = unequal_leaf_door_width('NFPA', 450,810,810,1200)
    NFPA_double_equal_door_width = double_equal_leaf_door_width('NFPA', 810,1200)
    NFPA_door_clear_height = clear_height_for_doors('NFPA', 2050)
    
#####################################################################################################################
elif userInputcategory == '01.FRENCH CODE':

    French_code_single_door_width = single_leaf_door_width('FRENCH', 900, 1200)
    French_code_unequal_door_width = unequal_leaf_door_width('FRENCH', 450,813,900,1200)
    French_code_double_equal_door_width = double_equal_leaf_door_width('FRENCH', 900,1200)
    French_code_door_clear_height = clear_height_for_doors('FRENCH', 2050)
    
#####################################################################################################################   

elif userInputcategory == '02.IBC':
    
    IBC_code_single_door_width = single_leaf_door_width('IBC', 813, 1219)
    IBC_code_unequal_door_width = unequal_leaf_door_width('IBC', 450,813,813,1219)
    IBC_double_equal_door_width = double_equal_leaf_door_width('IBC', 813,1219)
    IBC_code_door_clear_height = clear_height_for_doors('IBC', 2032)
    
#####################################################################################################################

elif userInputcategory == '03.BS-EN':

    BS_EN_code_single_door_width = single_leaf_door_width('BS-EN', 850, 1200)
    BS_EN_code_unequal_door_width = unequal_leaf_door_width('BS-EN', 450,600,850,1200)
    BS_EN_double_equal_door_width = double_equal_leaf_door_width('BS-EN', 850,1200)
    BS_EN_code_door_clear_height = clear_height_for_doors('BS-EN', 2050)
    
#####################################################################################################################

elif userInputcategory == '04.SBC':
    
    SBC_code_single_door_width = single_leaf_door_width('SBC', 810, 1200)
    SBC_code_unequal_door_width = unequal_leaf_door_width('SBC', 450,813,810,1200)
    SBC_double_equal_door_width = double_equal_leaf_door_width('SBC', 810,1200)
    SBC_code_door_clear_height = clear_height_for_doors('SBC', 2100)
    
#####################################################################################################################

elif userInputcategory == '05.NBC':
    
    NBC_code_single_door_width = single_leaf_door_width('NBC', 1000, 1200)
    NBC_code_unequal_door_width = unequal_leaf_door_width('NBC', 450,1000,1000,1200)
    NBC_double_equal_door_width = double_equal_leaf_door_width('NBC', 1000,1200)
    NBC_code_door_clear_height = clear_height_for_doors('NBC', 2000)
    
#####################################################################################################################

elif userInputcategory == '06.DCD':
    
    DCD_code_single_door_width = single_leaf_door_width('DCD', 915, 1200)
    DCD_code_unequal_door_width = unequal_leaf_door_width('DCD', 450,810,915,1200)
    DCD_double_equal_door_width = double_equal_leaf_door_width('DCD', 915,1200)
    DCD_code_door_clear_height = clear_height_for_doors('DCD', 2050)
#####################################################################################################################

else:
    pass

#####################################################################################################################
