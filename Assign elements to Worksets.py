"""Assign Elements Worksets"""

__title__ = "Assign to\nWorksets"
__author__= "JK Roshan"

####################################

import os.path as op
# pylint: disable=E0401,W0703,C0103
from collections import namedtuple
from pyrevit import revit, UI, DB
from pyrevit import forms
from pyrevit import script
from pyrevit import System
logger = script.get_logger()

######################################################
"""Acquire file name"""

central_path = revit.query.get_central_path(doc=revit.doc)
file_name = central_path.split("\\")
file_name_length = (len(file_name))
file_name_length = int(file_name_length)
revit_file_name = file_name[file_name_length - 1]
# print(revit_file_name)

#####################################################
import Autodesk.Revit.DB as DB
from  Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter, Transaction, TransactionGroup, Workset
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

#####################################################
#####################################################
def all_elements_of_category(category):
	return FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def get_parameter_value_by_name(element, parameterName):
	return element.LookupParameter(parameterName).AsValueString()

###############################################################################################################################################

# collect user created worksets

worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
# loop worksets
workset_names, workset_ids = [], []
for w in worksets:
    workset_names.append(w.Name)
    workset_ids.append(w.Id)
# print(workset_names)
# print(workset_ids)

#############################################################################################
# All Doors
#############################################################################################

# All Elements Of Doors Category.
doors = all_elements_of_category(BuiltInCategory.OST_Doors)
   
index_of_door_workset = []
index_of_door_workset = workset_names.index("ARX_Door")
door_workset_id = workset_ids[index_of_door_workset].IntegerValue

# START TRANSACTION

door_pass_list = list()
door_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for d in doors:
	try:
		door_param = d.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		door_param.Set(door_workset_id)
		door_pass_list.append(d)
	except:
		door_fail_list.append(d)
t.Commit()

###################################################################################################
# All Railings
##################################################################################################

collector_of_railings = FilteredElementCollector(doc)
railings = collector_of_railings.OfCategory(BuiltInCategory.OST_StairsRailing).WhereElementIsNotElementType().ToElements()
# print(railings)
 
railing_Family_Names = []
for r in railings:
    railing_Family_Names.append(r.Name)
# print(railing_Family_Names)

index_of_railing_workset = []
index_of_railing_workset = workset_names.index("ARX_Railing")
railing_workset_id = workset_ids[index_of_railing_workset].IntegerValue

# START TRANSACTION

railing_pass_list = list()
railing_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for r in railings:
	try:
		railing_param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		railing_param.Set(railing_workset_id)
		railing_pass_list.append(r)
	except:
		railing_fail_list.append(r)
t.Commit()

###################################################################################################
# All Groups
###################################################################################################

collector_of_groups = FilteredElementCollector(doc)
groups = collector_of_groups.OfCategory(BuiltInCategory.OST_IOSModelGroups).WhereElementIsNotElementType().ToElements()

# Name of groups    
group_Names = []
for gp in groups:
    group_Names.append(gp.Name)
# print(group_Names)

index_of_group_workset = []
index_of_group_workset = workset_names.index("ARX_Group")
group_workset_id = workset_ids[index_of_group_workset].IntegerValue

# START TRANSACTION

group_pass_list = list()
group_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for gp in groups:
	try:
		group_param = gp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		group_param.Set(group_workset_id)
		group_pass_list.append(gp)
	except:
		group_fail_list.append(gp)
t.Commit()
 
###################################################################################################
# All Levels
###################################################################################################

levels = all_elements_of_category(BuiltInCategory.OST_Levels)
# print(levels)
 
# Name of Levels
level_Names = []
for l in levels:
    level_Names.append(l.Name)
# print(level_Names)    

index_of_levels = []
index_of_levels = workset_names.index("Shared Levels and Grids")
levels_workset_id = workset_ids[index_of_levels].IntegerValue

# START TRANSACTION

levels_pass_list = list()
levels_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for l in levels:
	try:
		Levels_param = l.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		Levels_param.Set(levels_workset_id)
		levels_pass_list.append(l)
	except:
		levels_fail_list.append(l)
t.Commit()

###################################################################################################
# All Grids
###################################################################################################

grids = all_elements_of_category(BuiltInCategory.OST_Grids)
# print(grids)
 
# Name of Grids
grid_Names = []
for g in grids:
    grid_Names.append(g.Name)
# print(grid_Names)    

index_of_grids = []
index_of_grids = workset_names.index("Shared Levels and Grids")
grids_workset_id = workset_ids[index_of_grids].IntegerValue

# START TRANSACTION

grids_pass_list = list()
grids_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for g in grids:
	try:
		Grids_param = g.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		Grids_param.Set(grids_workset_id)
		grids_pass_list.append(g)
	except:
		grids_fail_list.append(g)
t.Commit()

###################################################################################################
# All Scope Boxes
###################################################################################################

collector_of_scope_boxes = FilteredElementCollector(doc)
scope_boxes = collector_of_scope_boxes.OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
# print(scope_boxes)

scope_box_Names = []
for sb in scope_boxes:
    scope_box_Names.append(sb.Name)
# print(scope_box_Names) 

index_of_scope_boxes = []
index_of_scope_boxes = workset_names.index("ARX_Scope Boxes")
scope_boxes_workset_id = workset_ids[index_of_scope_boxes].IntegerValue

# START TRANSACTION

scope_boxes_pass_list = list()
scope_boxes_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for sb in scope_boxes:
	try:
		scope_boxes_param = sb.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		scope_boxes_param.Set(scope_boxes_workset_id)
		scope_boxes_pass_list.append(sb)
	except:
		scope_boxes_fail_list.append(sb)
t.Commit()

#################################################################################
# All Room Separators
#################################################################################

room_separators = all_elements_of_category(BuiltInCategory.OST_RoomSeparationLines)
# print(room_separators)

index_of_room_separators = []
index_of_room_separators = workset_names.index("ARX_Internal")
room_separators_workset_id = workset_ids[index_of_room_separators].IntegerValue
# print(room_separators_workset_id)

# START TRANSACTION

room_separators_pass_list = list()
room_separators_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for r in room_separators:
	try:
		room_separators_param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		room_separators_param.Set(room_separators_workset_id)
		room_separators_pass_list.append(r)
	except:
		room_separators_fail_list.append(r)
t.Commit()

#################################################################################
# All Rooms
#################################################################################

rooms = all_elements_of_category(BuiltInCategory.OST_Rooms)
   
index_of_room_workset = []
index_of_room_workset = workset_names.index("ARX_Internal")
room_workset_id = workset_ids[index_of_room_workset].IntegerValue

# START TRANSACTION

room_pass_list = list()
room_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for r in rooms:
	try:
		room_param = r.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		room_param.Set(room_workset_id)
		room_pass_list.append(r)
	except:
		room_fail_list.append(r)
t.Commit()

#################################################################################
# All Ceilings
#################################################################################

ceilings = all_elements_of_category(BuiltInCategory.OST_Ceilings)
   
index_of_ceiling_workset = []
index_of_ceiling_workset = workset_names.index("AIX_Ceiling")
ceiling_workset_id = workset_ids[index_of_ceiling_workset].IntegerValue

# START TRANSACTION

ceiling_pass_list = list()
ceiling_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for c in ceilings:
	try:
		ceiling_param = c.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ceiling_param.Set(ceiling_workset_id)
		ceiling_pass_list.append(c)
	except:
		ceiling_fail_list.append(c)
t.Commit()

#################################################################################
# Furniture
#################################################################################

furniture = all_elements_of_category(BuiltInCategory.OST_Furniture)
   
index_of_furniture_workset = []
index_of_furniture_workset = workset_names.index("AIX_Furniture")
furniture_workset_id = workset_ids[index_of_furniture_workset].IntegerValue

# START TRANSACTION

furniture_pass_list = list()
furniture_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ca in furniture:
	try:
		furniture_param = ca.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		furniture_param.Set(furniture_workset_id)
		furniture_pass_list.append(ca)
	except:
		furniture_fail_list.append(ca)
t.Commit()

#################################################################################
# All Casework
#################################################################################

casework = all_elements_of_category(BuiltInCategory.OST_Casework)
   
index_of_casework_workset = []
index_of_casework_workset = workset_names.index("AIX_Furniture")
casework_workset_id = workset_ids[index_of_casework_workset].IntegerValue

# START TRANSACTION

casework_pass_list = list()
casework_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ca in casework:
	try:
		casework_param = ca.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		casework_param.Set(casework_workset_id)
		casework_pass_list.append(ca)
	except:
		casework_fail_list.append(ca)
t.Commit()

#################################################################################
# Plumbing Fixtures
#################################################################################

plumbing_fixtures = all_elements_of_category(BuiltInCategory.OST_PlumbingFixtures)
   
index_of_plumbing_fixtures_workset = []
index_of_plumbing_fixtures_workset = workset_names.index("AIX_Plumbing Fixtures")
plumbing_fixtures_workset_id = workset_ids[index_of_plumbing_fixtures_workset].IntegerValue

