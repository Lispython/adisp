#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
adisp
~~~~~

Adisp is a library that allows structuring code with asynchronous calls and
callbacks without defining callbacks as separate functions.

:copyright: (c) 2009 - 2013 by Ivan Sagalaev.
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/adisp
"""

__all__ = ('CallbackDispatcher', 'process', 'async')
__author__ = "Ivan Sagalaev"
__license__ = "BSD, see LICENSE for more details"
__version_info__ = (0, 0, 4)
__build__ = 0x000004
__version__ = ".".join(map(str, __version_info__))
__maintainer__ = "Alexandr Lispython (alex@obout.ru)"


def get_version():
    return __version__

from functools import partial

class CallbackDispatcher(object):
    def __init__(self, generator):
        self.g = generator
        try:
            self.call(self.g.next())
        except StopIteration:
            pass

    def _send_result(self, results, single):
        try:
            result = results[0] if single else results
            self.call(self.g.send(result))
        except StopIteration:
            pass

    def call(self, callers):
        single = not hasattr(callers, '__iter__')
        if single:
            callers = [callers]
        self.call_count = len(list(callers))
        results = [None] * self.call_count
        if self.call_count == 0:
            self._send_result(results, single)
        else:
            for count, caller in enumerate(callers):
                caller(callback=partial(self.callback, results, count, single))

    def callback(self, results, index, single, arg):
        self.call_count -= 1
        results[index] = arg
        if self.call_count > 0:
            return
        self._send_result(results, single)

def process(func):
    def wrapper(*args, **kwargs):
        CallbackDispatcher(func(*args, **kwargs))
    return wrapper

def async(func, cbname='callback', cbwrapper=lambda x: x):
    def wrapper(*args, **kwargs):
        def caller(callback):
            kwargs[cbname] = cbwrapper(callback)
            return func(*args, **kwargs)
        return caller
    return wrapper
