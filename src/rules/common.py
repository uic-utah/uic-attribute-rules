#!/usr/bin/env python
# * coding: utf8 *
'''
common.py
A module that holds common arcade expressions
'''

__constain_to_domain = '''if (!haskey($feature, '{0}')) {{
    return true;
}}

return iif (isempty(domainname($feature, '{0}', $feature.{0})), {{
    'errorMessage': '{0} may not be <null>; select the appropriate value from the{1} domain (dropdown menu). Input: ' + $feature.{0}
}}, true);'''


def constrain_to_domain(field, domain=None):
    if domain is None:
        domain = ' '
    else:
        domain = ' ' + domain

    return __constain_to_domain.format(field, domain)