# START TRANSACTION

plumbing_fixtures_pass_list = list()
plumbing_fixtures_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for pl in plumbing_fixtures:
	try:
		plumbing_fixtures_param = pl.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		plumbing_fixtures_param.Set(plumbing_fixtures_workset_id)
		plumbing_fixtures_pass_list.append(pl)
	except:
		plumbing_fixtures_fail_list.append(pl)
t.Commit()

#################################################################################
# All Stair Finishes
#################################################################################

stair_finishes = all_elements_of_category(BuiltInCategory.OST_Stairs)
   
index_of_stair_finish_workset = []
index_of_stair_finish_workset = workset_names.index("ARX_Finishes")
stair_finish_workset_id = workset_ids[index_of_stair_finish_workset].IntegerValue

# START TRANSACTION

stair_finish_pass_list = list()
stair_finish_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for st in stair_finishes:
	try:
		stair_finish_param = st.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		stair_finish_param.Set(stair_finish_workset_id)
		stair_finish_pass_list.append(st)
	except:
		stair_finish_fail_list.append(st)
t.Commit()

#################################################################################
#All Flooring
#################################################################################

flooring = all_elements_of_category(BuiltInCategory.OST_Floors)
# print(flooring)

flooring_Family_Names = []
for sp in flooring:
    flooring_Family_Names.append(sp.Name)
# print(flooring_Family_Names)

#################################################################################
# Flooring - Screed

index_of_flooring = [i for i, sp in enumerate(flooring_Family_Names) if 'Screed' in sp]
# print(index_of_flooring)

arch_flooring_list = [flooring[i] for i in index_of_flooring]
arch_flooring_list = list(arch_flooring_list)
   
index_of_arch_flooring_workset = []
index_of_arch_flooring_workset = workset_names.index("AIX_Floors")
arch_flooring_workset_id = workset_ids[index_of_arch_flooring_workset].IntegerValue

# START TRANSACTION

arch_flooring_pass_list = list()
arch_flooring_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for asp in arch_flooring_list:
	try:
		arch_flooring_param = asp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		arch_flooring_param.Set(arch_flooring_workset_id)
		arch_flooring_pass_list.append(asp)
	except:
		arch_flooring_fail_list.append(asp)
t.Commit()


####################################################################################
# Flooring - Not Screed

index_of_flooring = [i for i, sp in enumerate(flooring_Family_Names) if 'Screed' not in sp]
# print(index_of_flooring)

interior_flooring_list = [flooring[i] for i in index_of_flooring]
interior_flooring_list = list(interior_flooring_list)
   
index_of_interior_flooring_workset = []
index_of_interior_flooring_workset = workset_names.index("AIX_Floors")
interior_flooring_workset_id = workset_ids[index_of_interior_flooring_workset].IntegerValue

# START TRANSACTION

interior_flooring_pass_list = list()
interior_flooring_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for asp in interior_flooring_list:
	try:
		interior_flooring_param = asp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		interior_flooring_param.Set(interior_flooring_workset_id)
		interior_flooring_pass_list.append(asp)
	except:
		interior_flooring_fail_list.append(asp)
t.Commit()

###################################################################################################
#All Generic Models
###################################################################################################

generic_models = all_elements_of_category(BuiltInCategory.OST_GenericModel)  
# print(generic_models)
    
generic_model_Family_Names = []
for gm in generic_models:
    generic_model_Family_Names.append(gm.Name)
# print(generic_model_Family_Names)

###################################################################################################
# Generic Models- Access Panels

index_of_access_panel = [i for i, ap in enumerate(generic_model_Family_Names) if 'Access' in ap]
# print(index_of_access_panel)

Access_Panel_list = [generic_models[i] for i in index_of_access_panel]
Access_Panel_list = list(Access_Panel_list)
   
index_of_access_panel_workset = []
index_of_access_panel_workset = workset_names.index("ARX_Door")
access_panel_workset_id = workset_ids[index_of_access_panel_workset].IntegerValue

# START TRANSACTION

access_panel_pass_list = list()
access_panel_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ap in Access_Panel_list:
	try:
		access_panel_param = ap.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		access_panel_param.Set(access_panel_workset_id)
		access_panel_pass_list.append(ap)
	except:
		access_panel_fail_list.append(ap)
t.Commit()

###################################################################################################
# Generic Models- Access Panels Additional

index_of_access_panel = [i for i, ap in enumerate(generic_model_Family_Names) if 'AP' in ap]
# print(index_of_access_panel)

Access_Panel_list = [generic_models[i] for i in index_of_access_panel]
Access_Panel_list = list(Access_Panel_list)
   
index_of_access_panel_workset = []
index_of_access_panel_workset = workset_names.index("ARX_Door")
access_panel_workset_id = workset_ids[index_of_access_panel_workset].IntegerValue

# START TRANSACTION

access_panel_pass_list = list()
access_panel_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ap in Access_Panel_list:
	try:
		access_panel_param = ap.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		access_panel_param.Set(access_panel_workset_id)
		access_panel_pass_list.append(ap)
	except:
		access_panel_fail_list.append(ap)
t.Commit()

###################################################################################################
# Generic Models- Floor Transitions

index_of_floor_transition = [i for i, ft in enumerate(generic_model_Family_Names) if 'FLR' in ft]
# print(index_of_floor_transition)

floor_tranisiton_list = [generic_models[i] for i in index_of_floor_transition]
floor_tranisiton_list = list(floor_tranisiton_list)
   
index_of_floor_tranisiton_workset = []
index_of_floor_tranisiton_workset = workset_names.index("AIX_Floors")
floor_tranisiton_workset_id = workset_ids[index_of_floor_tranisiton_workset].IntegerValue

# START TRANSACTION

floor_tranisiton_pass_list = list()
floor_tranisiton_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ft in floor_tranisiton_list:
	try:
		floor_tranisiton_param = ft.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		floor_tranisiton_param.Set(floor_tranisiton_workset_id)
		floor_tranisiton_pass_list.append(ft)
	except:
		floor_tranisiton_fail_list.append(ft)
t.Commit()

###################################################################################################
# Generic Models- Column Cladding

index_of_column_cladding = [i for i, cl in enumerate(generic_model_Family_Names) if 'Clad' in cl]
# print(index_of_column_cladding)

column_cladding_list = [generic_models[i] for i in index_of_column_cladding]
column_cladding_list = list(column_cladding_list)
   
index_of_column_cladding_workset = []
index_of_column_cladding_workset = workset_names.index("AIX_Wall Finish")
column_cladding_workset_id = workset_ids[index_of_column_cladding_workset].IntegerValue

# START TRANSACTION

column_cladding_pass_list = list()
column_cladding_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for cl in column_cladding_list:
	try:
		column_cladding_param = cl.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		column_cladding_param.Set(column_cladding_workset_id)
		column_cladding_pass_list.append(cl)
	except:
		column_cladding_fail_list.append(cl)
t.Commit()

###################################################################################################
# Generic Models- Corner Guard

index_of_corner_guard = [i for i, cr in enumerate(generic_model_Family_Names) if 'x' in cr]
# print(index_of_corner_guard)

corner_guard_list = [generic_models[i] for i in index_of_corner_guard]
corner_guard_list = list(corner_guard_list)
   
index_of_corner_guard_workset = []
index_of_corner_guard_workset = workset_names.index("AIX_Wall Finish")
corner_guard_workset_id = workset_ids[index_of_corner_guard_workset].IntegerValue

# START TRANSACTION

corner_guard_pass_list = list()
corner_guard_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for cr in corner_guard_list:
	try:
		corner_guard_param = cr.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		corner_guard_param.Set(corner_guard_workset_id)
		corner_guard_pass_list.append(cr)
	except:
		corner_guard_fail_list.append(cr)
t.Commit()



###################################################################################################
# Generic Models- Stair Post

index_of_stair_post = [i for i, sp in enumerate(generic_model_Family_Names) if 'Post' in sp]
# print(index_of_stair_post)

stair_post_list = [generic_models[i] for i in index_of_stair_post]
stair_post_list = list(stair_post_list)

index_of_stair_post_workset = []
index_of_stair_post_workset = workset_names.index("AIX_Wall Finish")
stair_post_workset_id = workset_ids[index_of_stair_post_workset].IntegerValue

# START TRANSACTION

stair_post_pass_list = list()
stair_post_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for sp in stair_post_list:
	try:
		stair_post_param = sp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		stair_post_param.Set(stair_post_workset_id)
		stair_post_pass_list.append(sp)
	except:
		stair_post_fail_list.append(sp)
t.Commit()

###################################################################################################
# Generic Models- Stair Post(Circular)

index_of_stair_circular_post = [i for i, sp in enumerate(generic_model_Family_Names) if 'POST' in sp]
# print(index_of_stair_circular_post)

