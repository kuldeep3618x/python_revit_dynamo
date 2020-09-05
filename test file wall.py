"""Assign Rating\nto Walls"""

__title__ = "Assign Rating\nto Walls"
__author__= "J K Roshan\nKerketta"

######################################################################

import time
start = time.time()

######################################################################
# pylint: disable=E0401,W0703,C0103
from collections import namedtuple

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from pyrevit.framework import List

import itertools
from itertools import chain
from itertools import islice

import operator
import math
####################################################################################################################

import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset, SpatialElement
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind, Element

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

app = __revit__.Application

####################################################################################################################

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIDocument, Selection



clr.AddReference('ProtoGeometry')                       
from Autodesk.DesignScript.Geometry import *            
        
clr.AddReference("RevitNodes")                          
import Revit    
clr.ImportExtensions(Revit.GeometryConversion)
                                        
clr.ImportExtensions(Revit.Elements)                    
clr.ImportExtensions(Revit.GeometryConversion)         
from Revit.Elements import *

clr.AddReference("RevitServices")                       
import RevitServices                                    
from RevitServices.Persistence import DocumentManager    

from pyrevit import HOST_APP
from pyrevit import revit, DB

import math
import itertools

#######################################

from math import pi as PI

from rpw import revit, DB
# from rpw.base import BaseObjectWrapper
# from rpw.db.element import Element
# from rpw.db.xyz import XYZ
# from rpw.utils.mixins import ByNameCollectMixin

###########################################################################################################

import rpw
from rpw import revit, db, ui, DB, UI
# from rpw.db.bounding_box import BoundingBox

from rpw.ui.forms import SelectFromList
from rpw.utils.coerce import to_category 


# from rpw.db.bounding_box import BoundingBox

####################################################################################################################
# Function to acquire all elements of category & get parameter value by name 

def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()

####################################################################################################################

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

def tolist(obj1):
    if hasattr(obj1, "__iter__"):
        return obj1
    else:
        return [obj1]


def PadLists(lists):
    len1 = len(lists[0])
    for i in xrange(1, len(lists)):
        len2 = len(lists[i])
        if len2 == len1:
            continue
        elif len2 > len1:
            lists[i] = lists[i][:len1]
        else:
            lists[i].extend(repeat(lists[i][-1], len1 - len2))
    return lists


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

levels_in_project = all_elements_of_category(BuiltInCategory.OST_Levels)
levels_in_project_name = [lvl.Name for lvl in levels_in_project]
# print(levels_in_project_name)

userInputLevel1 = SelectFromList('Select Level for Fire Rating Walls', [l for l in levels_in_project_name])
userInputLevel1 = str(userInputLevel1)

userInputLevel2 = SelectFromList('Select Level for Rooms', [l for l in levels_in_project_name])
userInputLevel2 = str(userInputLevel2)


levels = all_elements_of_category(BuiltInCategory.OST_Levels)

user_selected_level_bool1 = [lvl.Name == userInputLevel1 for lvl in levels]
filtered_level_index1 = [ l for l, index in enumerate(user_selected_level_bool1) if index]
filtered_level1 = [levels[i] for i in filtered_level_index1]
lvlId1 = filtered_level1[0].Id

filter1 = ElementLevelFilter(lvlId1)
wall_filtered_elems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WherePasses(filter1).WhereElementIsNotElementType().ToElements()
# print(wall_filtered_elems)
user_selected_level_bool2 = [lvl.Name == userInputLevel2 for lvl in levels]
filtered_level_index2 = [ l for l, index in enumerate(user_selected_level_bool2) if index]
filtered_level2 = [levels[i] for i in filtered_level_index2]
lvlId2 = filtered_level2[0].Id

filter2 = ElementLevelFilter(lvlId2)
room_filtered_elems = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WherePasses(filter2).WhereElementIsNotElementType().ToElements()


fire_rating_rooms = shared_parameter_values(room_filtered_elems, 'Fire_Rating')
# print(fire_rating_rooms)

Fire_rating_param_empty_or_None = [None, '', '0']

