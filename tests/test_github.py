#!/usr/bin/env python
import pytest


def test_compare_forks():
    pgu = pytest.importorskip('gitutils.github_repo_stats')

    if not pgu.check_api_limit():
        pytest.skip('GitHub API limit exceeded')

    repos, ahead = pgu.repo_prober('scivision/pymap3d')


if __name__ == '__main__':
    pytest.main(['-x', __file__])