stair_circular_post_list = [generic_models[i] for i in index_of_stair_circular_post]
stair_circular_post_list = list(stair_circular_post_list)

index_of_stair_circular_post_workset = []
index_of_stair_circular_post_workset = workset_names.index("AIX_Wall Finish")
stair_circular_post_workset_id = workset_ids[index_of_stair_circular_post_workset].IntegerValue

# START TRANSACTION

stair_circular_post_pass_list = list()
stair_circular_post_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for sp in stair_circular_post_list:
	try:
		stair_circular_post_param = sp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		stair_circular_post_param.Set(stair_circular_post_workset_id)
		stair_circular_post_pass_list.append(sp)
	except:
		stair_circular_post_fail_list.append(sp)
t.Commit()

###################################################################################################
# Generic Models- Generic Ceilings

index_of_generic_ceiling = [i for i, gcl in enumerate(generic_model_Family_Names) if 'CLG' in gcl]
# print(index_of_generic_ceiling)

generic_ceiling_list = [generic_models[i] for i in index_of_generic_ceiling]
generic_ceiling_list = list(generic_ceiling_list)

   
index_of_generic_ceiling_workset = []
index_of_generic_ceiling_workset = workset_names.index("AIX_Ceiling")
generic_ceiling_workset_id = workset_ids[index_of_generic_ceiling_workset].IntegerValue

# START TRANSACTION

generic_ceiling_pass_list = list()
generic_ceiling_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for gcl in generic_ceiling_list:
	try:
		generic_ceiling_param = gcl.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		generic_ceiling_param.Set(generic_ceiling_workset_id)
		generic_ceiling_pass_list.append(gcl)
	except:
		generic_ceiling_fail_list.append(gcl)
t.Commit()

###################################################################################################
# Generic Models- Wall Openings

index_of_wall_openings = [i for i, wop in enumerate(generic_model_Family_Names) if 'OPNG' in wop]
# print(index_of_wall_openings)

wall_opening_list = [generic_models[i] for i in index_of_wall_openings]
wall_opening_list = list(wall_opening_list)
   
index_of_wall_opening_workset = []
index_of_wall_opening_workset = workset_names.index("Shared Levels and Grids")
wall_opening_workset_id = workset_ids[index_of_wall_opening_workset].IntegerValue

# START TRANSACTION

wall_opening_pass_list = list()
wall_opening_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wop in wall_opening_list:
	try:
		wall_opening_param = wop.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		wall_opening_param.Set(wall_opening_workset_id)
		wall_opening_pass_list.append(wop)
	except:
		wall_opening_fail_list.append(wop)
t.Commit()

###################################################################################################
# Generic Models- Wall Cutouts

index_of_wall_cutouts= [i for i, wc in enumerate(generic_model_Family_Names) if 'Cutout' in wc]
# print(index_of_wall_cutouts)

wall_cutout_list = [generic_models[i] for i in index_of_wall_cutouts]
wall_cutout_list = list(wall_cutout_list)
   
index_of_wall_cutout_workset = []
index_of_wall_cutout_workset = workset_names.index("Shared Levels and Grids")
wall_cutout_workset_id = workset_ids[index_of_wall_cutout_workset].IntegerValue

# START TRANSACTION

wall_cutout_pass_list = list()
wall_cutout_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wc in wall_cutout_list:
	try:
		wall_cutout_param = wc.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		wall_cutout_param.Set(wall_cutout_workset_id)
		wall_cutout_pass_list.append(wc)
	except:
		wall_cutout_fail_list.append(wc)
t.Commit()

###################################################################################################
# Generic Models- Additional Wall Cutouts (Rectangular)

index_of_wall_cutouts_rectangular = [i for i, wc in enumerate(generic_model_Family_Names) if 'WallRectCutHole' in wc]
# print(index_of_wall_cutouts)

wall_cutouts_rectangular_list = [generic_models[i] for i in index_of_wall_cutouts_rectangular]
wall_cutouts_rectangular_list = list(wall_cutouts_rectangular_list)
   
index_of_wall_cutouts_rectangular_workset = []
index_of_wall_cutouts_rectangular_workset = workset_names.index("Shared Levels and Grids")
wall_cutouts_rectangular_workset_id = workset_ids[index_of_wall_cutouts_rectangular_workset].IntegerValue

# START TRANSACTION

wall_cutouts_rectangular_pass_list = list()
wall_cutouts_rectangular_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wc in wall_cutouts_rectangular_list:
	try:
		wall_cutouts_rectangular_param = wc.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		wall_cutouts_rectangular_param.Set(wall_cutouts_rectangular_workset_id)
		wall_cutouts_rectangular_pass_list.append(wc)
	except:
		wall_cutouts_rectangular_fail_list.append(wc)
t.Commit()

###################################################################################################
# Generic Models- Additional Wall Cutouts (Circular)

index_of_wall_cutouts_circular = [i for i, wc in enumerate(generic_model_Family_Names) if 'WallCircCutHole' in wc]
# print(index_of_wall_cutouts)

wall_cutouts_circular_list = [generic_models[i] for i in index_of_wall_cutouts_circular]
wall_cutouts_circulars_list = list(wall_cutouts_circular_list)
   
index_of_wall_cutouts_circular_workset = []
index_of_wall_cutouts_circular_workset = workset_names.index("Shared Levels and Grids")
wall_cutouts_circular_workset_id = workset_ids[index_of_wall_cutouts_circular_workset].IntegerValue

# START TRANSACTION

wall_cutouts_circular_pass_list = list()
wall_cutouts_circular_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wc in wall_cutouts_circular_list:
	try:
		wall_cutouts_circular_param = wc.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		wall_cutouts_circular_param.Set(wall_cutouts_circular_workset_id)
		wall_cutouts_circular_pass_list.append(wc)
	except:
		wall_cutouts_circular_fail_list.append(wc)
t.Commit()

###################################################################################################
# Generic Models- Wall Voids

index_of_wall_voids= [i for i, wv in enumerate(generic_model_Family_Names) if 'Void' in wv]
# print(index_of_wall_voids)

wall_void_list = [generic_models[i] for i in index_of_wall_voids]
wall_void_list = list(wall_void_list)
   
index_of_wall_void_workset = []
index_of_wall_void_workset = workset_names.index("Shared Levels and Grids")
wall_void_workset_id = workset_ids[index_of_wall_void_workset].IntegerValue

# START TRANSACTION

wall_void_pass_list = list()
wall_void_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wv in wall_void_list:
	try:
		wall_void_param = wv.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		wall_void_param.Set(wall_void_workset_id)
		wall_void_pass_list.append(wv)
	except:
		wall_void_fail_list.append(wv)
t.Commit()

###################################################################################################
# Generic Models- Counter

index_of_counter_interior= [i for i, wv in enumerate(generic_model_Family_Names) if 'COUNTER' in wv]
# print(index_of_counter_interior)

counter_interior_list = [generic_models[i] for i in index_of_counter_interior]
counter_interior_list = list(counter_interior_list)
   
index_of_counter_interior_workset = []
index_of_counter_interior_workset = workset_names.index("AIX_Furniture")
counter_interior_workset_id = workset_ids[index_of_counter_interior_workset].IntegerValue

# START TRANSACTION

counter_interior_pass_list = list()
counter_interior_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wv in counter_interior_list:
	try:
		counter_interior_param = wv.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		counter_interior_param.Set(counter_interior_workset_id)
		counter_interior_pass_list.append(wv)
	except:
		counter_interior_fail_list.append(wv)
t.Commit()



##################################################################################################
#All Speciality Equipment
##################################################################################################

speciality_equipment = all_elements_of_category(BuiltInCategory.OST_SpecialityEquipment)
# print(speciality_equipment)

speciality_equipment_Family_Names = []
for sp in speciality_equipment:
    speciality_equipment_Family_Names.append(sp.Name)
# print(speciality_equipment_Family_Names)

###################################################################################################
# Speciality Equipment- Security Systems, Elevators

index_of_speciality_equipment = [i for i, sp in enumerate(speciality_equipment_Family_Names) if 'Type' in sp]
# print(index_of_speciality_equipment)

arch_speciality_equipment_list = [speciality_equipment[i] for i in index_of_speciality_equipment]
arch_speciality_equipment_list = list(arch_speciality_equipment_list)
   
index_of_arch_speciality_equipment_workset = []
index_of_arch_speciality_equipment_workset = workset_names.index("ARX_Specialty Equipment")
arch_speciality_equipment_workset_id = workset_ids[index_of_arch_speciality_equipment_workset].IntegerValue

# START TRANSACTION

arch_speciality_equipment_pass_list = list()
arch_speciality_equipment_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for asp in arch_speciality_equipment_list:
	try:
		arch_speciality_equipment_param = asp.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		arch_speciality_equipment_param.Set(arch_speciality_equipment_workset_id)
		arch_speciality_equipment_pass_list.append(asp)
	except:
		arch_speciality_equipment_fail_list.append(asp)
t.Commit()

###################################################################################################
# Speciality Equipment- Escalators

