"""Defines transactions, transaction transformations and visualizations."""
from __future__ import print_function

import csv
import matplotlib.pyplot as plt
import matplotlib
from utils import split, scan
from collections import OrderedDict

class Transaction(object):
    """Data object that represents a bank transaction."""

    DISPLAY = "date: %s; src: %s; amount: %.2f; category: %s"

    def __init__(self, date, dest, amount, cat=None):
        self.dest = dest
        self.amount = amount
        self.date = date
        self.cat = cat

    def __str__(self):
        return Transaction.DISPLAY % (self.date.strftime("%Y-%m-%d"), self.dest, self.amount, self.cat)

    @property
    def month(self):
        return Month(self.date.year, self.date.month)

    @staticmethod
    def read(scheme, path, header=True):
        with open(path, "rb") as stored:
            reader = csv.reader(stored)
            if header: reader.next()
            return [scheme(row) for row in reader]

class Month(object):
    """Represents a specific month in history."""

    DISPLAY = "%02d-%02d"

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def __str__(self):
        return Month.DISPLAY % (self.year, self.month)

    def __lt__(self, other):
        return True if self.year < other.year else self.month < other.month

    def __eq__(self, other):
        return self.year == other.year and self.month == other.month

    def __hash__(self):
        return 12 * self.year + self.month - 1

def cumulative_sum(xs, initial=0):
    result = [initial]
    for x in xs:
        result.append(result[-1] + x)
    return result

def plot_cumulative_amount(histories, colors=None):
    """Show cumulative transaction totals in plot, one line for each history."""
    if colors == None:
        colors = ["r", "b"]
    for (i, history) in enumerate(histories.itervalues()):
        balances = cumulative_sum([t.amount for t in history])
        dates = matplotlib.dates.date2num([t.date for t in history])
        plt.plot_date(dates, balances[1:], colors[i] + "-")
    plt.show()

def print_summary(history, hierarchy):
    """Split transaction summary per month and category."""

    def mkstring(value):
        return "%.2f (%d)" % (value[0], value[1])

    def print_tree(node, indent="\t", level=0):
        print(mkstring(node[0]))
        if len(node) > 1:
            for (label, branch) in sorted(node[1].items()):
                print(indent * level + str(label), end=": ")
                print_tree(branch, indent, level + 1)

    tree = split(history, hierarchy)
    statistics = lambda ts: [sum(t.amount for t in ts), len(ts)]
    summary = scan(tree, statistics, lambda xs, ys: [x + y for (x, y) in zip(xs, ys)])
    print("total", end=": ")
    print_tree(summary)

def show_total_amount_per_month(history):
    totm = totals_per_month(history).items()
    for month, total in totm:
        print("%02d-%02d:\t%f" % (month[0], month[1], total))

def total_amount(history):
    return sum(t.amount for t in history)
