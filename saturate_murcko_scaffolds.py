#!/usr/bin/env python3

# name:   saturate_murcko_scaffolds.py
# author: nbehrnd@yahoo.com
# date:   2019-06-07 (YYYY-MM-DD)
# edit:   2021-05-03 (YYYY-MM-DD)
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

python saturate_murcko_scaffolds.py [example.txt]

Results are written into file example_sat.txt.  Only SMILES with one
or zero pairs of square brackets (e.g., [Sn], [S@], [Fe3+]) are touched.

[1] Bemis GW, Murcko MA J. Med. Chem. 1996, 39, 2887-2893, doi
    10.1021/jm9602928.
[2] Sander T, Freyss J, von Korff M, Rufener C,
    J. Chem. Inf. Model. 2015, 55, 460-473, doi 10.1021/ci500588j,
    http://www.openmolecules.org, https://github.com/thsa/datawarrior
[3] https://en.wikipedia.org/wiki/Benomyl

License: Norwid Behrnd, 2019--2022, GPLv3.
"""
import argparse
import os
import re
import sys


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="""Reading a list of SMILES, the script reports 'saturated'
        Murcko scaffolds as a list of SMILES.  The script processes SMILES
        strings only if these contain one or zero pairs of square brackets
        (e.g., [Sn], [S@], [Fe3+]) and only works on elements C, N, O, P, and S
        (often written in lower case as an implicit description of the aromatic
        bond order) and explicit double/triple bonds.  To prevent potential
        errors, the square brackets are copied verbatim into the newly written
        SMILES string.  An input file 'example.smi' yields 'example_sat.smi' as
        new permanent record.""")

    parser.add_argument("source_file",
                        metavar="FILE",
                        help="Input file with a list of SMILES strings.")

    return parser.parse_args()


def access_raw_data(input_file=""):
    """Attempt to read the SMILES strings in question."""
    raw_data = []

    try:
        with open(input_file, encoding="utf-8", mode="r") as source:
            raw_data = source.readlines()
    except OSError:
        print(f"Error while accessing input file {input_file}.  Exit.")
        sys.exit()

    return raw_data


def check_admission(smiles):
    """Exclude SMILES with more than one pair of square brackets."""
    check = ""
    pattern_1 = re.compile(r'\[')
    test_1 = pattern_1.findall(smiles)

    pattern_2 = re.compile(r']')
    test_2 = pattern_2.findall(smiles)

    if (len(test_1) == 0 and len(test_2) == 0):
        check = f"0 {smiles}"
    elif (len(test_1) == 1 and len(test_2) == 1):
        check = f"1 {smiles}"
    elif (len(test_1) > 1 or len(test_2) > 1):
        check = f"2 or more instances of square brackets in {smiles}"

    return check


def classifyer(raw_data):
    """Apply check_admission on raw_smiles to yield a list of working_data."""
    working_data = []
    for entry in raw_data:
        entry = str(entry).strip()
        working_data.append(check_admission(entry))

    return working_data


def saturator(raw_smiles):
    """Return a SMILES string about a saturated compound.

    Use this function only on (parts of) a SMILES string which does not
    contain square brackets to prevent confusion like [sn] and [Sn] vs [SN]."""
    characters_to_remove = ["=", "#", "/", "\\"]
    characters_to_captitalize = ["c", "n", "o", "p", "s"]
    retain = []
    saturated_smiles = ""

    for char in raw_smiles:
        if char in characters_to_remove:
            pass
        elif char in characters_to_captitalize:
            retain.append(char.upper())
        else:
            retain.append(char)
    saturated_smiles = "".join(retain)

    return saturated_smiles


def write_record(input_file, listing):
    """Provide the permanent record."""
    stem_input_file = os.path.splitext(input_file)[0]
    report_file = "".join([stem_input_file, "_sat.smi"])

    try:
        with open(report_file, encoding="utf-8", mode="w") as newfile:
            for entry in listing:
                newfile.write(f"{entry}\n")
    except OSError:
        print(f"System error while writing file {report_file}.  Exit.")
        sys.exit()


def main():
    """Join the functions."""
    args = get_args()
    input_file = args.source_file
    raw_data = access_raw_data(input_file)

    working_data = classifyer(raw_data)
    list_processed_smiles = []

    for entry in working_data:
        retain = []

        # absence of square brackets:
        if str(entry).startswith("0"):
            raw_smiles = str(entry).split()[1]
            list_processed_smiles.append(saturator(raw_smiles))

        # one pair of square brackets per SMILES:
        elif str(entry).startswith("1"):
            raw_smiles = str(entry).split()[1]

            # the entry in the center:
            pattern = re.compile(r'\[.*\]')
            test = pattern.search(raw_smiles)
            bracketed_element = test.group()

            # part to the left of "bracketed_element":
            divider = re.compile(r'\[.*\]')
            split_list = divider.split(raw_smiles)
            first_section_raw = split_list[0]
            saturated_left = saturator(first_section_raw)

            # part to the right of "bracketed_element":
            second_section_raw = split_list[1]
            saturated_right = saturator(second_section_raw)

            retain = "".join(
                [saturated_left, bracketed_element, saturated_right])
            list_processed_smiles.append(retain)

        # presence of two or more pairs of square brackets per SMILES:
        elif str(entry).startswith("2"):
            list_processed_smiles.append(entry)

    write_record(input_file, list_processed_smiles)


if __name__ == "__main__":
    main()