index_of_escalators = [i for i, es in enumerate(speciality_equipment_Family_Names) if 'Deg' in es]

escalators_list = [speciality_equipment[i] for i in index_of_escalators]
escalators_list = list(escalators_list)
   
index_of_escalators_workset = []
index_of_escalators_workset = workset_names.index("ARX_Specialty Equipment")
escalators_workset_id = workset_ids[index_of_escalators_workset].IntegerValue

# START TRANSACTION

escalators_pass_list = list()
escalators_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for esc in escalators_list:
	try:
		escalators_param = esc.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		escalators_param.Set(escalators_workset_id)
		escalators_pass_list.append(esc)
	except:
		escalators_fail_list.append(esc)
t.Commit()

###################################################################################################
# Speciality Equipment- Travelators

index_of_travelators = [i for i, tl in enumerate(speciality_equipment_Family_Names) if 'Travel' in tl]
# print(index_of_travelators)

travelators_list = [speciality_equipment[i] for i in index_of_travelators]
travelators_list = list(travelators_list)
   
index_of_travelators_workset = []
index_of_travelators_workset = workset_names.index("ARX_Specialty Equipment")
travelators_workset_id = workset_ids[index_of_travelators_workset].IntegerValue

# START TRANSACTION

travelators_pass_list = list()
travelators_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for tr in travelators_list:
	try:
		travelators_param = tr.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		travelators_param.Set(travelators_workset_id)
		travelators_pass_list.append(tr)
	except:
		travelators_fail_list.append(tr)
t.Commit()

###################################################################################################
# Speciality Equipment- Robe Hook

index_of_robe_hook = [i for i, th in enumerate(speciality_equipment_Family_Names) if 'hook' in th]
# print(index_of_robe_hook)

robe_hook_list = [speciality_equipment[i] for i in index_of_robe_hook]
robe_hook_list = list(robe_hook_list)
   
index_of_robe_hook_workset = []
index_of_robe_hook_workset = workset_names.index("AIX_Plumbing Fixtures")
robe_hook_workset_id = workset_ids[index_of_robe_hook_workset].IntegerValue

# START TRANSACTION

robe_hook_pass_list = list()
robe_hook_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for th in robe_hook_list:
	try:
		robe_hook_param = th.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		robe_hook_param.Set(robe_hook_workset_id)
		robe_hook_pass_list.append(th)
	except:
		robe_hook_fail_list.append(th)
t.Commit()

###################################################################################################
# Speciality Equipment- Double Robe Hook

index_of_double_robe_hook = [i for i, th in enumerate(speciality_equipment_Family_Names) if 'TP' in th]
# print(index_of_double_robe_hook)

double_robe_hook_list = [speciality_equipment[i] for i in index_of_double_robe_hook]
double_robe_hook_list = list(double_robe_hook_list)
   
index_of_double_robe_hook_workset = []
index_of_double_robe_hook_workset = workset_names.index("AIX_Plumbing Fixtures")
double_robe_hook_workset_id = workset_ids[index_of_double_robe_hook_workset].IntegerValue

# START TRANSACTION

double_robe_hook_pass_list = list()
double_robe_hook_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for th in double_robe_hook_list:
	try:
		double_robe_hook_param = th.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		double_robe_hook_param.Set(double_robe_hook_workset_id)
		double_robe_hook_pass_list.append(th)
	except:
		double_robe_hook_fail_list.append(th)
t.Commit()

###################################################################################################
# Speciality Equipment- Towel Pin, Robe Hook

index_of_towel_hangars = [i for i, th in enumerate(speciality_equipment_Family_Names) if 'ARC' in th]
# print(index_of_towel_hangars)

towel_hangars_list = [speciality_equipment[i] for i in index_of_towel_hangars]
towel_hangars_list = list(towel_hangars_list)
   
index_of_towel_hangars_workset = []
index_of_towel_hangars_workset = workset_names.index("AIX_Plumbing Fixtures")
towel_hangars_workset_id = workset_ids[index_of_towel_hangars_workset].IntegerValue

# START TRANSACTION

towel_hangars_pass_list = list()
towel_hangars_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for th in towel_hangars_list:
	try:
		towel_hangars_param = th.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		towel_hangars_param.Set(towel_hangars_workset_id)
		towel_hangars_pass_list.append(th)
	except:
		towel_hangars_fail_list.append(th)
t.Commit()

###################################################################################################
# Speciality Equipment- Grab bar

index_of_grab_bars = [i for i, gb in enumerate(speciality_equipment_Family_Names) if 'Grab' in gb]
# print(index_of_grab_bars)

grab_bars_list = [speciality_equipment[i] for i in index_of_grab_bars]
grab_bars_list = list(grab_bars_list)
   
index_of_grab_bars_workset = []
index_of_grab_bars_workset = workset_names.index("AIX_Plumbing Fixtures")
grab_bars_workset_id = workset_ids[index_of_grab_bars_workset].IntegerValue

# START TRANSACTION

grab_bars_pass_list = list()
grab_bars_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for gb in grab_bars_list:
	try:
		grab_bars_param = gb.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		grab_bars_param.Set(grab_bars_workset_id)
		grab_bars_pass_list.append(gb)
	except:
		grab_bars_fail_list.append(gb)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Additional Grab bar 

index_of_additional_grab_bars = [i for i, gb in enumerate(speciality_equipment_Family_Names) if 'GB' in gb]
# print(index_of_additional_grab_bars)

additional_grab_bars_list = [speciality_equipment[i] for i in index_of_additional_grab_bars]
additional_grab_bars_list = list(additional_grab_bars_list)
   
index_of_additional_grab_bars_workset = []
index_of_additional_grab_bars_workset = workset_names.index("AIX_Plumbing Fixtures")
additional_grab_bars_workset_id = workset_ids[index_of_additional_grab_bars_workset].IntegerValue

# START TRANSACTION

additional_grab_bars_pass_list = list()
additional_grab_bars_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for gb in additional_grab_bars_list:
	try:
		additional_grab_bars_param = gb.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		additional_grab_bars_param.Set(additional_grab_bars_workset_id)
		additional_grab_bars_pass_list.append(gb)
	except:
		additional_grab_bars_fail_list.append(gb)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Mirror

index_of_Mirrors = [i for i, m in enumerate(speciality_equipment_Family_Names) if '14' in m]
# print(index_of_Mirrors)

Mirrors_list = [speciality_equipment[i] for i in index_of_Mirrors]
Mirrors_list = list(Mirrors_list)
   
index_of_Mirrors_workset = []
index_of_Mirrors_workset = workset_names.index("AIX_Plumbing Fixtures")
Mirrors_workset_id = workset_ids[index_of_Mirrors_workset].IntegerValue

# START TRANSACTION

Mirrors_pass_list = list()
Mirrors_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for m in Mirrors_list:
	try:
		Mirrors_param = m.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		Mirrors_param.Set(Mirrors_workset_id)
		Mirrors_pass_list.append(m)
	except:
		Mirrors_fail_list.append(m)
t.Commit()

###################################################################################################
# Speciality Equipment- Mirror Additional

index_of_Mirrors1 = [i for i, m in enumerate(speciality_equipment_Family_Names) if '17' in m]
# print(index_of_Mirrors1)

Mirrors1_list = [speciality_equipment[i] for i in index_of_Mirrors1]
Mirrors1_list = list(Mirrors1_list)
   
index_of_Mirrors1_workset = []
index_of_Mirrors1_workset = workset_names.index("AIX_Plumbing Fixtures")
Mirrors1_workset_id = workset_ids[index_of_Mirrors1_workset].IntegerValue

# START TRANSACTION

Mirrors1_pass_list = list()
Mirrors1_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for m in Mirrors1_list:
	try:
		Mirrors1_param = m.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		Mirrors1_param.Set(Mirrors1_workset_id)
		Mirrors1_pass_list.append(m)
	except:
		Mirrors1_fail_list.append(m)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Additional Bathroom Equipment

index_of_additional_bath_equip = [i for i, be in enumerate(speciality_equipment_Family_Names) if 'x' in be]
# print(index_of_additional_bath_equip)

additional_bath_equip_list = [speciality_equipment[i] for i in index_of_additional_bath_equip]
additional_bath_equip_list = list(additional_bath_equip_list)
   
index_of_additional_bath_equip_workset = []
index_of_additional_bath_equip_workset = workset_names.index("AIX_Plumbing Fixtures")
additional_bath_equip_workset_id = workset_ids[index_of_additional_bath_equip_workset].IntegerValue

# START TRANSACTION

additional_bath_equip_pass_list = list()
additional_bath_equip_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for be in additional_bath_equip_list:
	try:
		additional_bath_equip_param = be.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		additional_bath_equip_param.Set(additional_bath_equip_workset_id)
		additional_bath_equip_pass_list.append(be)
	except:
		additional_bath_equip_fail_list.append(be)
t.Commit()

