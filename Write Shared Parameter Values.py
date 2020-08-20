"""Write Shared Parameter Values"""

__title__ = "Write\nShared Parameter\nValues"
__author__= "J K Roshan\nKerketta"

from pyrevit.coreutils import envvars
from decimal import *
from pyrevit import forms
from pyrevit import script
from pyrevit import coreutils
from itertools import chain

#Select Excel File from Folder

logger = script.get_logger()
# if__name__ == '__main__':
source_file = forms.pick_file(file_ext='xls')
 
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
loc = source_file
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
 
   
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

#####################################################################################################################
# Read Excel Parameters and Family Category

plumbing_param_to_read = sheet.col_values(0)
# print(plumbing_param_to_read)

def str_parameters(_paraVal):
    	for x in _paraVal:
		return str(x)		

plumbing_params = str_parameters(plumbing_param_to_read)
# print(plumbing_params)

MXPA_ASSETNUM = sheet.col_values(0)
MXPA_ASSET_DESCRIPTION = sheet.col_values(1)
MXPA_PARENT = sheet.col_values(2)
MXPA_ASSET_STATUS = sheet.col_values(3)
MXPA_CLASSIFICATIONID = sheet.col_values(4)
MXPA_FUNCTIONALLOCATION = sheet.col_values(5)
MXPA_DESCRIPTION = sheet.col_values(6)
MXPA_DAFACILITY = sheet.col_values(7)
MXPA_CRITICALITY = sheet.col_values(8)
MXPA_BUSINESSFACTOR = sheet.col_values(9)
MXPA_LOCATION_STATUS = sheet.col_values(10)
MXPA_FUNCTIONAL = sheet.col_values(11)
MXPA_ITEMNUM =sheet.col_values(12)
MXPA_SERIALNUM =sheet.col_values(13)
MXPA_VENDOR =sheet.col_values(14)
MXPA_MANUFACTURER = sheet.col_values(15)
MXPA_MODEL = sheet.col_values(16)
MXPA_PHY_LOCATION = sheet.col_values(17)
MXPA_SYSTEMID = sheet.col_values(18)
MXPA_SITEID = sheet.col_values(19)

asset_dictionary = {z[0]:list(z[1:]) for z in zip(MXPA_ASSETNUM,MXPA_ASSET_DESCRIPTION,MXPA_PARENT,MXPA_ASSET_STATUS,MXPA_CLASSIFICATIONID,MXPA_FUNCTIONALLOCATION,MXPA_DESCRIPTION,MXPA_DAFACILITY,MXPA_CRITICALITY,MXPA_BUSINESSFACTOR,MXPA_LOCATION_STATUS,MXPA_FUNCTIONAL,MXPA_ITEMNUM,MXPA_SERIALNUM,MXPA_VENDOR,MXPA_MANUFACTURER,MXPA_MODEL,MXPA_PHY_LOCATION,MXPA_SYSTEMID,MXPA_SITEID)}
# print(asset_dictionary)

#####################################################################################################################
#All elements of category- Plumbing Fixtures

plumbing_fixtures = all_elements_of_category(BuiltInCategory.OST_PlumbingFixtures)
# print(plumbing_fixtures)

#####################################################################################################################
# Acquiring MXPA Asset Numbers for Category

def filtered_category_list(category_collector):
    cat_asset_num = list()
    for cat in category_collector:
        for param in cat.Parameters:
            if param.IsShared and param.Definition.Name == 'MXPA_ASSETNUM':
                paramValue = cat.get_Parameter(param.GUID)
                cat_asset_num.append(paramValue.AsString())
    
    cat_None_index = indices(cat_asset_num, None)
    filtered_cat_list = [ j for i, j in enumerate(category_collector) if i not in (cat_None_index)]
    return filtered_cat_list

def filtered_asset_num(filtered_assets):
    asset_num =  []
    for asset in filtered_assets:
        for param in asset.Parameters:
            if param.IsShared and param.Definition.Name == 'MXPA_ASSETNUM':
                paramValue = asset.get_Parameter(param.GUID)
                asset_num.append(paramValue.AsString())
    return asset_num          

