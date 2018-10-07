#!/usr/bin/env python
import pytest


def test_compare_forks():
    pgu = pytest.importorskip('gitutils.github_repo_stats')

    try:
        repos, ahead = pgu.repo_prober('scivision/gitutils')
    except RuntimeError:
        pytest.skip('GitHub API limit exceeded')


if __name__ == '__main__':
    pytest.main(['-x', __file__])
