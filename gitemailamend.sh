#!/bin/bash
# Don't run this script till you understand consequences of rebase.
# Everyone will have to reclone
#
# Note that "noreply@github.com" comes from making commits from the website.
# it doesn't seem to impact commit count?
#
# https://help.github.com/articles/changing-author-info/
# https://www.git-tower.com/learn/git/faq/change-author-name-email

git filter-branch -f --env-filter '
WRONG_EMAIL='"$1"'
NEW_NAME='"$2"'
NEW_EMAIL="'"$2"'@users.noreply.github.com"

if [ "$GIT_COMMITTER_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$NEW_NAME"
    export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$WRONG_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$NEW_NAME"
    export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
