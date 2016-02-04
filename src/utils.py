"""Utility functions that do not deal directly deal with the domain."""
from itertools import permutations
import sys
import inspect

def contains_function(mod, fn):
    """Return whether module contains a function"""
    return inspect.isfunction(fn) and inspect.getmodule(fn) == mod

def list_functions(mod):
    """List functions in module"""
    return [fn.__name__ for fn in mod.__dict__.itervalues()
                        if contains_function(mod, fn)]

def split(xs, fns):
    """Split xs into a forest.

    The trees in the forest are indexed by the distinct values of the
    first element of 'fn' on 'xs'. The leaves in those trees are
    indexed by the values of the second element of 'fn' on 'xs', etc.
    """
    if not fns:
        return xs
    result = {}
    for x in xs:
        result.setdefault(fns[0](x), []).append(x)
    tail_fns = fns[1:]
    for (key, xss) in result.items():
        result[key] = split(xss, tail_fns)
    return result

def scan(tree, f, r):
    """Reduce function value on leaves up the tree.

    The value on a leaf is the application of 'f' on that leaf. The
    value on an inner node is the reduction of the values of its
    children by 'r'.
    """
    if not isinstance(tree, dict):
        return (f(tree),)
    else:
        branches = {node: scan(branch, f, r) for (node, branch) in tree.items()}
        annotation = reduce(r, map(lambda branch: branch[0], branches.itervalues()))
        return (annotation, branches)

def test():
    xs = list(permutations([1, 2, 3, 4]))
    tree = split(xs, [lambda x: x[0], lambda x: x[1]])
    plus = lambda x, y: x + y
    summary = scan(tree, len, plus)
    print summary

if __name__ == "__main__":
    test()