###################################################################################################
# Speciality Equipment- More Additional Bathroom Equipment

index_of_more_additional_bath_equip = [i for i, abe in enumerate(speciality_equipment_Family_Names) if 'X' in abe]
# print(index_of_more_additional_bath_equip)

more_additional_bath_equip_list = [speciality_equipment[i] for i in index_of_more_additional_bath_equip]
more_additional_bath_equip_list = list(more_additional_bath_equip_list)
   
index_of_more_additional_bath_equip_workset = []
index_of_more_additional_bath_equip_workset = workset_names.index("AIX_Plumbing Fixtures")
more_additional_bath_equip_workset_id = workset_ids[index_of_more_additional_bath_equip_workset].IntegerValue

# START TRANSACTION

more_additional_bath_equip_pass_list = list()
more_additional_bath_equip_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for mbe in more_additional_bath_equip_list:
	try:
		more_additional_bath_equip_param = mbe.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		more_additional_bath_equip_param.Set(more_additional_bath_equip_workset_id)
		more_additional_bath_equip_pass_list.appendm(be)
	except:
		more_additional_bath_equip_fail_list.append(mbe)
t.Commit()

###################################################################################################

# Speciality Equipment- Handrail

index_of_handrail = [i for i, h in enumerate(speciality_equipment_Family_Names) if 'Handrail' in h]
# print(index_of_handrail)

handrail_list = [speciality_equipment[i] for i in index_of_handrail]
handrail_list = list(handrail_list)
   
index_of_handrail_workset = []
index_of_handrail_workset = workset_names.index("ARX_Railing")
handrail_workset_id = workset_ids[index_of_handrail_workset].IntegerValue

# START TRANSACTION

handrail_pass_list = list()
handrail_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in handrail_list:
	try:
		handrail_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		handrail_param.Set(handrail_workset_id)
		handrail_pass_list.append(h)
	except:
		handrail_fail_list.append(h)
t.Commit()

###################################################################################################
# Speciality Equipment- Coffee Machine

index_of_coffee_machines = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'COFFEE' in ut]
# print(index_of_coffee_machines)

coffee_machines_list = [speciality_equipment[i] for i in index_of_coffee_machines]
coffee_machines_list = list(coffee_machines_list)
   
index_of_coffee_machines_workset = []
index_of_coffee_machines_workset = workset_names.index("AIX_Furniture")
coffee_machines_workset_id = workset_ids[index_of_coffee_machines_workset].IntegerValue

# START TRANSACTION

coffee_machines_pass_list = list()
coffee_machines_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in coffee_machines_list:
	try:
		coffee_machines_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		coffee_machines_param.Set(coffee_machines_workset_id)
		coffee_machines_pass_list.append(h)
	except:
		coffee_machines_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Ice Cube Machine

index_of_ice_cube_machines = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'ICE' in ut]
# print(index_of_ice_cube_machines)

ice_cube_machines_list = [speciality_equipment[i] for i in index_of_ice_cube_machines]
ice_cube_machines_list = list(ice_cube_machines_list)
   
index_of_ice_cube_machines_workset = []
index_of_ice_cube_machines_workset = workset_names.index("AIX_Furniture")
ice_cube_machines_workset_id = workset_ids[index_of_ice_cube_machines_workset].IntegerValue

# START TRANSACTION

ice_cube_machines_pass_list = list()
ice_cube_machines_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in ice_cube_machines_list:
	try:
		ice_cube_machines_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ice_cube_machines_param.Set(ice_cube_machines_workset_id)
		ice_cube_machines_pass_list.append(h)
	except:
		ice_cube_machines_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Kitchnette

index_of_kitchenette = [i for i, ut in enumerate(speciality_equipment_Family_Names) if '1372' in ut]
# print(index_of_kitchenette)

kitchenette_list = [speciality_equipment[i] for i in index_of_kitchenette]
kitchenette_list = list(kitchenette_list)
   
index_of_kitchenette_workset = []
index_of_kitchenette_workset = workset_names.index("AIX_Furniture")
kitchenette_workset_id = workset_ids[index_of_kitchenette_workset].IntegerValue

# START TRANSACTION

kitchenette_pass_list = list()
kitchenette_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in kitchenette_list:
	try:
		kitchenette_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		kitchenette_param.Set(kitchenette_workset_id)
		kitchenette_pass_list.append(h)
	except:
		kitchenette_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Utility Shelf

index_of_utility_shelf = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'UTILITY' in ut]
# print(index_of_utility_shelf)

utility_shelf_list = [speciality_equipment[i] for i in index_of_utility_shelf]
utility_shelf_list = list(utility_shelf_list)
   
index_of_utility_shelf_workset = []
index_of_utility_shelf_workset = workset_names.index("AIX_Plumbing Fixtures")
utility_shelf_workset_id = workset_ids[index_of_utility_shelf_workset].IntegerValue

# START TRANSACTION

utility_shelf_pass_list = list()
utility_shelf_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in utility_shelf_list:
	try:
		utility_shelf_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		utility_shelf_param.Set(utility_shelf_workset_id)
		utility_shelf_pass_list.append(h)
	except:
		utility_shelf_fail_list.append(h)
t.Commit()

###################################################################################################
# Speciality Equipment- Bath Bench

index_of_bath_bench = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'BENCH' in ut]
# print(index_of_bath_bench)

bath_bench_list = [speciality_equipment[i] for i in index_of_bath_bench]
bath_bench_list = list(bath_bench_list)
   
index_of_bath_bench_workset = []
index_of_bath_bench_workset = workset_names.index("AIX_Plumbing Fixtures")
bath_bench_workset_id = workset_ids[index_of_bath_bench_workset].IntegerValue

# START TRANSACTION

bath_bench_pass_list = list()
bath_bench_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in bath_bench_list:
	try:
		bath_bench_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		bath_bench_param.Set(bath_bench_workset_id)
		bath_bench_pass_list.append(h)
	except:
		bath_bench_fail_list.append(h)
t.Commit()

###################################################################################################
# Speciality Equipment- Paper Towel Dispenser

index_of_paper_towel_dispenser = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'PTD' in ut]
# print(index_of_paper_towel_dispenser)

paper_towel_dispenser_list = [speciality_equipment[i] for i in index_of_paper_towel_dispenser]
paper_towel_dispenser_list = list(paper_towel_dispenser_list)
   
index_of_paper_towel_dispenser_workset = []
index_of_paper_towel_dispenser_workset = workset_names.index("AIX_Plumbing Fixtures")
paper_towel_dispenser_workset_id = workset_ids[index_of_paper_towel_dispenser_workset].IntegerValue

# START TRANSACTION

paper_towel_dispenser_pass_list = list()
paper_towel_dispenser_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in paper_towel_dispenser_list:
	try:
		paper_towel_dispenser_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		paper_towel_dispenser_param.Set(paper_towel_dispenser_workset_id)
		paper_towel_dispenser_pass_list.append(h)
	except:
		paper_towel_dispenser_fail_list.append(h)
t.Commit()

###################################################################################################
# Speciality Equipment- Soap Dishes

index_of_soap_dishes = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'SOAP' in ut]
# print(index_of_soap_dishes)

soap_dishes_list = [speciality_equipment[i] for i in index_of_soap_dishes]
soap_dishes_list = list(soap_dishes_list)
   
index_of_soap_dishes_workset = []
index_of_soap_dishes_workset = workset_names.index("AIX_Plumbing Fixtures")
soap_dishes_workset_id = workset_ids[index_of_soap_dishes_workset].IntegerValue

# START TRANSACTION

soap_dishes_pass_list = list()
soap_dishes_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in soap_dishes_list:
	try:
		soap_dishes_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		soap_dishes_param.Set(soap_dishes_workset_id)
		soap_dishes_pass_list.append(h)
	except:
		soap_dishes_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Recess

index_of_recessed = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'RECESS' in ut]
# print(index_of_recessed)

recessed_list = [speciality_equipment[i] for i in index_of_recessed]
recessed_list = list(recessed_list)
   
index_of_recessed_workset = []
index_of_recessed_workset = workset_names.index("AIX_Plumbing Fixtures")
recessed_workset_id = workset_ids[index_of_recessed_workset].IntegerValue

# START TRANSACTION

recessed_pass_list = list()
recessed_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in recessed_list:
	try:
		recessed_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		recessed_param.Set(recessed_workset_id)
		recessed_pass_list.append(h)
	except:
		recessed_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Towel Ring

index_of_towel_ring = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'RING' in ut]
# print(index_of_towel_ring)

towel_ring_list = [speciality_equipment[i] for i in index_of_towel_ring]
towel_ring_list = list(towel_ring_list)
   
index_of_towel_ring_workset = []
index_of_towel_ring_workset = workset_names.index("AIX_Plumbing Fixtures")
towel_ring_workset_id = workset_ids[index_of_towel_ring_workset].IntegerValue

# START TRANSACTION

