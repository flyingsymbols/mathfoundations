# intent here is to have a format that will handle storing to and from the
# users home directory as json, also clean to/from between basic python
# data structures (dict, list, int, float, str, etc)

# implemented as a decorator over functions
# don't need to show defaults... but defaults can change

import inspect
from collections import OrderedDict

def __init__(self): pass
bare_init = __init__

def kw_and_pos_args_from_func(func):
    """
    returns (kwarg_names, posarg_names)
    where 
     kwarg_names : [str]
     posarg_names : [str]
    """

def define(cls):
    """
    class decorator that takes a class with a function that has the same name as
    the class, and creates the __init__, __repr__, and __eq__ from it
    """
    cls_name = cls.__name__
    constructor = cls.__dict__[cls_name]

    sig = inspect.signature(constructor)
    cls.__sig__ = sig
    cls.__defaults__ = OrderedDict()
    cls.__pos_args__ = []
    cls.__kw_args__ = []

    for n, p in sig.parameters.items():
        if p.default != p.empty:
            cls.__defaults__[n] = p.default

        if p.kind == p.KEYWORD_ONLY or cls.__defaults__:
        # If we have seen defaults already, we treat everything as keyword
            cls.__kw_args__.append(n)
        elif p.kind == p.POSITIONAL_OR_KEYWORD:
            cls.__pos_args__.append(n)
        else:
            raise NotImplementedError(p.kind)

    if hasattr(cls, '__init__'):
        old_init = cls.__init__
    else:
        old_init = bare_init

    def __init__(self, *pvals, **kwvals):
        bound_args = sig.bind(*pvals, **kwvals)
        bound_args.apply_defaults()
        for k, v in bound_args.arguments.items():
            self.__dict__[k] = v

        old_init(self)

    def __attrs__(self):
        for n in self.__pos_args__:
            yield n

        for k in sorted(self.__kw_args__):
            yield k

    def __repr__(self):
        args = [repr(self.__dict__[n]) for n in self.__pos_args__]
        for k in self.__kw_args__:
            v = self.__dict__[k]
            if k not in self.__defaults__ or v != self.__defaults__[k]:
                args.append('%s=%r' % (k, v))

        param_str = ', '.join(args)

        return '%s(%s)' % (self.__class__.__name__, param_str)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        h = 0

        for k in self.__attrs__():
            v = getattr(self, k)
            h ^=  hash(k) ^ hash(v)
        
        return h

    cls.__init__ = __init__
    cls.__repr__ = __repr__
    cls.__eq__ = __eq__
    cls.__attrs__ = __attrs__
    cls.__hash__ = __hash__

    return cls


