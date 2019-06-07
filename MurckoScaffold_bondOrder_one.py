# name:   MurckoScaffold_bondOrder_one.py
# author: nbehrnd@yahoo.com
# date:   2019-06-07 (YYYY-MM-DD)
""" Read Smiles of Murcko scaffolds and return these as 'saturated'.

The Bemis-Murcko scaffold [1] provided by DataWarrior [2] retains
information about bond order and chirality.  There are instances where
retaining only information about which atoms are connected with each
other, but not their bond order is desired.  This corresponds to the
assumption 'there are only single bonds'.  DataWarrior equally offers
the export of Bemis-Murcko skeleton, however this simplifies e.g. an
imidazole scaffold into cyclopentane.

To be used on the CLI of Python (either branch 2 or 3) with the mandatory
parameter about listing file containing the SMILES to work with:

python MurckoScaffold_bondOrder_one [listing_file.txt]

to generate saturated_Murcko_scaffold.csv as permanent record.

[1] Bemis GW, Murcko MA J. Med. Chem. 1996, 39, 2887-2893,
    doi 10.1021/jm9602928
[2] Sander T, Freyss J, von Korff M, Rufener C, J. Chem. Inf. Model. 2015,
    55, 460-473, doi 10.1021/ci500588j, http://www.openmolecules.org
"""
import sys

# read input file
try:
    if sys.argv[1] is not None:
        input_file = str(sys.argv[1])
except:
    print("\nExpected use: python bond_order_one.py [listing.txt]")
    print("Without changing data, the script will close now.\n")
    sys.exit()


def smiles_reading():
    """ read the smiles to work with """
    global smiles_register
    smiles_register = []
    with open(input_file, mode="r") as source:
        for line in source:
            smiles_register.append(line.strip())


def worker():
    """ umbrella of the individual methods lowering bond order to one """
    global smiles_entry
    for smiles_entry in smiles_register:
        remove_explicit_chars()
        capitalize_CNOPS()


def remove_explicit_chars():
    """ remove the characters about a higher bond order or chirality """
    global retained_after_char_removal
    retained_after_char_removal = ""

    for char in smiles_entry:
        strip_characters = ['=', '#', '-', '@', '/', '\\', 'H']
        if str(char) not in strip_characters:
            retained_after_char_removal += str(char)


def capitalize_CNOPS():
    """ change to upper case if these elements are met typed as lower case

    Considered are only mono-character elements more frequently seen in
    homo- / heterocyclic chemistry.  Two-character elements (e.g., Si) seem
    to be written consistently in brackets (e.g., [Si]) regardless if the
    cycle locally is saturated, or not."""

    change_case = ['c', 'n', 'o', 'p', 's']
    retained_BO_one_string = ""

    reporter_file = str("saturated_Murcko_scaffold.csv")
    with open(reporter_file, mode="a") as newfile:

        for char in retained_after_char_removal:
            if str(char) in change_case:
                retained_BO_one_string += char.upper()
            else:
                retained_BO_one_string += char

        retained_BO_one_string += str("\n")
        newfile.write(retained_BO_one_string)


# action calls:
smiles_reading()
worker()

# closing
print("\nPermanent record written into 'saturated_Murcko_scaffold.csv'.")
print("Script 'MurckoScaffold_bondOrder_one' closes now.\n")
sys.exit()