indices_of_rooms_with_fire_ratings = [i for i, x in enumerate(fire_rating_rooms) if x not in Fire_rating_param_empty_or_None]
# print(indices_of_rooms_with_missing_fire_ratings)
rooms_with_fire_rating  = [room_filtered_elems[i] for i in indices_of_rooms_with_fire_ratings]
room_nums_with_fire_rating = [r.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString() for r in rooms_with_fire_rating ]
room_names_with_fire_rating = [r.get_Parameter(BuiltInParameter.ROOM_NAME).AsString() for r in rooms_with_fire_rating ]
# print(rooms_with_fire_rating )

################################################################################################

solids = []
for g in rooms_with_fire_rating:
    geoms = g.get_Geometry(Options())
    tmplist =[]
    for g in geoms:
        tmplist.append(g)
    solids.append(tmplist)
    

print(solids)


################################################################################################

activeV = doc.ActiveView

wall_host = []
room_inst = []
room_inst_ID = []
wall_ID =  []
for w in wall_filtered_elems:
    wall_host.append(w)


superset = []

for h in wall_host:
    collection = List[ElementId](room_inst_ID)
    collector = FilteredElementCollector(doc, collection)
    
    a = h.BoundingBox[activeV]
    
    min_bound_val = a.Min
    max_bound_val = a.Max
   

    mod_min_pt = XYZ(min_bound_val.X + 0.0000000000001, min_bound_val.Y, min_bound_val.Z)
    mod_max_pt = XYZ(max_bound_val.X - 0.0000000000001, max_bound_val.Y, max_bound_val.Z)

# print(min_bound_val, max_bound_val, mod_min_pt, mod_max_pt)


    testBB = BoundingBoxXYZ()
    testBB.Min = mod_min_pt
    testBB.Max = mod_max_pt
    
    try:
        c = Outline(testBB.Min, testBB.Max)       
        d = BoundingBoxIntersectsFilter(c,float(0))
        e = collector.WherePasses(d).ToElements()
        setlist = []
        hostlist = []
        hostlist.append(h)
        setlist.append(e)
        all_lists = [hostlist,setlist]
        f = reduce(operator.add, all_lists)
        superset.append(f)
    except:
        superset.append('failed')

# print(superset) 




# #################################################################################################

# activeV = doc.ActiveView

# wall_host = []
# room_inst = []
# room_inst_ID = []
# wall_ID =  []
# for w in wall_filtered_elems:
#     wall_host.append(w)
# for r in rooms_with_fire_rating:
#     room_inst.append(r)
# for i in rooms_with_fire_rating:
#     room_inst_ID.append((i).Id)

# # print(room_inst_ID)

# superset = []

# for h in wall_host:
#     collection = List[ElementId](room_inst_ID)
#     collector = FilteredElementCollector(doc, collection)
    
#     a = h.BoundingBox[activeV]
    
#     min_bound_val = a.Min
#     max_bound_val = a.Max
   

#     mod_min_pt = XYZ(min_bound_val.X + 0.0000000000001, min_bound_val.Y, min_bound_val.Z)
#     mod_max_pt = XYZ(max_bound_val.X - 0.0000000000001, max_bound_val.Y, max_bound_val.Z)

# # print(min_bound_val, max_bound_val, mod_min_pt, mod_max_pt)

 
#     testBB = BoundingBoxXYZ()
#     testBB.Min = mod_min_pt
#     testBB.Max = mod_max_pt
    
#     try:
#         c = Outline(testBB.Min, testBB.Max)       
#         d = BoundingBoxIntersectsFilter(c,float(0))
#         e = collector.WherePasses(d).ToElements()
#         setlist = []
#         hostlist = []
#         hostlist.append(h)
#         setlist.append(e)
#         all_lists = [hostlist,setlist]
#         f = reduce(operator.add, all_lists)
#         superset.append(f)
#     except:
#         superset.append('failed')

# # print(superset)

# idx_of_non_failed_walls = [i for i, x in enumerate(superset) if x != 'failed']
# # print(idx_of_non_failed_walls)

# superset_filtered = [superset[i] for i in idx_of_non_failed_walls]
# # print(superset_filtered)