#####################################################################################################################
filtered_plumbing_fixtures = filtered_category_list(plumbing_fixtures)
filtered_plumbing_fixtures_num = filtered_asset_num(filtered_plumbing_fixtures)

#####################################################################################################################
# Acquiring MXPA Asset Classification List

classify = asset_dictionary.values()
count = len(classify)
classify_identity = [i[3] for i in classify[:count]]
# print(classify_identity)

#####################################################################################################################

def classify_category_from_database(classificationID):
    classify_cat_index = indices(classify_identity,classificationID)
    classified_cat_keys = [ j for i, j in enumerate(asset_dictionary) if i in (classify_cat_index)]
    classified_cat_values = [ j for i, j in enumerate(classify) if i in (classify_cat_index)]
    return classified_cat_keys, classified_cat_values

#####################################################################################################################

classified_plumbing_data  = classify_category_from_database("DOOR, ROLL UP")
classified_plumbing_keys = classified_plumbing_data[0]
classified_plumbing_values = classified_plumbing_data[1]

# classified_sliding_door_values = classify_category_from_database("DOOR, ROLL UP")
# classified_shutter_values = classify_category_from_database("SHUTTER")

#####################################################################################################################

def scheduled_values_for_revit(filtered_asset_num_values, classified_asset_keys, classified_asset_values, asset_serial_number_index):
    temp = set(filtered_asset_num_values)
    lookup_assets = [i for i, val in enumerate(classified_asset_keys) if val in temp]
    res_list = [classified_asset_keys[i] for i in lookup_assets]
    values_from_register = [classified_asset_values[i] for i in lookup_assets]
    count = len(values_from_register)
    final_asset_data = [i[asset_serial_number_index] for i in values_from_register[:count]]
    index_test = range(len(res_list))
    test_dict = dict(zip(res_list,index_test))
    final_val = [test_dict.get(anum, None) for anum in filtered_asset_num_values]
    Revit_data = [final_asset_data[i] for i in final_val if i is not None]
    res_None = [i for i in range(len(final_val)) if final_val[i] != None]
    for(i, r) in zip(res_None, Revit_data):
        final_val[i] = r
    final_val = [str(i or '') for i in final_val]
    return final_val

#####################################################################################################################

final_plumbing_Revit_values_asset_description = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 0)
final_plumbing_Revit_values_parent = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 1)
final_plumbing_Revit_values_asset_status = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 2)
final_plumbing_Revit_values_classificationID= scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 3)
final_plumbing_Revit_values_functional_location = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 4)
final_plumbing_Revit_values_description = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 5)
final_plumbing_Revit_values_dafacility = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 6)
final_plumbing_Revit_values_criticality = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 7)
final_plumbing_Revit_values_businessfactor = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 8)
final_plumbing_Revit_values_location_status = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 9)
final_plumbing_Revit_values_functional = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values,10)
final_plumbing_Revit_values_itemnum  = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 11)
final_plumbing_Revit_values_serialnum = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 12)
final_plumbing_Revit_values_vendor = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 13)
final_plumbing_Revit_values_manufacturer = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 14)
final_plumbing_Revit_values_model = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 15)
final_plumbing_Revit_values_phy_location = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 16)
final_plumbing_Revit_values_systemID = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 17)
final_plumbing_Revit_values_siteID = scheduled_values_for_revit(filtered_plumbing_fixtures_num, classified_plumbing_keys, classified_plumbing_values, 18)

#####################################################################################################################


def set_parameter_by_name(element, parameterName, value):
	element.LookupParameter(parameterName).Set(value)

def add_values_to_revit(asset_name, filtered_assets, final_asset_values_for_Revit):
    t = Transaction(doc, 'script')
    write_asset_pass = []
    write_asset_fail = []
    
    t.Start()
    for p in filtered_assets:
        try:
            write_asset_pass = [set_parameter_by_name(p, asset_name, pval) for p, pval in zip(filtered_assets, final_asset_values_for_Revit)]
        except:
            write_asset_fail.append(pval)

    t.Commit()
    return(write_asset_pass,write_asset_fail)


