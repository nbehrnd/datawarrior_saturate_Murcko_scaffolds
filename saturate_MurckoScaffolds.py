#!/usr/bin/env python3

# name:   saturate_MurckoScaffolds.py
# author: nbehrnd@yahoo.com
# date:   2019-06-07 (YYYY-MM-DD)
# edit:   2021-04-27 (YYYY-MM-DD)
#
"""Read Smiles of Murcko scaffolds and return these as 'saturated'.

The Bemis-Murcko scaffold [1] provided by DataWarrior [2] retains
information about bond order and chirality, which simplifies Benomyl
[3] (i.e., Methyl 1-(butylcarbamoyl)-2-benzimidazolecarbamate) to
benzimidazole.  Note, DataWarrior offers to identify the
Bemis-Murcko skeleton; in case of Benomyl, this is octahydro-1H-indene.

There are instances where an intermediate simplification is required,
retaining only information atom connectivity which corresponds to the
assumption 'there are only single bonds' and a neutral state.
Benomyl, already simplified by DataWarrior to benzimidazole, thus
yields octahydro-1H-benzimidazole

The script works from the CLI of Python to read a list of SMILES from
[input_file.smi] as the mandatory parameter:

python saturate_MurckoScaffolds.py [input_file.smi]

The results are written into file [input_file_sat.smi].  Atoms
with at maximum one positive or one negative charge in the input
SMILES will yield neuter atoms in the output.

[1] Bemis GW, Murcko MA J. Med. Chem. 1996, 39, 2887-2893, doi
    10.1021/jm9602928.
[2] Sander T, Freyss J, von Korff M, Rufener C,
    J. Chem. Inf. Model. 2015, 55, 460-473, doi 10.1021/ci500588j,
    http://www.openmolecules.org, https://github.com/thsa/datawarrior
[3] https://en.wikipedia.org/wiki/Benomyl
[4] http://www.openbabel.org/wiki/Main_Page, version 3.0.0

License: Norwid Behrnd, 2019--2021, GPLv3.
"""
import argparse


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Report 'saturated' Murcko scaffolds as a list of SMILES.")

    parser.add_argument('source_file',
                        metavar='FILE',
                        help='Input file containing a list of SMILES strings.')

    return parser.parse_args()


def smiles_reading():
    """Identify the smiles to work with."""
    global smiles_register
    global input_file
    args = get_args()
    input_file = args.source_file
    smiles_register = []
    with open(input_file, mode="r") as source:
        for line in source:
            smiles_register.append(line.strip())


def remove_explicit_chars():
    """Remove the characters about a higher bond order."""
    global retained_after_char_removal
    retained_after_char_removal = ""

    for char in smiles_entry:
        strip_characters = ['=', '#', '/', '\\']
        if str(char) not in strip_characters:
            retained_after_char_removal += str(char)


def capitalize_CNOPS():
    """Ensure capitalization of elements (C, N, O, P, S).

    A simple string-conversion to yield upper-case characters only is
    not sensible here; this would render the SMILES strings of
    compounds like stannabenzene, arsabenzene, germabenzene and
    silabenzene at least ambigous.  The later, for example, is
    understood by openbabel[4] with the SMILES string c1cc[siH]cc1,
    where the naive capitalization would yield S (like sulfur) and
    I (like iodine) simultaneously.

    Silicon accidentally may benefit from the capitalization of its
    first character, though."""

    change_case = ['c', 'n', 'o', 'p', 's']
    retained_BO_one_string = ""

    reporter_file = input_file[:-4] + str("_sat.smi")
    with open(reporter_file, mode="a") as newfile:

        for char in retained_after_char_removal:
            if str(char) in change_case:
                retained_BO_one_string += char.upper()
            else:
                retained_BO_one_string += char

        retained_BO_one_string += str("\n")
        newfile.write(retained_BO_one_string)


def main():
    """Join the individual methods, lower the bond order to one."""
    smiles_reading()
    global smiles_entry
    for smiles_entry in smiles_register:
        remove_explicit_chars()
        capitalize_CNOPS()


if __name__ == "__main__":
    main()
