#!/usr/bin/env python
# * coding: utf8 *
'''
test_facility.py
A module that tests the facility attribute rules
'''

import os

import arcpy

table_name = 'UICFacility'
sde = os.path.join(os.path.dirname(__file__), '..', 'pro-project', 'localhost.sde')
TABLE = os.path.join(sde, table_name)

# pragma pylint: disable=no-member


def cleanup():
    with arcpy.da.UpdateCursor(TABLE, ['OID@'], where_clause="FacilityName IN ('0', '1')") as cursor:
        for _ in cursor:
            cursor.deleteRow()


def setup_function():
    '''function setup'''
    cleanup()


def teardown_function():
    '''function teardown'''
    cleanup()


def test_guid_calculation():
    test_attribute = 'FacilityName'
    calculated_attribute = 'GUID'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Calculate_Guid'
    arcpy.management.DisableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([disabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        for name, in cursor:
            assert name is None

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([enabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        for name, in cursor:
            assert name is not None


def test_state_calculation():
    test_attribute = 'FacilityName'
    calculated_attribute = 'FacilityState'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Calculate_State'
    arcpy.management.DisableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([disabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        for value, in cursor:
            print('disabled value: {}'.format(value))
            assert value is None

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([enabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        for value, in cursor:
            print('enabled value: {}'.format(value))
            assert value == 'UT'


def test_facility_id_calculation():
    test_attribute = 'CountyFIPS'
    calculated_attribute = 'FacilityID'
    disabled_rule_value = '0'
    enabled_rule_value = '1'

    rule_name = 'Calculate_Id'
    arcpy.management.DisableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([disabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, disabled_rule_value)) as cursor:
        for value, in cursor:
            print('disabled value: {}'.format(value))
            assert value is None

    arcpy.management.EnableAttributeRules(TABLE, rule_name)

    with arcpy.da.InsertCursor(TABLE, [test_attribute]) as cursor:
        cursor.insertRow([enabled_rule_value])

    with arcpy.da.SearchCursor(TABLE, [calculated_attribute], where_clause="{}='{}'".format(test_attribute, enabled_rule_value)) as cursor:
        for value, in cursor:
            print('enabled value: {}'.format(value))
            assert value.startswith('UTU1')
