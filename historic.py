#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import wmffolks
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('date', type=int)
    args = ap.parse_args()

    print(wmffolks.folks_at(args.date))
