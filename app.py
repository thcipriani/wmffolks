#!/usr/bin/env python3
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
import wmffolks

from bottle import route, run, response

@route('/')
def current_folks():
    response.content_type = 'text/plain; charset=utf-8'
    return wmffolks.current_folks()

# YYYYMMdd
@route('/<date:re:20(0|1)[0-9]{5}>')
def folks_at(date):
    response.content_type = 'text/plain; charset=utf-8'
    return wmffolks.folks_at(date)

run(host='localhost', port=8080, debug=True)