#####################################################################################################################





write_plumbing_fixture_values_asset_description_to_Revit = add_values_to_revit('MXPA_ASSET_DESCRIPTION', filtered_plumbing_fixtures, final_plumbing_Revit_values_asset_description)
write_plumbing_fixture_values_parent_to_Revit = add_values_to_revit('MXPA_PARENT', filtered_plumbing_fixtures, final_plumbing_Revit_values_parent)
write_plumbing_fixture_values_asset_status_to_Revit = add_values_to_revit('MXPA_ASSET_STATUS', filtered_plumbing_fixtures, final_plumbing_Revit_values_asset_status)
write_plumbing_fixture_values_classificationID_to_Revit = add_values_to_revit('MXPA_ASSET_STATUS', filtered_plumbing_fixtures, final_plumbing_Revit_values_classificationID)
write_plumbing_fixture_values_functional_location_to_Revit = add_values_to_revit('MXPA_FUNCTIONAL LOCATION', filtered_plumbing_fixtures, final_plumbing_Revit_values_functional_location)
write_plumbing_fixture_values_description_to_Revit = add_values_to_revit('MXPA_DESCRIPTION', filtered_plumbing_fixtures, final_plumbing_Revit_values_description)
write_plumbing_fixture_values_dafacility_to_Revit = add_values_to_revit('MXPA_DAFACILITY', filtered_plumbing_fixtures, final_plumbing_Revit_values_dafacility)
write_plumbing_fixture_values_criticality_to_Revit = add_values_to_revit('MXPA_CRITICALITY', filtered_plumbing_fixtures, final_plumbing_Revit_values_criticality)
write_plumbing_fixture_values_businessfactor_to_Revit = add_values_to_revit('MXPA_BUSINESSFACTOR', filtered_plumbing_fixtures, final_plumbing_Revit_values_businessfactor)
write_plumbing_fixture_values_location_status_to_Revit = add_values_to_revit('MXPA_LOCATION_STATUS', filtered_plumbing_fixtures, final_plumbing_Revit_values_location_status)
write_plumbing_fixture_values_functional_to_Revit = add_values_to_revit('MXPA_FUNCTIONAL', filtered_plumbing_fixtures, final_plumbing_Revit_values_functional)
write_plumbing_fixture_values_itemnum_to_Revit = add_values_to_revit('MXPA_ITEMNUM', filtered_plumbing_fixtures, final_plumbing_Revit_values_itemnum)
write_plumbing_fixture_values_serialnum_to_Revit = add_values_to_revit('MXPA_SERIALNUM', filtered_plumbing_fixtures, final_plumbing_Revit_values_serialnum)
write_plumbing_fixture_values_vendor_to_Revit = add_values_to_revit('MXPA_VENDOR', filtered_plumbing_fixtures, final_plumbing_Revit_values_vendor)
write_plumbing_fixture_values_manufacturer_to_Revit = add_values_to_revit('MXPA_MANUFACTURER', filtered_plumbing_fixtures, final_plumbing_Revit_values_manufacturer)
write_plumbing_fixture_values_model_to_Revit = add_values_to_revit('MXPA_MODEL', filtered_plumbing_fixtures, final_plumbing_Revit_values_model)
write_plumbing_fixture_values_phy_location_to_Revit = add_values_to_revit('MXPA_PHY_LOCATION', filtered_plumbing_fixtures, final_plumbing_Revit_values_phy_location)
write_plumbing_fixture_values_systemID_to_Revit = add_values_to_revit('MXPA_SYSTEMID', filtered_plumbing_fixtures, final_plumbing_Revit_values_systemID)
write_plumbing_fixture_values_siteID_to_Revit = add_values_to_revit('MXPA_SITEID', filtered_plumbing_fixtures, final_plumbing_Revit_values_siteID)



######################################################################################################################





