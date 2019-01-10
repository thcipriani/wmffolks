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

    # This is probably still imperfect.
    #
    # The idea is to go over the page twice.
    #
    # Manager/Director types on the old staff page weren't in gallery
    # boxes, but mostly had user pages.
    #
    # Some folks in galleryboxes didn't have user pages.
    #
    # The set of folks with user pages OR in gallery boxes should be everybody
    # who was a staff or contractor including director-type-folks ¯\_(ツ)_/¯
    for div in soup.select('.gallerybox > div'):
        try:
            folks.add([x for x in div.children][3].text.strip())
        except:
            continue

    for a in soup.find_all('a'):
        try:
            href = a['href']
        except KeyError:
            continue
        if 'User:' not in href:
            continue
        folks.add(a.text.strip())

    ret = '{} WMF folks\n---'.format(len(folks))
    ret += '\n'
    ret += '\n'.join(sorted(folks))

    return ret

if __name__ == '__main__':
    print(current_folks())
