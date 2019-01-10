#!/usr/bin/env bash
export GIT_WORKTREE="$HOME/Projects/wmf-staff-and-contractors-historic"

# Initialize a new git repo
mkdir -p "$GIT_WORKTREE"
git -C "$GIT_WORKTREE" init

# The rough shelf-life of the wikimediafoundation wiki
START_DATE='20120101'
END_DATE='20180701'

MONTHS_TO_ADD=0
DATE="$START_DATE"

while [[ "$DATE" != "$END_DATE" ]]; do
    RFC5322_DATE="$(date -R --date="$DATE")"

    echo "getting info for $DATE"
    FOLKS=$(python3 historic.py "$DATE")

    if [[ "$FOLKS" != "False" ]]; then
        echo "$FOLKS" > "${GIT_WORKTREE}/README"
    fi

    echo "committing $DATE"
    DIFF_FOLKS="$(grep folks "${GIT_WORKTREE}/README")"
    COMMIT_MESSAGE="$RFC5322_DATE ($DIFF_FOLKS)"

    git -C "${GIT_WORKTREE}" add --all
    git -C "${GIT_WORKTREE}" commit --quiet --date "$RFC5322_DATE" -m "$COMMIT_MESSAGE"
    git -C "${GIT_WORKTREE}" gc --quiet --auto

    # Advance dates by a month
    (( MONTHS_TO_ADD++ ))
    DATE="$(date +'%Y%m%d' --date="${START_DATE} ${MONTHS_TO_ADD} month")"
done
