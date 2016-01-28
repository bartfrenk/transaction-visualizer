"""Utility functions that do not deal directly deal with the domain."""
import sys
import inspect

def contains_function(mod, fn):
    return inspect.isfunction(fn) and inspect.getmodule(fn) == mod

def list_functions(mod):
    return [fn.__name__ for fn in mod.__dict__.itervalues()
                        if contains_function(mod, fn)]
