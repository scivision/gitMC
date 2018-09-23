from time import sleep
from pathlib import Path
import pandas
import subprocess
import tempfile
from .github_base import github_session, check_api_limit, repo_exists, last_commit_date


def repo_dupe(repos: pandas.Series, oauth: Path, orgname: str = '', stem: str = ''):
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
        newname = f'{username}/{mirrorname}'
        newurl = f'ssh://github.com/{newname}'

        exists = repo_exists(op, mirrorname)
        if exists:
            newrepo = op.get_repo(mirrorname)
            if newrepo.pushed_at >= oldtime:
                continue

        print('\n', email, oldurl, '\n')
        with tempfile.TemporaryDirectory() as d:
            tmprepo = Path(d)
            # 1. bare clone
            subprocess.check_call(['git', 'clone', '--bare', oldurl],
                                  stdout=subprocess.DEVNULL, cwd=tmprepo)

            # 2. create new repo
            if not exists:
                op.create_repo(name=mirrorname, private=True)

            # 3. mirror to new repo
            pwd = (tmprepo / (oldurl.split('/')[-1])).with_suffix('.git')
            cmd = ['git', 'push', '--mirror', newurl]
            subprocess.check_call(cmd, cwd=pwd)

        sleep(0.1)
