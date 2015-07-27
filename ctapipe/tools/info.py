# Licensed under a 3-clause BSD style license - see LICENSE.rst
import sys
import logging
import importlib
from .utils import get_parser

__all__ = ['info']


def main(args=None):
    parser = get_parser(info)
    parser.add_argument('--version', action='store_true',
                        help='Print version number')
    parser.add_argument('--tools', action='store_true',
                        help='Print available command line tools')
    parser.add_argument('--dependencies', action='store_true',
                        help='Print available versions of dependencies')
    args = parser.parse_args(args)

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    info(**vars(args))


def info(version=False, tools=False, dependencies=False):
    """Print various info to the console.

    TODO: explain.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s')

    if version:
        _info_version()

    if tools:
        _info_tools()

    if dependencies:
        _info_dependencies()


def _info_version():
    """Print version info."""
    from ctapipe import version
    print('\n*** ctapipe version info ***\n')
    print('version: {0}'.format(version.version))
    print('release: {0}'.format(version.release))
    print('githash: {0}'.format(version.githash))
    print('')


def _info_tools():
    """Print info about command line tools."""
    print('\n*** ctapipe tools ***\n')

    # TODO: how to get a one-line description or
    # full help text from the docstring or ArgumentParser?
    # This is the function names, we want the command-line names
    # that are defined in setup.py !???
    from ctapipe.tools.utils import get_all_main_functions
    scripts = get_all_main_functions()
    names = sorted(scripts.keys())
    for name in names:
        print(name)

    print('')


def _info_dependencies():
    """Print info about dependencies."""
    print('\n*** ctapipe dependencies ***\n')
    from ctapipe.conftest import PYTEST_HEADER_MODULES

    for label, name in PYTEST_HEADER_MODULES.items():
        try:
            module = importlib.import_module(name)
            version = module.__version__
        except ImportError:
            version = 'not available'

        print('{:>20s} -- {}'.format(label, version))
