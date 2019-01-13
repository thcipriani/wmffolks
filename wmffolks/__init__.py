#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
wmf-folks
~~~~~~~~~
A naïve attempt to answer the burning question: *exactly* how many
people work at the Wikimedia Foundation now?
"""
import os
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests


class FolksFinder(object):
    """
    Base folksfinder
    """
    def __init__(self, date):
        self.date = date
        self.url = 'https://wikimediafoundation.org/role/staff-contractors/'
        self.page = self._fetch_page()
        self.folks = self._parse_page()

    def _fetch_page(self):
        raise NotImplementedError()
    def _parse_page(self):
        raise NotImplementedError()


class CurrentFolksFinder(FolksFinder):
    """
    Scrape the current staff page for folks
    """
    def _fetch_page(self):
        r = requests.get(self.url)
        if r.status_code != requests.codes.ok:
            return False

        return BeautifulSoup(r.text, 'html.parser')

    def _parse_page(self):
        if not self.page:
            return self.page

        folks = set()
        for a in self.page.find_all(attrs={'class': 'staff-list-item'}):
            person = a.text.strip().split('\n')[0]
            folks.add(person.strip())

        return folks


class TemplateFolksFinder(FolksFinder):
    """
    We used the staff template in 2010-08-18 all the way through 2018-07-31
    """
    def _fetch_page(self):
        params = {
            'titles': 'Template:Staff_and_contractors',
            'action': 'query',
            'prop': 'revisions',
            'rvprop': 'content',
            'rvslots': 'main',
            'formatversion': 2,
            'format': 'json',
            'rvstart': self.date.strftime('%Y%m%d000000')
        }
        r = requests.get('https://foundation.wikimedia.org/w/api.php', params=params)
        if r.status_code != requests.codes.ok:
            return False

        return r.json()

    def _parse_page(self):
        if not self.page:
            return self.page

        folks = set()

        revisions = self.page['query']['pages'][0]['revisions']
        content = revisions[0]['slots']['main']['content']

        for line in content.splitlines():
            if ('=' in line and
                    (line.startswith('| name ') or line.startswith('| head'))):
                folks.add(line.split('=')[-1].strip().split('|')[-1].rstrip('}]'))

        return folks


def at_date(date):
    """
    Parse the closest page to a given start date to find number of folks who worked here
    :date: YYYYMMDD
    """
    if not date or date == 'now':
        date = datetime.utcnow()
    else:
        date = parse(date)

    if ((date.year == 2018 and date.month > 8) or
            (date.year > 2018)):
        folk_finder = CurrentFolksFinder(date)

    if ((date.year == 2018 and date.month < 8) or
            (date.year == 2010 and date.month == 8 and date.day > 18) or
            (date.year == 2010 and date.month > 8) or
            (date.year < 2018 and date.year > 2010)):
        folk_finder = TemplateFolksFinder(date)

    if not folk_finder:
        raise RuntimeError('No scrapper for that date :(\nPull requests welcome though')

    return folk_finder.folks


def format_folks(folks):
    """
    Make printable output from folks set

    :folks: set of names
    """
    ret = '{} WMF folks\n---'.format(len(folks))
    ret += '\n'
    ret += '\n'.join(sorted(folks))
    return ret


if __name__ == '__main__':
    print(format_folks(at_date('now')))
