#!/usr/bin/env bash

BASEDIR="$(dirname $(readlink -f $0))"

python3 "${BASEDIR}/wmffolks/__init__.py" > "${BASEDIR}/README"
git -C "${BASEDIR}" add --all
git -C "${BASEDIR}" commit --quiet -m "$(date -I)"
git -C "${BASEDIR}" gc --quiet --auto
git -C "${BASEDIR}" push https://github.com/thcipriani/wmffolks.git master
