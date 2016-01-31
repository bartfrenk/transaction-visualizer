from collections import OrderedDict
import re

class Categorizer:
    def __init__(self, categories):
        self.categories = OrderedDict([(cat[0], re.compile(cat[1])) for cat in categories])

    def __call__(self, description):
        for (name, regex) in self.categories.items():
            if not regex.match(description) == None:
                return name
