#!/usr/bin/env bash

BASEDIR="$(dirname $(readlink -f $0))"

python "${BASEDIR}/wmf-folks" > "${BASEDIR}/README"
git add --all
git commit --quiet -m "$(date -I)"
git gc --quiet --auto
