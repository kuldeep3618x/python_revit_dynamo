"""Assign Rating\nto Walls"""

__title__ = "Assign Rating\nto Walls"
__author__= "J K Roshan\nKerketta"

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

####################################################################################################################

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

from pyrevit import HOST_APP
from pyrevit import revit, DB

import math
import itertools

###########################################################################################################

import rpw
from rpw import revit, db, ui, DB, UI


####################################################################################################################
# Function to acquire all elements of category & get parameter value by name 

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()


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
# Extract Shared Parameter values, returns index of valid and None values

def elem_param_values_test(elems, parameter_name):
    elem_param_values = shared_parameter_values(elems,parameter_name)
    elem_param_empty_or_None = [None, '']
    elem_param_None_index = [i for i, x in enumerate(elem_param_values) if x in elem_param_empty_or_None]
    elem_param_valid_index = [ i for i, x in enumerate(elem_param_values) if x not in elem_param_empty_or_None]
    return (elem_param_values, elem_param_valid_index, elem_param_None_index)

####################################################################################################################

walls = all_elements_of_category(BuiltInCategory.OST_Walls)

rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
# print(rooms)

# room_name =  [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms]
# print(room_name)


fire_rating_rooms = shared_parameter_values(rooms, 'Fire_Rating')
print(fire_rating_rooms)

Fire_rating_param_empty_or_None = [None, '']

indices_of_rooms_with_missing_fire_ratings = [i for i, x in enumerate(fire_rating_rooms) if x not in Fire_rating_param_empty_or_None]
print(indices_of_rooms_with_missing_fire_ratings)
rooms_with_fire_rating  = [rooms[i] for i in indices_of_rooms_with_missing_fire_ratings]

room_nums_with_fire_rating = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in rooms_with_fire_rating ]
room_names_with_fire_rating = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms_with_fire_rating ]

print(room_nums_with_fire_rating, room_names_with_fire_rating)


options = SpatialElementBoundaryOptions()
options.SpatialElementBoundaryLocation = SpatialElementBoundaryLocation.Finish

# walls = []


segments = []
for r in rooms_with_fire_rating :
    segments = r.GetBoundarySegments(options)

print(segments)

wall_segments = []
for w in walls:
    wall_segments = w.GetBoundarySegments(options)
print(wall_segments)

# options = SpatialElementBoundaryOptions()
# options.SpatialElementBoundaryLocation = SpatialElementBoundaryLocation.Finish

# walls = []



# for r in rooms:
#     segments = r.GetBoundarySegments(options)
#     boundaries = []
#     for sl in segments:
#         for s in sl:
#             e = doc.GetElement(s.ElementId)
#             if isinstance(e,RevitLinkInstance):
#                 pass
#             else:
#                 boundaries.append(e)
#     walls.append(boundaries)
# # print(walls)
            
# wall_fire_rating = []         
# for w in walls:
#     temp = []
#     for e in w:
#         if e != None:
#             temp1 = []
#             # temp = e.Category.Id
#             for param in e.Parameters:
#                 if param.IsShared and param.Definition.Name == 'Fire_Rating':
#                     paramValue = e.get_Parameter(param.GUID)
#                     temp1.append(paramValue.AsString())
                    
            
#         else:
#             temp1 = 'fail'  
#         temp.append(temp1)      
#     wall_fire_rating.append(temp)
# print(wall_fire_rating)

     


####################################################################################################################

# Phase dependent Door properties

# def troom_froom_name_for_doors(doors_to_acquire = doors):
#     phases = doc.Phases
#     phase = phases[phases.Size - 1]
#     troom = []
#     froom = []

#     for d in doors_to_acquire:
#         temp = []
#         try:
#             temp = d.FromRoom[phase]
#             froom.append(temp)
#         except:
#             temp = 'fail'
#             froom.append(temp)
#         temp1 = []
#         try:
#             temp1 = d.ToRoom[phase]
#             troom.append(temp1)
#         except:
#             temp1 = 'fail'
#             troom.append(temp1)

#     filtered_from_rooms_index = [i for i, x in enumerate(froom) if x != None]
#     # print(filtered_from_rooms_index)
#     filtered_from_rooms = [froom[i] for i in filtered_from_rooms_index]
#     # print(filtered_from_rooms)
#     FromRoomName = [[r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in filtered_from_rooms]]
#     # print(FromRoomName)
#     iter_flat_FromRoomName_list =  itertools.chain.from_iterable
#     flat_FromRoomName_list = list(iter_flat_FromRoomName_list(FromRoomName))
#     # print(flat_FromRoomName_list)
#     froom_list_length = (len(froom))
#     from_room_name_list = ["None"] * froom_list_length
#     # print(from_room_name_list)
#     # print(len(from_room_name_list))
#     for (index, replacements) in zip(filtered_from_rooms_index,flat_FromRoomName_list):
#         from_room_name_list[index] = replacements
#     # print(from_room_name_list)


#     filtered_to_rooms_index = [i for i, x in enumerate(troom) if x != None]
#     filtered_to_rooms = [troom[i] for i in filtered_to_rooms_index]
#     # print(filtered_to_rooms)
#     ToRoomName = [[r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in filtered_to_rooms]]
#     # print(ToRoomName)
#     iter_flat_ToRoomName_list =  itertools.chain.from_iterable
#     flat_ToRoomName_list = list(iter_flat_ToRoomName_list(ToRoomName))
#     # print(flat_ToRoomName_list)
#     troom_list_length = (len(troom))
#     to_room_name_list = ["None"] * troom_list_length
#     # print(to_room_name_list)
#     # print(len(to_room_name_list))
#     for (index, replacements) in zip(filtered_to_rooms_index,flat_ToRoomName_list):
#         to_room_name_list[index] = replacements
#     # print(to_room_name_list)
#     return(to_room_name_list, from_room_name_list)

