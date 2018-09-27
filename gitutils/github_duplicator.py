from time import sleep
from pathlib import Path
import subprocess
import logging
import tempfile
from datetime import datetime
import webbrowser
from typing import Optional, Dict
from .github_base import github_session, check_api_limit, repo_exists, last_commit_date


def repo_dupe(repos: Dict[str, str], oauth: Path,
              orgname: str = None, stem: str = ''):
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
    for email, oldurl in repos.items():
        if not check_api_limit(sess):
            raise RuntimeError('GitHub API limit exceeded')

        oldurl = oldurl.replace('https', 'ssh')
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
        try:
            subprocess.check_call(['git', 'ls-remote', '--exit-code', oldurl],
                                  stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            logging.error(f'{oldurl} has no Wiki')
            return

    newname = f'{username}/{mirrorname}'
    newurl = f'ssh://github.com/{newname}'

    if not iswiki:
        exists = repo_exists(op, mirrorname)
        if exists:
            newrepo = op.get_repo(mirrorname)
            if newrepo.pushed_at >= oldtime:
                return

    else:
        try:
            subprocess.check_call(['git', 'ls-remote', '--exit-code', newurl],
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
            return
        except subprocess.CalledProcessError:
            exists = True

    print('\n', oldurl, '\n')

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
            dupewiki(tmprepo, oldurl, newurl)
        else:
            pwd = (tmprepo / (oldurl.split('/')[-1]))
            pwd = pwd.with_suffix('.git')

            cmd = ['git', 'push', '--mirror', newurl]
            subprocess.check_call(cmd, cwd=pwd)


def dupewiki(prepo: Path, oldurl: str, newurl: str):
    """
    Note: GitLab API has Wiki included, but at this time, GitHub API does not cover Wiki
    """
    pwd = (prepo / (oldurl.split('/')[-1]).split('.git')[0])

    subprocess.check_call(['git', 'remote', 'set-url', 'origin', newurl], cwd=pwd, stdout=subprocess.DEVNULL)

    browseurl = newurl
    browseurl = browseurl.replace('ssh', 'https').replace('.wiki.git', '/wiki')
    webbrowser.open_new_tab(browseurl)
    sleep(10.)  # TODO: use suprocess.run() instead of webbrowser

    subprocess.check_call(['git', 'push', '-f'], cwd=pwd)
