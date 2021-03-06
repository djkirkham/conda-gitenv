import contextlib
import os
import textwrap
import unittest

from git import Repo
from conda_gitenv import resolve


class Test_full_build(unittest.TestCase):
    @contextlib.contextmanager
    def create_repo(self):
        with resolve.tempdir() as tmpdir:
            repo = Repo.init(tmpdir)
            repo.index.commit('Initial commit.')
            yield repo

    def add_env(self, repo, name, spec):
        branch = repo.create_head(name)
        branch.checkout()
        env_spec = os.path.join(repo.working_dir, 'env.spec')
        with open(env_spec, 'w') as fh:
            fh.write(textwrap.dedent(spec))
        repo.index.add([env_spec])
        repo.index.commit('Add {} spec'.format(name))

    def test_single_env(self):
        with self.create_repo() as repo:
            self.add_env(repo, 'master', """
            env:
             - python
            channels:
             - defaults 
            """)
            resolve.build_manifest_branches(repo)

            self.assertIn('manifest/master', repo.branches)
            manifest = repo.branches['manifest/master']
            manifest.checkout()
            with open(os.path.join(repo.working_dir, 'env.manifest'), 'r') as fh:
                manifest_contents = fh.readlines()
            pkg_names = [pkg.split('\t', 1)[1].split('-')[0] for pkg in manifest_contents]
            self.assertIn('python', pkg_names)
            self.assertIn('zlib', pkg_names)


if __name__ == '__main__':
    unittest.main()
