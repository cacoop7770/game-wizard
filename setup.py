"""
  ________       .__ ____  __.      .__
 /  _____/_____  |__|    |/ _|____  |__|
/   \  ___\__  \ |  |      < \__  \ |  |
\    \_\  \/ __ \|  |    |  \ / __ \|  |
 \______  (____  /__|____|__ (____  /__|
        \/     \/           \/    \/

Copyright 2013-2018 Gaikai Inc, a Sony Computer Entertainment company
"""

import subprocess
import os
import sys

from os.path import isdir, islink, relpath, dirname, realpath

from setuptools import setup, Command

### Created by projmaker.py on 2018-07-25 18:55:26.792510

class GaikaiCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class PyTest(GaikaiCommand):
    user_options = [('match=', 'k', 'Run only tests that match the provided expressions')]

    def initialize_options(self):
        self.match = None

    def run(self):
        cli_options = ['-k', self.match] if self.match else []

        testpath = 'src/test'
        buildlink = 'build/lib/test'

        if isdir(dirname(buildlink)):
            if islink(buildlink):
                os.unlink(buildlink)

            os.symlink(relpath(testpath, dirname(buildlink)), buildlink)
            testpath = buildlink

        try:
            covSrcPaths = ['--cov=' + os.path.join(dirname(testpath), p) for p in []]

            os.environ['EPYTHON'] = 'python{}.{}'.format(sys.version_info.major, sys.version_info.minor)
            errno = subprocess.call(['py.test', '-v', testpath] + covSrcPaths + cli_options +
                                    ['--cov-report=html', '--cov-report=term'])
            raise SystemExit(errno)

        finally:
            if islink(buildlink):
                os.unlink(buildlink)


class PyLint(GaikaiCommand):
    user_options = [('errorsonly', 'E', 'Check only errors with pylint'),
                    ('format=', 'f', 'Change the output format')]

    def initialize_options(self):
        self.errorsonly = 0
        self.format = 'colorized'

    def run(self):
        standaloneModules = [m for m in []]
        cli_options = ['-E'] if self.errorsonly else []
        cli_options.append('--output-format={0}'.format(self.format))
        pkgdir = 'build/lib' if isdir('build/lib') else 'src'
        os.environ['EPYTHON'] = 'python{}.{}'.format(sys.version_info.major, sys.version_info.minor)
        errno = subprocess.call(['pylint', '--rcfile=/etc/pylintrc',
                                "--msg-template='{C}:{msg_id}:{line:3d},{column}: {obj}: {msg} ({symbol})'"] +
                                cli_options + [] + standaloneModules, cwd=realpath(pkgdir))
        raise SystemExit(errno)


class SphinxDoc(GaikaiCommand):
    def run(self):
        os.environ['EPYTHON'] = 'python{}.{}'.format(sys.version_info.major, sys.version_info.minor)
        errno = subprocess.call(['make', 'html'], cwd='./doc')
        raise SystemExit(errno)


setup(name='survey',
    version='0.0.1',
    description='Your description here',
    long_description='Your long description here',
    author='Jeremy Cooper',
    author_email='<jeremy.cooper@sony.com>',
    package_dir={'': 'src'},
    packages=[],
    platforms='Posix',
    cmdclass={'test': PyTest, 'lint': PyLint, 'doc': SphinxDoc},
)
