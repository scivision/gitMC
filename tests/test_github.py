#!/usr/bin/env python
"""
maximum Github username length ~39 characters
"""
import pytest
import random
import string

random_username = ''.join(random.choice(string.ascii_lowercase) for i in range(32))
OK_username = 'scivision'


def test_bad_username():
    pgu = pytest.importorskip('gitutils.github_base')
    with pytest.raises(ValueError):
        pgu.user_or_org(pgu.github_session(), random_username)


def test_get_repos():
    pgu = pytest.importorskip('gitutils.github_base')
    userorg = pgu.user_or_org(pgu.github_session(), OK_username)
    try:
        repos = pgu.get_repos(userorg)
    except ConnectionRefusedError:
        pytest.skip('GitHub API limit exceeded')

    assert len(repos) > 0


if __name__ == '__main__':
    pytest.main(['-x', __file__])
