"""A scheme is a map from CSV formatted rows to Transaction objects."""
from datetime import datetime
from transaction import Transaction

def triodos(categorizer):
    """Get scheme for transforming Triodos CSV files."""

    def reader(row):
        amount = float(row[2].replace(",", "."))
        if (row[3] == "Debet"):
            amount = -amount
        date = datetime.strptime(row[0], "%d-%m-%Y")

        category = categorizer(row[4])
        if category is None:
            category = categorizer(row[7])

        if category is None:
            print("; ".join(row))

        return Transaction(date, row[1], amount, category)

    return reader

def rabobank(categorizer):
    """Get scheme for transforming Rabobank CSV files."""

    def reader(row):
        amount = float(row[4])
        if (row[3] == "D"):
            amount = -amount

        date = datetime.strptime(row[2], "%Y%m%d")
        return Transaction(date, row[0], amount, categorizer(row[10]))

    return reader