towel_ring_pass_list = list()
towel_ring_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in towel_ring_list:
	try:
		towel_ring_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		towel_ring_param.Set(towel_ring_workset_id)
		towel_ring_pass_list.append(h)
	except:
		towel_ring_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Toilet Flush

index_of_toilet_flush = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'FLUSH' in ut]
# print(index_of_toilet_flush)

toilet_flush_list = [speciality_equipment[i] for i in index_of_toilet_flush]
toilet_flush_list = list(toilet_flush_list)
   
index_of_toilet_flush_workset = []
index_of_toilet_flush_workset = workset_names.index("AIX_Plumbing Fixtures")
toilet_flush_workset_id = workset_ids[index_of_toilet_flush_workset].IntegerValue

# START TRANSACTION

toilet_flush_pass_list = list()
toilet_flush_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in toilet_flush_list:
	try:
		toilet_flush_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		toilet_flush_param.Set(toilet_flush_workset_id)
		toilet_flush_pass_list.append(h)
	except:
		toilet_flush_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Toilet Roll Paper Holder

index_of_toilet_roll_holder = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'TRPH' in ut]
# print(index_of_toilet_roll_holder)

toilet_roll_holder_list = [speciality_equipment[i] for i in index_of_toilet_roll_holder]
toilet_roll_holder_list = list(toilet_roll_holder_list)
   
index_of_toilet_roll_holder_workset = []
index_of_toilet_roll_holder_workset = workset_names.index("AIX_Plumbing Fixtures")
toilet_roll_holder_workset_id = workset_ids[index_of_toilet_roll_holder_workset].IntegerValue

# START TRANSACTION

toilet_roll_holder_pass_list = list()
toilet_roll_holder_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in toilet_roll_holder_list:
	try:
		toilet_roll_holder_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		toilet_roll_holder_param.Set(toilet_roll_holder_workset_id)
		toilet_roll_holder_pass_list.append(h)
	except:
		toilet_roll_holder_fail_list.append(h)
t.Commit()
 
###################################################################################################

# Speciality Equipment-  Additional Toilet Roll Paper Holder

index_of_toilet_roll_holder_type2 = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'Chrome' in ut]
# print(index_of_toilet_roll_holder_type2)

toilet_roll_holder_type2_list = [speciality_equipment[i] for i in index_of_toilet_roll_holder_type2]
toilet_roll_holder_type2_list = list(toilet_roll_holder_type2_list)
   
index_of_toilet_roll_holder_type2_workset = []
index_of_toilet_roll_holder_type2_workset = workset_names.index("AIX_Plumbing Fixtures")
toilet_roll_holder_type2_workset_id = workset_ids[index_of_toilet_roll_holder_type2_workset].IntegerValue

# START TRANSACTION

toilet_roll_holder_type2_pass_list = list()
toilet_roll_holder_type2_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in toilet_roll_holder_type2_list:
	try:
		toilet_roll_holder_type2_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		toilet_roll_holder_type2_param.Set(toilet_roll_holder_type2_workset_id)
		toilet_roll_holder_type2_pass_list.append(h)
	except:
		toilet_roll_holder_type2_fail_list.append(h)
t.Commit()
 
###################################################################################################
# Speciality Equipment- Tissue Dispenser

index_of_tissue_dispenser = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'TS DIS' in ut]
# print(index_of_tissue_dispenser)

tissue_dispenser_list = [speciality_equipment[i] for i in index_of_tissue_dispenser]
tissue_dispenser_list = list(tissue_dispenser_list)
   
index_of_tissue_dispenser_workset = []
index_of_tissue_dispenser_workset = workset_names.index("AIX_Plumbing Fixtures")
tissue_dispenser_workset_id = workset_ids[index_of_tissue_dispenser_workset].IntegerValue

# START TRANSACTION

tissue_dispenser_pass_list = list()
tissue_dispenser_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in tissue_dispenser_list:
	try:
		tissue_dispenser_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		tissue_dispenser_param.Set(tissue_dispenser_workset_id)
		tissue_dispenser_pass_list.append(h)
	except:
		tissue_dispenser_fail_list.append(h)
t.Commit()

###################################################################################################
# Speciality Equipment- Toilet Sensor

index_of_toilet_sensor = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'SENSOR' in ut]
# print(index_of_toilet_sensor)

toilet_sensor_list = [speciality_equipment[i] for i in index_of_toilet_sensor]
toilet_sensor_list = list(toilet_sensor_list)
   
index_of_toilet_sensor_workset = []
index_of_toilet_sensor_workset = workset_names.index("AIX_Plumbing Fixtures")
toilet_sensor_workset_id = workset_ids[index_of_toilet_sensor_workset].IntegerValue

# START TRANSACTION

toilet_sensor_pass_list = list()
toilet_sensor_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in toilet_sensor_list:
	try:
		toilet_sensor_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		toilet_sensor_param.Set(toilet_sensor_workset_id)
		toilet_sensor_pass_list.append(h)
	except:
		toilet_sensor_fail_list.append(h)
t.Commit()


###################################################################################################
# Speciality Equipment- Planter Box

index_of_planter_box = [i for i, ut in enumerate(speciality_equipment_Family_Names) if 'PLANTER' in ut]
# print(index_of_planter_box)

planter_box_list = [speciality_equipment[i] for i in index_of_planter_box]
planter_box_list = list(planter_box_list)
   
index_of_planter_box_workset = []
index_of_planter_box_workset = workset_names.index("ARX_Specialty Equipment")
planter_box_workset_id = workset_ids[index_of_planter_box_workset].IntegerValue

# START TRANSACTION

planter_box_pass_list = list()
planter_box_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in planter_box_list:
	try:
		planter_box_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		planter_box_param.Set(planter_box_workset_id)
		planter_box_pass_list.append(h)
	except:
		planter_box_fail_list.append(h)
t.Commit()
 
 
 
###################################################################################################
# Speciality Equipment- Escalator

index_of_escalator_override = [i for i, ut in enumerate(speciality_equipment_Family_Names) if '27.35' in ut]
# print(index_of_escalator_override)

escalator_override_list = [speciality_equipment[i] for i in index_of_escalator_override]
escalator_override_list = list(escalator_override_list)
   
index_of_escalator_override_workset = []
index_of_escalator_override_workset = workset_names.index("ARX_Specialty Equipment")
escalator_override_workset_id = workset_ids[index_of_escalator_override_workset].IntegerValue

# START TRANSACTION

escalator_override_pass_list = list()
escalator_override_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for h in escalator_override_list:
	try:
		escalator_override_param = h.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		escalator_override_param.Set(escalator_override_workset_id)
		escalator_override_pass_list.append(h)
	except:
		planter_box_fail_list.append(h)
t.Commit() 
###################################################################################################
# All Walls
###################################################################################################

walls = all_elements_of_category(BuiltInCategory.OST_Walls)
# print(walls)

# loop walls
wall_Master_Name = []
for w in walls:
    wall_Master_Name.append(w.Name)
# print(wall_Master_Name)    

###################################################################################################
# All Wall Sweeps

index_of_Wall_Sweep = [i for i, ws in enumerate(wall_Master_Name) if 'Sweep' in ws]
# print(index_of_Wall_Sweep)

wall_sweep_list = [walls[i] for i in index_of_Wall_Sweep]
wall_sweep_list = list(wall_sweep_list)
# print(wall_sweep_list)

wall_sweep_Name = []
for w in wall_sweep_list:
    wall_sweep_Name.append(w.Name)
# print(wall_sweep_Name)

###################################################################################################
# Acquring index of Wall Sweep Workset

index_of_Wall_Sweep_workset = []
index_of_Wall_Sweep_workset = workset_names.index("AIX_Wall Finish")
Wall_Sweep_workset_id = workset_ids[index_of_Wall_Sweep_workset].IntegerValue

# START TRANSACTION for assigning Wall_Sweep to 'AIX_Wall Finish' Workset

Wall_Sweep_pass_list = list()
Wall_Sweep_Wall_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ws in wall_sweep_list:
	try:
		ws_param = ws.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ws_param.Set(Wall_Sweep_workset_id)
		Wall_Sweep_pass_list.append(ws)
	except:
		Wall_Sweep_fail_list.append(ws)
t.Commit()

#########################
#  Filtering Wall Sweeps

index_of_Filter_Wall_Sweep = [i for i, ws in enumerate(wall_Master_Name) if 'Sweep' not in ws]
# print(index_of_Filter_Wall_Sweep)

Filtered_wall_list = [walls[i] for i in index_of_Filter_Wall_Sweep]
Filtered_wall_list = list(Filtered_wall_list)
# print(Filtered_wall_list)

# loop Filtered walls
wall_Master1_Name = []
for w in Filtered_wall_list:
    wall_Master1_Name.append(w.Name)
# print(wall_Master1_Name)    

#####################################
# All Wall Void

index_of_wall_void = [i for i, ws in enumerate(wall_Master_Name) if 'Void' in ws]
# print(index_of_wall_void)

