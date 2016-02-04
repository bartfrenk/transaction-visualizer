from collections import OrderedDict
import re

class Categorizer(object):
    """Function that assigns input strings to categories."""
    def __init__(self, categories):
        self.categories = OrderedDict([(cat[0], cat[1]) for cat in categories])

    def __call__(self, description):
        for (name, predicate) in self.categories.items():
                if predicate(description):
                    return name

def contains(*args):
    """Abstract the representation of a category matching on a set of keywords."""
    def predicate(description):
        for keyword in list(args):
            if keyword in description:
                return True
        return False
    return predicate
