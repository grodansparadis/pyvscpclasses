# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
sys.path.append('../')
from vscp import *

def test_success():
    h1 = pyvscphlp_newSession()
    if (0 == h1 ):
        pyvscphlp_closeSession(h1)
    assert True

if __name__ == "__main__":
    test_success()
    print("Everything passed")