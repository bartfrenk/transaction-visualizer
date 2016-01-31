from transaction import Transaction, plot_cumulative_amount, split, show_total_amount_per_month
from utils import list_functions
from collections import OrderedDict
from categorizer import Categorizer

import sys
import scheme

CAT = Categorizer([
    ("child-care", "bla"),
    ("groceries", ".*[AH|Jumbo].*"),
    ("misc", ".*")
])

# TODO: make GUI (using Tkinter?)

# TODO: this depends too much of the internals of the scheme module
def derive_schemes(argv):
    """Returns the schemes that might apply to the arguments."""
    if len(argv) < 2:
        return []
    return [getattr(scheme, name) for name in list_functions(scheme)
                                  if name in argv[1]]

def main(argv):
    """Visualizes command line specified transaction data."""
    if (len(argv) != 2):
        print "syntax: " + argv[0].split("/")[-1] + " <csv file>"
    else:
        schemes = derive_schemes(argv)
        if (len(schemes) == 0):
            print("Cannot derive transaction format from input arguments.""")
        elif len(schemes) > 1:
            print("Multiple transaction formats might apply to the input.""")
        else:
            history = Transaction.read(schemes[0](CAT), argv[1])
            history.sort(key=lambda t: t.date)
            plot_cumulative_amount({None: history})

if __name__ == "__main__":
    main(sys.argv)
