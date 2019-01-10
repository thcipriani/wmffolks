#!/usr/bin/env bash

BASEDIR="$(dirname $(readlink -f $0))"
GITDIR="$HOME/Projects/wmf-staff-and-contractors-historic"

python3 "${BASEDIR}/wmffolks/__init__.py" > "${GITDIR}/README"
git -C "${GITDIR}" add --all
git -C "${GITDIR}" commit --quiet -m "$(date -I)"
git -C "${GITDIR}" gc --quiet --auto
git -C "${GITDIR}" push https://github.com/thcipriani/wmffolks.git master
