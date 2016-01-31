"""Defines transactions, transaction transformations and visualizations."""
import csv
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict

"""Represents in a single transaction in a unified format."""
class Transaction:

    DISPLAY = "date: %s; src: %s; amount: %f; category: %s"

    def __init__(self, date, dest, amount, cat=None):
        self.dest = dest
        self.amount = amount
        self.date = date
        self.cat = cat

    def __str__(self):
        return Transaction.DISPLAY % (self.date.strftime("%Y-%m-%d"), self.src, self.amount, self.cat)

    @staticmethod
    def read(scheme, path, header=True):
        with open(path, "rb") as stored:
            reader = csv.reader(stored)
            if header: reader.next()
            return [scheme(row) for row in reader]

def cumulative_sum(xs, initial=0):
    result = [initial]
    for x in xs:
        result.append(result[-1] + x)
    return result

# TODO: not transaction specific, move to utils
def split(transactions, classifier):
    result = {}
    for transaction in transactions:
        transaction_class = classifier(transaction)
        if transaction_class in result:
            # use setdefault
            result[transaction_class].append(transaction)
        else:
            result[transaction_class] = [transaction]
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

def summarize(history):
    """Compute transactions totals per month and category."""
    tree = split(history, [lambda t: (t.date.year, t.date.month), lambda t: t.cat])
    totm = [(month, total_amount(ts)) for month, ts in tsm.items()]
    totm.sort()
    return OrderedDict(totm)

def show_total_amount_per_month(history):
    totm = totals_per_month(history).items()
    for month, total in totm:
        print "%02d-%02d:\t%f" % (month[0], month[1], total)

def total_amount(history):
    return sum(t.amount for t in history)
