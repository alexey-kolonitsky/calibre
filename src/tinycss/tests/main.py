#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2014, Kovid Goyal <kovid at kovidgoyal.net>'

import unittest, os, argparse

def find_tests():
    return unittest.defaultTestLoader.discover(os.path.dirname(os.path.abspath(__file__)), pattern='*.py')

def run_tests(find_tests=find_tests):
    parser = argparse.ArgumentParser()
    parser.add_argument('name', nargs='?', default=None,
                        help='The name of the test to run')
    args = parser.parse_args()
    if args.name and args.name.startswith('.'):
        tests = find_tests()
        q = args.name[1:]
        if not q.startswith('test_'):
            q = 'test_' + q
        ans = None
        try:
            for suite in tests:
                for test in suite._tests:
                    if test.__class__.__name__ == 'ModuleImportFailure':
                        raise Exception('Failed to import a test module: %s' % test)
                    for s in test:
                        if s._testMethodName == q:
                            ans = s
                            raise StopIteration()
        except StopIteration:
            pass
        if ans is None:
            print ('No test named %s found' % args.name)
            raise SystemExit(1)
        tests = ans
    else:
        tests = unittest.defaultTestLoader.loadTestsFromName(args.name) if args.name else find_tests()
    r = unittest.TextTestRunner
    r(verbosity=4).run(tests)

if __name__ == '__main__':
    run_tests()

