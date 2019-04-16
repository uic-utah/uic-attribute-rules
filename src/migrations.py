#!/usr/bin/env python
# * coding: utf8 *
'''
migrations.py
A module that migrates uic database
'''

import os

from arcgisscripting import ExecuteError  # pylint: disable=no-name-in-module

import arcpy
from config import config

delete_tables = [
    'UICAlternateDisposal',
    'UICAquiferRemediation',
    'UICBMPElement',
    'UICClassIConstituent',
    'UICClassIWaste',
    'UICConstructionElement',
    'UICDeepWellOperation',
    'UICVerticalWellEvent',
    'DEQFacilities',
    'UICSCHEMATRONERRORCODES',
    'UICToolbox',
]

delete_domains = [
    'UICAlternateDisposalTypeDomain',
    'UICAquiferRemediationDomain',
    'UICBMPElementTypeDomain',
    'UICConcentrationUnitDomain',
    'UICConstructionElementTypeDomain',
    'UICEventTypeDomain',
    'UICEventUnitsDomain',
    'UICCityDomain',
    'UICZoningCategoryDomain',
    'UICLocationMethodDomain',
    'UICLocationalAccuracyDomain',
    'UICICISCompActTypeDomain',
    'UICICISCompMonActReasonDomain',
    'UICICISMonitoringTypeDomain',
]

table_modifications = {
    'UICFacility': {
        'add': [],
        'delete': ['FRSID', 'FacilityState']
    },
    'UICWell': {
        'add': [{
            'in_table': 'UICWell',
            'field_name': 'WellDepth',
            'field_type': 'LONG',
            'field_length': '#',
            'field_precision': 10,
            'field_scale': 0,
            'field_alias': 'Well Depth in Feet',
            'field_is_nullable': 'NULLABLE'
        }],
        'delete': ['ConvertedOGWell', 'LocationMethod', 'LocationAccuracy']
    },
    'UICInspection': {
        'add': [],
        'delete': ['ICISCompMonActReason', 'ICISCompMonType', 'ICISCompActType', 'ICISMOAPriority', 'ICISRegionalPriority']
    },
    'UICArtPen': {
        'add': [
            {
                'in_table': 'UICArtPen',
                'field_name': 'EditedBy',
                'field_type': 'TEXT',
                'field_length': 40,
                'field_precision': '#',
                'field_scale': '#',
                'field_alias': 'EditedBy',
                'field_is_nullable': 'NULLABLE'
            },
            {
                'in_table': 'UICArtPen',
                'field_name': 'ArtPenWellDepth',
                'field_type': 'LONG',
                'field_length': '#',
                'field_precision': 10,
                'field_scale': 0,
                'field_alias': 'ArtPenWellDepth',
                'field_is_nullable': 'NULLABLE'
            },
        ],
        'delete': ['EditedBy']
    }
}

arcpy.env.workspace = config.sde

print('removing {} tables'.format(len(delete_tables)))
for table in delete_tables:
    arcpy.management.Delete(os.path.join(config.sde, table))
print('done')

print('applying table modifications')
for table_name in table_modifications:
    changes = table_modifications[table_name]

    deletes = changes['delete']
    adds = changes['add']

    try:
        if deletes:
            arcpy.management.DeleteField(table_name, deletes)

        for add in adds:
            arcpy.management.AddField(
                in_table=add['in_table'],
                field_name=add['field_name'],
                field_type=add['field_type'],
                field_precision=add['field_precision'],
                field_scale=add['field_scale'],
                field_length=add['field_length'],
                field_alias=add['field_alias'],
                field_is_nullable=add['field_is_nullable']
            )
    except ExecuteError as e:
        message, = e.args

        if 'ERROR 002557' in message:
            print('  field likely upgraded already')
        else:
            print(e)
print('done')

print('removing {} domains'.format(len(delete_domains)))
for domain in delete_domains:
    try:
        arcpy.management.DeleteDomain(config.sde, domain)
    except ExecuteError as e:
        message, = e.args

        if 'ERROR 000800' in message:
            print('  domain already removed')
        else:
            print(e)
print('done')

tables = arcpy.ListFeatureClasses() + arcpy.ListTables()

for dataset in arcpy.ListDatasets('', 'Feature'):
    arcpy.env.workspace = os.path.join(config.sde, dataset)
    tables += arcpy.ListFeatureClasses()

skip_tables = ['Counties', 'ZipCodes', 'Municipalities']

print('updating editor tracking and versioning for {} tables'.format(len(tables) - len(skip_tables)))

for table_name in tables:
    parts = table_name.split('.')
    if parts[2] in skip_tables:
        continue

    arcpy.management.EnableEditorTracking(
        in_dataset=os.path.join(config.sde, table_name),
        creator_field='CreatedBy',
        creation_date_field='CreatedOn',
        last_editor_field='EditedBy',
        last_edit_date_field='ModifiedOn',
        add_fields='ADD_FIELDS',
        # record_dates_in='UTC',
    )

    arcpy.management.RegisterAsVersioned(
        in_dataset=os.path.join(config.sde, table_name),
        edit_to_base='NO_EDITS_TO_BASE',
    )
print('done')

print('creating contingent field group for well class')
try:
    arcpy.management.DeleteFieldGroup(
        target_table='UICWell',
        name='Well Class',
    )
except ExecuteError as e:
    message, = e.args

    if 'ERROR 002585' in message:
        pass
    else:
        print(e)

try:
    arcpy.management.CreateFieldGroup(
        target_table='UICWell',
        name='Well Class',
        fields=['WellClass', 'WellSubclass'],
    )
except ExecuteError as e:
    print(e)

print('done')

well_classes = [
    (1, 'Class I'),
    (3, 'Class III'),
    (4, 'Class IV'),
    (5, 'Class V'),
    (6, 'Class VI'),
]

domains = arcpy.da.ListDomains(config.sde)
well_subclass = [x for x in domains if x.name == 'UICWellSubClassDomain'][0].codedValues

print('adding well class contingent values')
arcpy.management.AddContingentValue(
    target_table='UICWell',
    field_group_name='Well Class',
    values=[['WellClass', 'ANY'], ['WellSubclass', 'NULL']],
)

codes = []
for code, _ in well_subclass.items():
    well_class = int(str(code)[:1])

    if well_class == 7:
        continue

    codes.append((well_class, code))

codes.sort(key=lambda x: x[1])

for well_class, code in codes:
    arcpy.management.AddContingentValue(
        target_table='UICWell',
        field_group_name='Well Class',
        values=[['WellClass', 'CODED_VALUE', well_class], ['WellSubclass', 'CODED_VALUE', code]],
    )
print('done')
