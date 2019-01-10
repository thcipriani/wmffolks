#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
wmf-folks
~~~~~~~~~
A naïve attempt to answer the burning question: *exactly* how many
people work at the Wikimedia Foundation now?
"""
import os

import requests

from bs4 import BeautifulSoup

CURRENT_STAFF_PAGE = 'https://wikimediafoundation.org/role/staff-contractors/'
ARCHIVE_ORG_AVAILABLE_API = 'http://archive.org/wayback/available?url='
OLD_STAFF_PAGE = 'https://wikimediafoundation.org/wiki/Staff_and_Contractors'

def _get_closest_archive_page(date):
    """
    Find the closest archived page for a given date

    :date: YYYYMMDD
    """
    r = requests.get('{}{}&timestamp={}'.format(
        ARCHIVE_ORG_AVAILABLE_API, OLD_STAFF_PAGE, date))
    if r.status_code != requests.codes.ok:
        return False
    old_page_json = r.json()
    if not old_page_json['archived_snapshots']:
        return False
    return old_page_json['archived_snapshots']['closest']


def current_folks():
    """
    Count up the folks on the current staff page
    """
    r = requests.get(CURRENT_STAFF_PAGE)
    if r.status_code != requests.codes.ok:
        return False
    folks = set()

    soup = BeautifulSoup(r.text, 'html.parser')

    for a in soup.find_all(attrs={'class': 'staff-list-item'}):
        person = a.text.strip().split('\n')[0]
        folks.add(person.strip())

    ret = '{} WMF folks\n---'.format(len(folks))
    ret += '\n'
    ret += '\n'.join(sorted(folks))
    return ret


def folks_at(date):
    """
    Parse the closest page to a given start date to find number of folks who worked here
    :date: YYYYMMDD
    """
    closest_page = _get_closest_archive_page(date)
    if not closest_page:
        return False
    r = requests.get(closest_page['url'])
    if r.status_code != requests.codes.ok:
        return False
    folks = set()

    soup = BeautifulSoup(r.text, 'html.parser')
    for l in soup.find_all(attrs={'class': 'gallerybox'}):
        person = l.attrs['id']
        folks.add(person.strip())

    ret = '{} WMF folks'.format(len(folks))
    ret += ' (as of {})'.format(closest_page['timestamp'])
    ret += '\n---\n'
    ret += '\n'.join(sorted(folks))
    return ret

if __name__ == '__main__':
    print(current_folks())
