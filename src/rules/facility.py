#!/usr/bin/env python
# * coding: utf8 *
'''
facility.py
A module that creates attribute rules for the UICFacility table
'''

from config import config
from services.loader import load_rule_for
from models.ruletypes import Calculation, Constant, Constraint

TABLE = 'UICFacility'
FOLDER = 'facility'

guid_constant = Constant('Facility Guid', 'GUID', 'Facility.Guid', 'Guid()')

fips_calculation = Calculation('County Fips', 'CountyFIPS', 'Facility.FIPS', load_rule_for(FOLDER, 'fipsCalculation'))

id_calculation = Calculation('Facility Id', 'FacilityID', 'Facility.Id', load_rule_for(FOLDER, 'idCalculation'))
id_calculation.triggers = [config.triggers.insert, config.triggers.update]
id_calculation.editable = config.editable.no

city_calculation = Calculation('Facility City', 'FacilityCity', 'Facility.City', load_rule_for(FOLDER, 'cityCalculation'))

zip_calculation = Calculation('Facility Zip', 'FacilityZIP', 'Facility.ZipCode', load_rule_for(FOLDER, 'zipCalculation'))

fips_domain_constraint = Constraint('County Fips', 'Facility.FIPS', load_rule_for(FOLDER, 'fipsConstraint'))
fips_domain_constraint.triggers = [config.triggers.insert, config.triggers.update]

zip_domain_calculation = Constraint('Facility Zip', 'Facility.ZipCode', load_rule_for(FOLDER, 'zipConstraint'))
zip_domain_calculation.triggers = [config.triggers.insert, config.triggers.update]

RULES = [
    guid_constant,
    fips_calculation,
    id_calculation,
    city_calculation,
    zip_calculation,
    fips_domain_constraint,
    zip_domain_calculation,
]
