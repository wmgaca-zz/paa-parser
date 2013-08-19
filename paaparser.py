#!/usr/bin/env python

# coding=utf8

import sys
import csv
import pickle
from pprint import pprint

TAXONOMY_MAP = pickle.load(open('taxonomy_map.pickle'))

TAXONOMY_SECT = pickle.load(open('taxonomy_sect_to_rootlist.pickle'))


SECTION_CODE_TO_NAME = {
    'CL': 'Classifieds',
    'CO': 'Community',
    'SP': 'Property for Sale',
    'JW': 'Jobs Wanted',
    'MT': 'Motors',
    'RP': 'Residential Property',
    'JB': 'Jobs',
}

SECTION_NAME_TO_CODE = dict([(v.lower(), k) for k, v in SECTION_CODE_TO_NAME.items()])


class Type(object):

    SECTION = 0
    DESC = 1
    DESC_HINT = 2
    MAP_HINT = 3


def get_section_code(section_name):
    section_name = section_name.strip().lower()
    
    return SECTION_NAME_TO_CODE[section_name]
    

def get_subsection_code(subsection_name, section_code):
    for k, v in TAXONOMY_MAP.items():
        if v[3] != section_code:
            continue
        elif v[4]:
            continue

        if subsection_name.strip().lower() == str(v[0]).strip().lower():
            return k


def is_header(row):
    return not row[Type.SECTION] and all(row[Type.DESC:])


def is_section(row):
    return row[Type.SECTION] and not any(row[Type.DESC:])


def is_data(row):
    return row[Type.SECTION] and any(row[Type.DESC:])


def format_desc(desc):
    if desc.startswith('*'):
        return ''.join(list(desc)[1:]).strip()
    elif desc.startswith('['):
        return '__callback'

    return 'Describe your %s' % desc.strip()


def format_desc_hint(desc_hint):
    return desc_hint.strip().split('\n')[0]

def format_map_hint(map_hint):
    if map_hint.startswith('*'):
        return ''.join(list(map_hint)[1:]).strip()

    return 'Locate your %s' % map_hint


def parse(data_path):
    reader = csv.reader(open(data_path, 'rb'), delimiter=',')

    section = None
    data = {}
    for row in reader:
        if is_header(row):
            continue
        elif is_section(row):
            section = get_section_code(row[Type.SECTION])

            if section not in data:
                data[section] = {}
            else:
                raise NotImplementedError('Big Bad Error #2')

            continue
        elif is_data(row):
            subsection = get_subsection_code(row[Type.SECTION], section)
            if subsection not in data[section]:
                data[section][subsection] = tuple([format_desc(row[Type.DESC]), 
                                                   format_desc_hint(row[Type.DESC_HINT]), 
                                                   format_map_hint(row[Type.MAP_HINT])])
            else:
                raise NotImplementedError('Big Bad Error #3')

        else:
            raise NotImplementedError('Big Bad Error')

    with open('data.py', 'w+') as f:
        f.write('_PRODUCT_FORM_DATA = ')
        pprint(data, f)


if __name__ == '__main__':
    parse(sys.argv[1])
