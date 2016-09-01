#!/bin/bash
# Don't run this script till you understand consequences of rebase -- everyone will have to reclone
#
# https://www.git-tower.com/learn/git/faq/change-author-name-email

git filter-branch -f --env-filter '
WRONG_EMAIL="nobody@github.com"
NEW_NAME="scienceopen"
NEW_EMAIL="scienceopen@users.noreply.github.com"

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