# def ExtractRooms(lst):
#     return[item[1] for item in lst]

# def ExtractWalls(lst):
#     return[item[0] for item in lst]

# room_filtered_list = ExtractRooms(superset_filtered)
# # print(room_filtered_list)

# empty_list_index = [i for i, x in enumerate(room_filtered_list) if not x]
# # print(empty_list_index)

# valid_list_index = [i for i, x in enumerate(room_filtered_list) if x ]
# # print(valid_list_index)

# room_sublist_with_valid_values = [room_filtered_list[i] for i in valid_list_index] 
# # print(room_sublist_with_valid_values)

# fire_rating_rooms_filtered = [shared_parameter_values(r, 'Fire_Rating') for r in room_sublist_with_valid_values]
# # print(fire_rating_rooms_filtered)

# sublist_room_fire_rating_to_num = [([int(x) for x in w]) for w in fire_rating_rooms_filtered]
# # print(sublist_room_fire_rating_to_num)

# max_fire_rating_for_room_list = [max(rating) for rating in sublist_room_fire_rating_to_num]
# # print(max_fire_rating_for_room_list)
# max_fire_rating_for_room_list_to_string = [str(x) for x in max_fire_rating_for_room_list]
# # print(max_fire_rating_for_room_list_to_string)

# wall_list = ExtractWalls(superset_filtered)
# wall_list_with_valid_values = [wall_list[i] for i in valid_list_index]
# # print(wall_list_with_valid_values)

# wall_fire_rating_from_rooms = set_parameter_by_name_transaction(wall_list_with_valid_values,'Fire_Rating', max_fire_rating_for_room_list_to_string)

# #####################################################################################################################

# print ('It took', time.time()-start, 'seconds.')

# print('*'*216)  

# ##################################################################################################################### 

































# #################################################################################################

# activeV = doc.ActiveView

# wall_host = []
# room_inst = []
# room_inst_ID = []
# wall_ID =  []
# for w in wall_filtered_elems:
#     wall_host.append(w)
# for r in rooms_with_fire_rating:
#     room_inst.append(r)
# for i in rooms_with_fire_rating:
#     room_inst_ID.append((i).Id)

# # print(room_inst_ID)

# superset = []

# for h in wall_host:
#     collection = List[ElementId](room_inst_ID)
#     collector = FilteredElementCollector(doc, collection)
    
#     a = h.BoundingBox[activeV]
    
#     min_bound_val = a.Min
#     max_bound_val = a.Max
   

#     mod_min_pt = XYZ(min_bound_val.X + 0.0000000000001, min_bound_val.Y, min_bound_val.Z)
#     mod_max_pt = XYZ(max_bound_val.X - 0.0000000000001, max_bound_val.Y, max_bound_val.Z)

# # print(min_bound_val, max_bound_val, mod_min_pt, mod_max_pt)

 
#     testBB = BoundingBoxXYZ()
#     testBB.Min = mod_min_pt
#     testBB.Max = mod_max_pt
    
#     try:
#         c = Outline(testBB.Min, testBB.Max)       
#         d = BoundingBoxIntersectsFilter(c,float(0))
#         e = collector.WherePasses(d).ToElements()
#         setlist = []
#         hostlist = []
#         hostlist.append(h)
#         setlist.append(e)
#         all_lists = [hostlist,setlist]
#         f = reduce(operator.add, all_lists)
#         superset.append(f)
#     except:
#         superset.append('failed')

# # print(superset)

# idx_of_non_failed_walls = [i for i, x in enumerate(superset) if x != 'failed']
# # print(idx_of_non_failed_walls)

# superset_filtered = [superset[i] for i in idx_of_non_failed_walls]
# # print(superset_filtered)

# def ExtractRooms(lst):
#     return[item[1] for item in lst]

# def ExtractWalls(lst):
#     return[item[0] for item in lst]

# room_filtered_list = ExtractRooms(superset_filtered)
# # print(room_filtered_list)

# empty_list_index = [i for i, x in enumerate(room_filtered_list) if not x]
# # print(empty_list_index)

