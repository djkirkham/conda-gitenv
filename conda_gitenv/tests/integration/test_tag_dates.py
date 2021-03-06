import contextlib
import os
import textwrap
import unittest
from subprocess import check_call

import conda_gitenv.tests.integration.setup_samples as setup_samples
from conda_gitenv.tag_dates import tag_by_branch


class Test_tag_by_date(unittest.TestCase):
    def test(self):
        repo = setup_samples.create_repo('tag_by_date')
        env = repo.create_head('manifest/example_env')
        new_tags = list(tag_by_branch(repo))
        self.assertEqual(len(new_tags), 1)
        self.assertEqual(new_tags[0].commit, env.commit)


class Test_cli(unittest.TestCase):
    def test(self):
        repo = setup_samples.create_repo('tag_by_date')
        env = repo.create_head('manifest/example_env')
                 
        check_call(['conda', 'gitenv', 'autotag', repo.working_dir])

        self.assertEqual(repo.tags[0].commit, env.commit)


if __name__ == '__main__':
    unittest.main()
