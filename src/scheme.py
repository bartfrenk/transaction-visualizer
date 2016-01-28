"""A scheme is a map from CSV formatted rows to Transaction objects."""
from datetime import datetime
from transaction import Transaction

def triodos(row):
    """Scheme for transforming Triodos CSV files."""
    amount = float(row[2].replace(",", "."))
    if (row[3] == "Debet"):
        amount = -amount

    date = datetime.strptime(row[0], "%d-%m-%Y")
    return Transaction(date, row[1], amount)

def rabobank(row):
    """Scheme for transforming Rabobank CSV files."""
    amount = float(row[4])
    if (row[3] == "D"):
        amount = -amount

    date = datetime.strptime(row[2], "%Y%m%d")
    return Transaction(date, row[0], amount)