wall_void_list = [Filtered_wall_list[i] for i in index_of_wall_void]
wall_void_list = list(wall_void_list)
# print(wall_void_list)

#####################################
# Acquring index of Wall Void Workset

index_of_Wall_Void_workset = []
index_of_Wall_Void_workset = workset_names.index("ARX_Internal")
Wall_Void_workset_id = workset_ids[index_of_Wall_Void_workset].IntegerValue

# START TRANSACTION for assigning Wall_Void to 'AIX_Wall Finish' Workset

Wall_Void_pass_list = list()
Wall_Void_Wall_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ws in wall_void_list:
	try:
		ws_param = ws.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ws_param.Set(Wall_Void_workset_id)
		Wall_Void_pass_list.append(ws)
	except:
		Wall_Void_fail_list.append(ws)
t.Commit()

#####################################
#  Filtering Wall Voids

index_of_Filter_Wall_Void = [i for i, ws in enumerate(wall_Master1_Name) if 'Void' not in ws]
# print(index_of_Filter_Wall_Void)

Filtered_wall_list2 = [Filtered_wall_list[i] for i in index_of_Filter_Wall_Void]
Filtered_wall_list2 = list(Filtered_wall_list2)
# print(Filtered_wall_list2)

# loop Filtered walls
wall_Master2_Name = []
for w in Filtered_wall_list2:
    wall_Master2_Name.append(w.Name)
# print(wall_Master2_Name)   


#####################################
# All Wall Ceiling Soffits

index_of_ceiling_soffit = [i for i, ws in enumerate(wall_Master2_Name) if 'CLG' in ws]
# print(index_of_ceiling_soffit)

ceiling_soffit_list = [Filtered_wall_list2[i] for i in index_of_ceiling_soffit]
ceiling_soffit_list = list(ceiling_soffit_list)
# print(ceiling_soffit_list)

#####################################
# Acquring index of Wall Void Workset

index_of_ceiling_soffit_workset = []
index_of_ceiling_soffit_workset = workset_names.index("AIX_Ceiling")
ceiling_soffit_workset_id = workset_ids[index_of_ceiling_soffit_workset].IntegerValue

# START TRANSACTION for assigning ceiling_soffit to 'AIX_Wall Finish' Workset

ceiling_soffit_pass_list = list()
ceiling_soffit_Wall_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ws in ceiling_soffit_list:
	try:
		ws_param = ws.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ws_param.Set(ceiling_soffit_workset_id)
		ceiling_soffit_pass_list.append(ws)
	except:
		ceiling_soffit_fail_list.append(ws)
t.Commit()

#####################################
#  Filtering Ceiling Soffits

index_of_Filter_ceiling_soffit = [i for i, ws in enumerate(wall_Master2_Name) if 'CLG' not in ws]
# print(index_of_Filter_ceiling_soffit)

Filtered_wall_list3 = [Filtered_wall_list2[i] for i in index_of_Filter_ceiling_soffit]
Filtered_wall_list3 = list(Filtered_wall_list3)
# print(Filtered_wall_list3)

# loop Filtered walls
wall_Master3_Name = []
for w in Filtered_wall_list3:
    wall_Master3_Name.append(w.Name)
# print(wall_Master3_Name)   


wall_Types = []
for w in Filtered_wall_list3:
    wall_Types.append(w.WallType)
# print(wall_Types)


# # ########################################################
# # '''Code for wall width segregation'''''

wall_Type_Width = []
for wtw in wall_Types:
    wall_Type_Width.append(wtw.Width)
# print(wall_Type_Width)

wall_Type_Width_mm = []
for wtw in wall_Type_Width:
    wall_Type_Width_mm.append(int(wtw * 304.8))
# print(wall_Type_Width_mm)


##########################################################

# Identifying 'Curtain Wall' & 'Basic Wall'
    
wall_Family_Names = []
for w in wall_Types:
    wall_Family_Names.append(w.FamilyName)
# print(wall_Family_Names)


##########################################################
#########################################################

# Accessing Basic walls

index_of_Basic_Wall = list()
for n, i in enumerate(wall_Family_Names):
    if i == "Basic Wall":
        index_of_Basic_Wall.append(n)  
# print(index_of_Basic_Wall)

Basic_Wall_list = [Filtered_wall_list3[i] for i in index_of_Basic_Wall]
Basic_Wall_list = list(Basic_Wall_list)
#print(Basic_Wall_list)

# Identifying Basic walls : Family Names

Basic_Wall_Names = []
for bw in Basic_Wall_list:
    Basic_Wall_Names.append(bw.Name)
# print(Basic_Wall_Names)

index_of_Ext_Basic_Wall = [i for i, ebw in enumerate(Basic_Wall_Names) if 'EXT' in ebw]
# print(index_of_Ext_Basic_Wall)

Exterior_Basic_Wall_list = [Basic_Wall_list[i] for i in index_of_Ext_Basic_Wall]
Exterior_Basic_Wall_list = list(Exterior_Basic_Wall_list)

########################################################################################
# test for filtered Exterior_Basic_Walls

Exterior_Basic_Wall_Names = []
for ebwl in Exterior_Basic_Wall_list:
    Exterior_Basic_Wall_Names.append(ebwl.Name)
# print(Exterior_Basic_Wall_Names)
########################################################################################

# Acquring index of Exterior wall Workset

index_of_Exterior_Wall_workset = []
index_of_Exterior_Wall_workset = workset_names.index("ARX_External")
Exterior_Wall_workset_id = workset_ids[index_of_Exterior_Wall_workset].IntegerValue

# START TRANSACTION for assigning Exterior_Basic_Walls to 'AR_Exterior' Workset

Exterior_Basic_Wall_pass_list = list()
Exterior_Basic_Wall_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ebwl in Exterior_Basic_Wall_list:
	try:
		ebwl_param = ebwl.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ebwl_param.Set(Exterior_Wall_workset_id)
		Exterior_Basic_Wall_pass_list.append(ebwl)
	except:
		Exterior_Basic_Wall_fail_list.append(ebwl)
t.Commit()


###################################################################################################
###################################################################################################
# Acquring index of Interior walls 

index_of_Int_Basic_Wall = [i for i, ebw in enumerate(Basic_Wall_Names) if 'INT' in ebw]
#print(index_of_Int_Basic_Wall)

Interior_Basic_Wall_list = [Basic_Wall_list[i] for i in index_of_Int_Basic_Wall]
Interior_Basic_Wall_list = list(Interior_Basic_Wall_list)

########################################################################################
# test for filtered Interior_Basic_Walls

Interior_Basic_Wall_Names = []
for ibwl in Interior_Basic_Wall_list:
    Interior_Basic_Wall_Names.append(ibwl.Name)
# print(Interior_Basic_Wall_Names)

########################################################################################
# loop Interior Basic Walls,segregation for load bearing, non load bearing walls

Interior_Basic_Wall_Types = []
for ibwl in Interior_Basic_Wall_list:
    Interior_Basic_Wall_Types.append(ibwl.WallType)
# print(Interior_Basic_Wall_Types)

Interior_Wall_Type_Width = []
for wtw in Interior_Basic_Wall_Types:
    Interior_Wall_Type_Width.append(wtw.Width)
# print(Interior_Wall_Type_Width)

Interior_Wall_Type_Width_mm = []
for wtw in Interior_Wall_Type_Width:
    Interior_Wall_Type_Width_mm.append(int(wtw * 304.8))
#print(Interior_Wall_Type_Width_mm)

index_of_Int_wall_non_load_bearing = [i for i, ebw in enumerate(Interior_Wall_Type_Width_mm) if (ebw <= 100)]
# print(index_of_Int_wall_non_load_bearing)     

final_Interior_Wall_List = [Interior_Basic_Wall_list[i] for i in index_of_Int_wall_non_load_bearing]
final_Interior_Wall_List = list(final_Interior_Wall_List)

########################################################################################
# test for filtered final_Interior_Basic_Walls

# final_Interior_Basic_Wall_Names = []
# for ibwl in final_Interior_Wall_List:
#     final_Interior_Basic_Wall_Names.append(ibwl.Name)
# print(final_Interior_Basic_Wall_Names)

########################################################################################
# Acquring index of Interior wall Workset

index_of_Interior_Wall_workset = []
index_of_Interior_Wall_workset = workset_names.index("AIX_Wall Finish")
Interior_Wall_workset_id = workset_ids[index_of_Interior_Wall_workset].IntegerValue

# # START TRANSACTION for assigning Interior_Basic_Walls to 'AR_Internal' Workset

Interior_Basic_Wall_pass_list = list()
Interior_Basic_Wall_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for ibwl in final_Interior_Wall_List:
	try:
		ibwl_param = ibwl.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		ibwl_param.Set(Interior_Wall_workset_id)
		Interior_Basic_Wall_pass_list.append(ibwl)
	except:
		Interior_Basic_Wall_fail_list.append(ibwl)
t.Commit()

##################################################################################################
# Acquring index of Soffits

