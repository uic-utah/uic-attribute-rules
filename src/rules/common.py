#!/usr/bin/env python
# * coding: utf8 *
'''
common.py
A module that holds common arcade expressions
'''

__constain_to_domain = '''if (!haskey($feature, '{0}') || isempty($feature.{0})) {{
    return true;
}}

return iif (isempty(domainname($feature, '{0}', $feature.{0})), {{
    'errorMessage': 'Value does not fall within the allowable domain values. Input: ' + $feature.{0}
}}, true);'''


def constrain_to_domain(field):
    return __constain_to_domain.format(field)
