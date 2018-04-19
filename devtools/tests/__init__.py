from .web import *
from nose.tools import assert_equal

from ..formtools import tostr, tobytes, toaddr


def test_tostr_and_tobytes():
    s = 'aa'
    b = b'aa'
    assert_equal(tostr(s), tostr(b))
    assert_equal(tobytes(s), tobytes(b))


def test_toaddr():
    s = ['192', '333']
    assert_equal(toaddr(s), ('192', 333))
    s = '192:333'
    assert_equal(toaddr(s), ('192', 333))