index_of_Soffits = [i for i, ebw in enumerate(Basic_Wall_Names) if 'Soffit' in ebw]
# print(index_of_Soffits)

Soffit_list = [Basic_Wall_list[i] for i in index_of_Soffits]
Soffit_list = list(Soffit_list)

########################################################################################
# test for filtered Interior_Basic_Walls

# Soffit_Names = []
# for sf in Soffit_list:
#     Soffit_Names.append(sf.Name)
# print(Soffit_Names)

########################################################################################

# Acquring index of Interior wall Workset

index_of_Soffit_Workset = []
index_of_Soffit_workset = workset_names.index("AIX_Wall Finish")
Soffit_workset_id = workset_ids[index_of_Soffit_workset].IntegerValue

# # START TRANSACTION for assigning Interior_Basic_Walls to 'AR_Internal' Workset

Soffit_pass_list = list()
Soffit_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for sf in Soffit_list:
	try:
		Soffit_param = sf.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		Soffit_param.Set(Soffit_workset_id)
		Soffit_pass_list.append(sf)
	except:
		Soffit_fail_list.append(sf)
t.Commit()

##################################################################################################

# Accessing Curtain Walls

index_of_Curtain_Wall = list()
for n, i in enumerate(wall_Family_Names):
    if i == "Curtain Wall":
        index_of_Curtain_Wall.append(n)  
# print(index_of_Curtain_Wall)

Curtain_Wall_list = [Filtered_wall_list3[i] for i in index_of_Curtain_Wall]
Curtain_Wall_list = list(Curtain_Wall_list)
# print(Curtain_Wall_list)

# Identifying Curtain walls : Family Names

Curtain_Wall_Names = []
for cw in Curtain_Wall_list:
    Curtain_Wall_Names.append(cw.Name)
# print(Curtain_Wall_Names)

index_of_Skin_Curtain_Wall_workset = []
index_of_Skin_Curtain_Wall_workset = workset_names.index("ARX_Internal")     # Add('ARX_Skin') for Skin File
skin_workset_id = workset_ids[index_of_Skin_Curtain_Wall_workset].IntegerValue

index_of_Interior_Curtain_Wall_workset = []
index_of_Interior_Curtain_Wall_workset = workset_names.index("ARX_Internal")
Interior_Curtain_Wall_workset_id = workset_ids[index_of_Interior_Curtain_Wall_workset].IntegerValue

index_of_Exterior_Curtain_Wall_workset = []
index_of_Exterior_Curtain_Wall_workset = workset_names.index("ARX_External")	# Add('ARX_External') for External Elements if any
Exterior_Curtain_Wall_workset_id = workset_ids[index_of_Exterior_Curtain_Wall_workset].IntegerValue

# revit_file_name
if('ZZ-ZZ' in revit_file_name):
    Skin_Curtain_Wall_pass_list = list()
    Skin_Curtain_Wall_fail_list = list()
    t = Transaction(doc, 'script')
    t.Start()
    for skin in Curtain_Wall_list:
        try:
            Skin_Curtain_Wall_param = skin.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
            Skin_Curtain_Wall_param.Set(skin_workset_id)
            Skin_Curtain_Wall_pass_list.append(skin)
        except:
            Skin_Curtain_Wall_fail_list.append(skin)
    t.Commit()

else:
    index_of_Int_Curtain_Wall = [i for i, icw in enumerate(Curtain_Wall_Names) if 'INT' in icw]
    # print(index_of_Int_Curtain_Wall)
    
    Interior_Curtain_Wall_list = [Curtain_Wall_list[i] for i in index_of_Int_Curtain_Wall]
    Interior_Curtain_Wall_list = list(Interior_Curtain_Wall_list)   
    Interior_Curtain_Wall_pass_list = list()
    Interior_Curtain_Wall_fail_list = list()
    t = Transaction(doc, 'script')
    t.Start()
    for icw in Interior_Curtain_Wall_list:
        try:
            Interior_Curtain_Wall_param = icw.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
            Interior_Curtain_Wall_param.Set(Interior_Curtain_Wall_workset_id)
            Interior_Curtain_Wall_pass_list.append(icw)
        except:
            Interior_Curtain_Wall_fail_list.append(icw)
    t.Commit()
    
    index_of_Ext_Curtain_Wall = [i for i, ecw in enumerate(Curtain_Wall_Names) if 'EXT' not in ecw]  # Change to " if "'EXT' in " case of Exterior Skin
    # print(index_of_Ext_Curtain_Wall)
    
    Exterior_Curtain_Wall_list = [Curtain_Wall_list[i] for i in index_of_Ext_Curtain_Wall]
    Exterior_Curtain_Wall_list = list(Exterior_Curtain_Wall_list)   
    Exterior_Curtain_Wall_pass_list = list()
    Exterior_Curtain_Wall_fail_list = list()
    t = Transaction(doc, 'script')
    t.Start()
    for ecw in Exterior_Curtain_Wall_list:
        try:
            Exterior_Curtain_Wall_param = ecw.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
            Exterior_Curtain_Wall_param.Set(Exterior_Curtain_Wall_workset_id)
            Exterior_Curtain_Wall_pass_list.append(ecw)
        except:
            Exterior_Curtain_Wall_fail_list.append(ecw)
    t.Commit()           
 
######################################################################################################

# Column Cladding

column_cladding = all_elements_of_category(BuiltInCategory.OST_Columns)
   
index_of_column_cladding = []
index_of_column_cladding = workset_names.index("AIX_Wall Finish")


column_cladding_id = workset_ids[index_of_column_cladding].IntegerValue

# START TRANSACTION

column_cladding_pass_list = list()
column_cladding_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for f in column_cladding:
	try:
		column_cladding_param = f.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		column_cladding_param.Set(column_cladding_id)
		column_cladding_pass_list.append(f)
	except:
		column_cladding_fail_list.append(f)
t.Commit()

###################################################################################################
# Roof 

roof = all_elements_of_category(BuiltInCategory.OST_Roofs)
# print(speciality_equipment)

roof_Family_Names = []
for sp in roof:
    roof_Family_Names.append(sp.Name)
# print(roof_Family_Names)

###################################################################################################
# Internal Design Roof

index_of_roof = [i for i, rf in enumerate(roof_Family_Names) if 'PIS' in rf]
# print(index_of_roof)

interior_roof_list = [roof[i] for i in index_of_roof]
interior_roof_list = list(interior_roof_list)
   
index_of_interior_roof_workset = []
index_of_interior_roof_workset = workset_names.index("AIX_Ceiling")
interior_roof_workset_id = workset_ids[index_of_interior_roof_workset].IntegerValue

# START TRANSACTION

interior_roof_pass_list = list()
interior_roof_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for rf in interior_roof_list:
	try:
		interior_roof_param = rf.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		interior_roof_param.Set(interior_roof_workset_id)
		interior_roof_pass_list.append(rf)
	except:
		interior_roof_fail_list.append(rf)
t.Commit()

###################################################################################################
# Roof Opening

roof_opening = all_elements_of_category(BuiltInCategory.OST_RoofOpening)
   
index_of_roof_opening = []
index_of_roof_opening = workset_names.index("AIX_Ceiling")


roof_opening_id = workset_ids[index_of_roof_opening].IntegerValue

# START TRANSACTION

roof_opening_pass_list = list()
roof_opening_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for f in roof_opening:
	try:
		roof_opening_param = f.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		roof_opening_param.Set(roof_opening_id)
		roof_opening_pass_list.append(f)
	except:
		roof_opening_fail_list.append(f)
t.Commit()

###################################################################################################

# Windows

windows = all_elements_of_category(BuiltInCategory.OST_Windows)
   
index_of_windows = []
index_of_windows = workset_names.index("ARX_Internal")


windows_id = workset_ids[index_of_windows].IntegerValue

# START TRANSACTION

windows_pass_list = list()
windows_fail_list = list()
t = Transaction(doc, 'script')
t.Start()
for wdw in windows:
	try:
		windows_param = wdw.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
		windows_param.Set(windows_id)
		windows_pass_list.append(wdw)
	except:
		windows_fail_list.append(wdw)
t.Commit()

###################################################################################################

# Wall Sweeps

# wall_sweep = all_elements_of_category(BuiltInCategory.OST_WallSweep)
   
# index_of_wall_sweep = []
# index_of_wall_sweep = workset_names.index("ARX_Internal")


# wall_sweep_id = workset_ids[index_of_wall_sweep].IntegerValue

# # START TRANSACTION

# wall_sweep_pass_list = list()
# wall_sweep_fail_list = list()
# t = Transaction(doc, 'script')
# t.Start()
# for wdw in wall_sweep:
# 	try:
# 		wall_sweep_param = wdw.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
# 		wall_sweep_param.Set(wall_sweep_id)
# 		wall_sweep_pass_list.append(wdw)
# 	except:
# 		wall_sweep_fail_list.append(wdw)
# t.Commit()

###################################################################################################

