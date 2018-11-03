import re

import pytest

from dsmath.types import define
import dsmath.types as T

def test_define():
    @define
    class Foo: 
        def Foo(k, t): pass

    f = Foo('a', 1)

    assert repr(f) == "Foo('a', 1)"
    assert f == Foo('a', 1)
    assert f != Foo('a', 2)

def test_define_with_types():
    """
    Nat(x) allows [0, x-1]
    Count(x) allows [1, x]
    """
    @define
    class Foo:
        def Foo(k: T.Nat(5)): pass

    with pytest.raises(
        TypeError, match=re.escape('6 is not in Nat(5): must be in [0, 4]')
    ): Foo(6)
    assert repr(Foo(4)) == "Foo(4)"

    @define
    class Foo2: 
        def Foo2(v: int): pass

    with pytest.raises(
        TypeError, match=re.escape("'a' is not in int")
    ): Foo2('a')
    assert repr(Foo2(500)) == "Foo2(500)"

def test_init():
    @define
    class Foo:
        def Foo(k, t): pass
        def __init__(self):
            self.pair = (self.k, self.t)

    f = Foo('a', 1)

    assert f.pair == ('a', 1)

def test_as_dict_key():
    @define
    class Pair:
        def Pair(a, b): pass

    d = {}

    d[Pair(1, 2)] = 1
    d[Pair(1, 2)] = 2

    assert d[Pair(1, 2)] == 2

