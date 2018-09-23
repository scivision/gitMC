from time import sleep
from pathlib import Path
import pandas
import subprocess
import tempfile
from datetime import datetime
import webbrowser
from typing import Optional
from .github_base import github_session, check_api_limit, repo_exists, last_commit_date


def repo_dupe(repos: pandas.Series, oauth: Path,
              orgname: str = '', stem: str = ''):
    """
    fn: .xlsx file with repos to duplicate
    oauth: Path to your GitHub Oauth token  https://github.com/settings/tokens
    orgname: create repos under Organization instead of username
    stem: what to start new repo name with
    """
# %% authenticate
    sess = github_session(oauth)
    guser = sess.get_user()

    org = None
    if orgname:
        orgs = list(guser.get_orgs())
        for o in orgs:
            if o.login == orgname:
                org = o
                break

        assert org is not None
        op = org
    else:
        op = guser

    username = op.login

    if not check_api_limit(sess):
        raise RuntimeError('GitHub API limit exceeded')
# %% prepare to loop over repos
    for email, row in repos.iterrows():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        oldurl = row.item().replace('https', 'ssh')
        oldname = '/'.join(oldurl.split('/')[-2:]).split('.')[0]

        oldtime = last_commit_date(sess, oldname)
        if oldtime is None:
            continue

        mirrorname = stem + email

        gitdupe(oldurl, oldtime, username, mirrorname, op)
        gitdupe(oldurl, None, username, mirrorname, op, iswiki=True)

        sleep(0.1)


def gitdupe(oldurl: str, oldtime: Optional[datetime],
            username: str, mirrorname: str, op, iswiki: bool = False):

    if iswiki:
        oldurl += '.wiki.git'
        mirrorname += '.wiki.git'

    newname = f'{username}/{mirrorname}'
    newurl = f'ssh://github.com/{newname}'

    if not iswiki:
        exists = repo_exists(op, mirrorname)
        if exists:
            newrepo = op.get_repo(mirrorname)
            if newrepo.pushed_at >= oldtime:
                return

        print('\n', oldurl, '\n')
    else:
        try:
            subprocess.check_call(['git', 'ls-remote', '--exit-code', newurl])
            return
        except subprocess.CalledProcessError:
            exists = True

    with tempfile.TemporaryDirectory() as d:
        tmprepo = Path(d)
        # 1. bare clone
        cmd = ['git', 'clone', oldurl] if iswiki else ['git', 'clone', '--bare', oldurl]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, cwd=tmprepo)

        # 2. create new repo
        if not exists:
            op.create_repo(name=mirrorname, private=True, has_wiki=True)

        # 3. mirror to new repo

        if iswiki:
            pwd = (tmprepo / (oldurl.split('/')[-1]).split('.git')[0])

            subprocess.check_call(['rm', '-rf', '.git'], cwd=pwd)
            subprocess.check_call(['git', 'init'], cwd=pwd)
            subprocess.check_call(['git', 'remote', 'add', 'origin', newurl], cwd=pwd)
            subprocess.check_call(['git', 'add', '.'], cwd=pwd)
            subprocess.check_call(['git', 'commit', '-am', 'duplicate'], cwd=pwd)

            browseurl = newurl
            browseurl = browseurl.replace('ssh', 'https').replace('.wiki.git', '/wiki')
            webbrowser.open_new_tab(browseurl)

            subprocess.check_call(['git', 'push', '-f', '-u', 'origin', 'master'], cwd=pwd)
        else:
            pwd = (tmprepo / (oldurl.split('/')[-1]))
            pwd = pwd.with_suffix('.git')

            cmd = ['git', 'push', '--mirror', newurl]
            subprocess.check_call(cmd, cwd=pwd)
