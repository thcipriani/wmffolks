#!/usr/bin/env bash

BASEDIR="$(dirname $(readlink -f $0))"

python "${BASEDIR}/wmf-folks" > "${BASEDIR}/README"
git -C "${BASEDIR}" add --all
git -C "${BASEDIR}" commit --quiet -m "$(date -I)"
git -C "${BASEDIR}" gc --quiet --auto
git -C "${BASEDIR}" push https://github.com/thcipriani/wmffolks.git master