# valid_list_index = [i for i, x in enumerate(room_filtered_list) if x ]
# # print(valid_list_index)

# room_sublist_with_valid_values = [room_filtered_list[i] for i in valid_list_index] 
# # print(room_sublist_with_valid_values)

# fire_rating_rooms_filtered = [shared_parameter_values(r, 'Fire_Rating') for r in room_sublist_with_valid_values]
# # print(fire_rating_rooms_filtered)

# sublist_room_fire_rating_to_num = [([int(x) for x in w]) for w in fire_rating_rooms_filtered]
# # print(sublist_room_fire_rating_to_num)

# max_fire_rating_for_room_list = [max(rating) for rating in sublist_room_fire_rating_to_num]
# # print(max_fire_rating_for_room_list)
# max_fire_rating_for_room_list_to_string = [str(x) for x in max_fire_rating_for_room_list]
# # print(max_fire_rating_for_room_list_to_string)

# wall_list = ExtractWalls(superset_filtered)
# wall_list_with_valid_values = [wall_list[i] for i in valid_list_index]
# # print(wall_list_with_valid_values)

# wall_fire_rating_from_rooms = set_parameter_by_name_transaction(wall_list_with_valid_values,'Fire_Rating', max_fire_rating_for_room_list_to_string)

# #####################################################################################################################

# print ('It took', time.time()-start, 'seconds.')

# print('*'*216)  

# ##################################################################################################################### 






# #################################################################################################

# activeV = doc.ActiveView

# wall_host = []
# room_inst = []
# room_inst_ID = []

# for w in wall_filtered_elems:
#     wall_host.append(w)
# for r in rooms_with_fire_rating:
#     room_inst.append(r)
# for i in rooms_with_fire_rating:
#     room_inst_ID.append((i).Id)
# # print(room_inst_ID)

# superset = []

# for h in wall_host:
#     collection = List[ElementId](room_inst_ID)
#     collector = FilteredElementCollector(doc, collection)
#     a = h.BoundingBox[activeV]
#     c = Outline(a.Min, a.Max)
#     d = BoundingBoxIntersectsFilter(c,float(0.01))
#     e = collector.WherePasses(d).ToElements()
#     setlist = []
#     hostlist = []
#     hostlist.append(h)
#     setlist.append(e)
#     all_lists = [hostlist,setlist]
#     c = reduce(operator.add, all_lists)
#     superset.append(c)

# def ExtractRooms(lst):
#     return[item[1] for item in lst]

# def ExtractWalls(lst):
#     return[item[0] for item in lst]

# room_filtered_list = ExtractRooms(superset)
# # print(room_filtered_list)

# empty_list_index = [i for i, x in enumerate(room_filtered_list) if not x]
# # print(empty_list_index)

# valid_list_index = [i for i, x in enumerate(room_filtered_list) if x ]
# # print(valid_list_index)

# room_sublist_with_valid_values = [room_filtered_list[i] for i in valid_list_index] 
# # print(room_sublist_with_valid_values)

# fire_rating_rooms_filtered = [shared_parameter_values(r, 'Fire_Rating') for r in room_sublist_with_valid_values]
# # print(fire_rating_rooms_filtered)

# sublist_room_fire_rating_to_num = [([int(x) for x in w]) for w in fire_rating_rooms_filtered]
# # print(sublist_room_fire_rating_to_num)

# max_fire_rating_for_room_list = [max(rating) for rating in sublist_room_fire_rating_to_num]
# # print(max_fire_rating_for_room_list)
# max_fire_rating_for_room_list_to_string = [str(x) for x in max_fire_rating_for_room_list]
# # print(max_fire_rating_for_room_list_to_string)

# wall_list = ExtractWalls(superset)
# wall_list_with_valid_values = [wall_list[i] for i in valid_list_index]
# # print(wall_list_with_valid_values)

# wall_fire_rating_from_rooms = set_parameter_by_name_transaction(wall_list_with_valid_values,'Fire_Rating', max_fire_rating_for_room_list_to_string)

# #####################################################################################################################

# print ('It took', time.time()-start, 'seconds.')

# print('*'*216)  

# ##################################################################################################################### 
