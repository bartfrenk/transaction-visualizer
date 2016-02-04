from transaction import Transaction, plot_cumulative_amount, print_summary
from utils import list_functions
from collections import OrderedDict
from categorizer import Categorizer, contains

import sys
import scheme


CAT = Categorizer([
    ("child care", contains("Mare Gastouderbureau", "Mare")),
    ("groceries", contains("AH", "Jumbo", "Ekoplaza", "Lidl",
                           "Genneper Hoeve", "Kruidvat", "EkoPlaza",
                           "Yasar Market", "Amazing Oriental",
                           "Olienoot", "Aldi", "ALBERT HEIJN")),
    ("shopping", contains("Prenatal", "Mediamarkt", "MediaMarkt",
                          "Xenos", "Handyman", "HEMA", "Apotheek",
                          "PRAXIS", "Gamma", "Baby-Dump")),
    ("restaurants", contains("CoffeeYou", "RESTAURANT", "Usine",
                             "Bakkertje Bol", "VOF Ding-Lin")),
    ("utilities", contains("BRABANT WATER", "ENERGIEDIRECT",
                           "De Gezondheidswinkel")),
    ("car", contains("Allsecur")),
    ("other insurance", contains("TAF")),
    ("internet", contains("TELFORT")),
    ("mortgage", contains("DELA HYPOTHEKEN")),
    ("bank", contains("Triodos")),
    ("transfer", contains("B\.J\. FRENK", "H\.E\.P\. Bosman")),
    ("taxes and allowances", contains("BELASTINGDIENST")) # should go somewhere else (toeslagen etc.)
])

# TODO: make GUI (using Tkinter?)

# TODO: this depends too much of the internals of the scheme module
def derive_schemes(argv):
    """Return the schemes that might apply to the arguments."""
    if len(argv) < 2:
        return []
    return [getattr(scheme, name) for name in list_functions(scheme)
                                  if name in argv[1]]

def main(argv):
    """Visualize command line specified transaction data."""
    if (len(argv) != 2):
        print "syntax: " + argv[0].split("/")[-1] + " <csv file>"
    else:
        schemes = derive_schemes(argv)
        if (len(schemes) == 0):
            print "Cannot derive transaction format from input arguments."
        elif len(schemes) > 1:
            print "Multiple transaction formats might apply to the input."
        else:
            scheme = schemes[0]
            history = Transaction.read(scheme(CAT), argv[1])

            hierarchy = [lambda t: t.month, lambda t: t.cat]
            print_summary(history, hierarchy)

if __name__ == "__main__":
    main(sys.argv)
