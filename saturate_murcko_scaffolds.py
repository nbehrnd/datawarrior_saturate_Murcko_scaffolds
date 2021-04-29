#!/usr/bin/env python3

# name:   saturate_murcko_scaffolds.py
# author: nbehrnd@yahoo.com
# date:   2019-06-07 (YYYY-MM-DD)
# edit:   2021-04-29 (YYYY-MM-DD)
#
"""Read Smiles of Murcko scaffolds and return these as 'saturated'.

The Bemis-Murcko scaffold [1] provided by DataWarrior [2] retains
information about bond order and chirality, which simplifies the
structure of Benomyl[3] (i.e., of methyl 1-(butylcarbamoyl)-2-
benzimidazolecarbamate, CAS-RN 17804-35-2) to benzimidazole.  Note,
DataWarrior equally offers to identify the Bemis-Murcko skeleton; in
case of Benomyl the simplification yields octahydro-1H-indene.

There are instances where an intermediate simplification is required,
retaining only information atom connectivity which corresponds to the
assumption 'there are only single bonds' and a neutral state.
Benomyl, already simplified by DataWarrior to benzimidazole, thus
yields octahydro-1H-benzimidazole

The script works from the CLI of Python with listing file containing
the SMILES to work with as mandatory parameter:

python saturate_murcko_scaffolds.py [listing_file.txt]

Results are written into file saturated_Murcko_scaffold.csv.  Atoms
with at maximum one positive or one negative charge in the input
SMILES will yield neuter atoms in the output.

[1] Bemis GW, Murcko MA J. Med. Chem. 1996, 39, 2887-2893, doi
    10.1021/jm9602928.
[2] Sander T, Freyss J, von Korff M, Rufener C,
    J. Chem. Inf. Model. 2015, 55, 460-473, doi 10.1021/ci500588j,
    http://www.openmolecules.org, https://github.com/thsa/datawarrior
[3] https://en.wikipedia.org/wiki/Benomyl

License: Norwid Behrnd, 2019--2021, GPLv3.
"""
import argparse
import os


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Report 'saturated' Murcko scaffolds as a list of SMILES.")

    parser.add_argument("source_file",
                        metavar="FILE",
                        help="Input file containing a list of SMILES strings.")

    return parser.parse_args()


def prepare_reporter():
    """Set the stage for a permanent record file."""
    args = get_args()
    input_file = args.source_file

    reporter_file = "".join([str(input_file).split(".")[0], str("_sat.smi")])

    # Ensure the absence of reporter_file left by a previous run:
    try:
        os.remove(reporter_file)
    except OSError:
        pass

    return reporter_file


def read_smiles():
    """Identify the smiles to work with."""
    smiles_register = []

    args = get_args()
    input_file = args.source_file

    try:
        with open(input_file, mode="r") as source:
            for line in source:
                retain = str(line).strip()
                smiles_register.append(retain)
    except OSError:
        print("File '{}' could not be accessed.  Exit.".format(input_file))
    return smiles_register


def adjust_smiles():
    """Remove, or capitalize characters in the SMILES string.

    Explicit descriptions of double or triple bonds will be removed,
    including the markers about (cis)/(trans) configuration.  A set
    of characters implicitly describing bond orders higher than one
    will be capitalized if these are about elements written by one
    character only."""

    characters_to_remove = ["=", "#", "/", "\\"]
    characters_to_captitalize = ["c", "n", "o", "p", "s"]
    retained_smiles = []

    smiles_register = read_smiles()

    for entry in smiles_register:
        smiles_per_entry = ""

        # Prevent the description of tin:
        if (str("[sn]") in str(entry)) or (str("[Sn]") in str(entry)):
            smiles_per_entry = str(
                "Entry {} might report tin and is skipped.".format(entry))
            retained_smiles.append(smiles_per_entry)
            continue

        # Process no-tin data:
        for char in entry:
            if char in characters_to_remove:
                pass
            elif char in characters_to_captitalize:
                smiles_per_entry += str(char).upper()
            else:
                smiles_per_entry += str(char)

        retained_smiles.append(smiles_per_entry)
    return retained_smiles


def report_results():
    """Write a permanent record of the 'saturized' SMILES strings."""

    reporter_file = prepare_reporter()
    smiles_to_report = adjust_smiles()

    try:
        with open(reporter_file, mode="w") as newfile:
            retain = "\n".join(smiles_to_report)
            newfile.write(retain)

        print("File '{}' lists the processed SMILES strings.".format(
            reporter_file))
    except OSError:
        print("File '{}' could not be written.  Exit.".format(reporter_file))


def main():
    """Join the functions."""
    adjust_smiles()
    report_results()


if __name__ == "__main__":
    main()
