import csv
import sys
from collections import OrderedDict
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

import pdb

class Category:

    cats = {
        "mortgage": [],
        "groceries": ["Jumbo", "AH", "Market"],
        "car": [],
        "insurance": [],
        "transfer": []
    }

    @staticmethod
    def classify(description):
        for (cat, keywords) in cats.items():
            for word in keywords:
                if word in description:
                    return cat;
        return None

class Transaction:

    DISPLAY = "date: %s; src: %s; amount: %f"


    def __init__(self, date, src, amount, cat=None):
        self.src = src
        self.amount = amount
        self.date = date
        self.cat = cat

    def __str__(self):
        return Transaction.DISPLAY % (self.date.strftime("%Y-%m-%d"), self.src, self.amount)

    @staticmethod
    def read(scheme, path, header=True):
        with open(path, "rb") as stored:
            reader = csv.reader(stored)
            if header: reader.next()
            return [scheme(row) for row in reader]


def triodos(row):
    amount = float(row[2].replace(",", "."))
    if (row[3] == "Debet"):
        amount = -amount

    date = datetime.strptime(row[0], "%d-%m-%Y")
    return Transaction(date, row[1], amount, Category.classify(row[7]))

def cumulative_sum(xs, initial=0):
    result = [initial]
    for x in xs:
        result.append(result[-1] + x)
    return result

def split(transactions, classifier):
    result = {}
    for transaction in transactions:
        if classifier in result:
            # use setdefault
            result[classifier].append(transaction)
        else:
            result[classifier] = [transaction]
    return result

def show_cumulative(history):
    """Show cumulative transaction totals in plot."""
    balances = cumulative_sum([trans.amount for trans in history])
    plt.plot_date(dates, balances[1:], "b-")
    plt.show()

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print "syntax: " + sys.argv[0].split("/")[-1] + " <csv file>"
    else:
        history = Transaction.read(triodos, sys.argv[1])
        dates = matplotlib.dates.date2num([trans.date for trans in history])
        show_cumulative(history)
#        per_month = split(history, lambda tr: tr.date.month)
