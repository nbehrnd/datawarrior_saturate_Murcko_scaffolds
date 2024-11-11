#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:   saturate_murcko_scaffolds.py
# author: nbehrnd@yahoo.com
# date:   [2019-06-07 Fri]
# edit:   [2024-11-11 Mon]
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

License: Norwid Behrnd, 2019--2023, GPLv3.
"""
import argparse
import io
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
        SMILES string. Enclose SMILES provided via the command line in quotes,
        or some characters permissible in a SMILES string can launch an unwanted
        action."""
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="provide one or multiple SMILES from the CLI, or an input text file listing SMILES")


    args = parser.parse_args()

#    if os.path.isfile(args.text):
#        args.text = open(file=args.text, mode="rt", encoding="utf-8")
#    else:
#        args.text = io.StringIO(args.text + "\n")

    return args


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


def saturate_bonds(input_smiles):
    """remove explicit designation of higher bond orders

    SMILES strings may describe double and triple bonds explicitly; this as well
    as then irrelevant information about (E)/(Z) configuration is removed."""
    characters_to_remove = ["=", "#", "/", "\\"]
    retain = []
    processed = ""

    for char in input_smiles:
        if char in characters_to_remove:
            pass
        else:
            retain.append(char)

    processed = "".join(retain)
    return processed


def saturate_carbon(input_string):
    """provide saturation of carbon atoms

    A sequential approach appears more suitable here.
    + though perhaps a bit verbose, it is possible to note every C atom enclosed
      in square brackets.  Inspired by OpenBabel, saturation is provided by drop
      of the enclosing square brackets and capitalization.
    + application of the mere string.uppercase() approach could transform `[sn]`
      about aromatic tin to `[SN]` -- which however now neither is non-aromatic
      tin `[Sn]`, nor follows the rule to enclose only one element into a pair
      of square brackets (you don't want to have `S` sulfur and `N` instead).
      So the second rule prevents a modification of `c` if `c` is used as second
      character of an element symbol enclosed by a pair or square brackets.
    + third, there may be formal charge on the atom of interest.  For now, only
      single positive, and single negative are supported by the algorithm.
    """
    processed = ""
    new01 = re.sub(r"\[c\]", "C", input_string)  # `[c]` -> `C`
    new02 = re.sub(r"(?<!\[[a-zA-Z])c(?!\])", "C", new01)
    new03 = re.sub(r"\[c-\]", "[C-]", new02)
    new04 = re.sub(r"\[c+\]", "[C+]", new03)

    processed = new04
    return processed


def saturate_nitrogen(input_string):
    """provide saturation of nitrogen atoms

    The approach copies the one introduced on carbon, confer vide supra."""
    processed = ""
    new01 = re.sub(r"\[n\]", "N", input_string)  # `[n]` -> `N`
    new02 = re.sub(r"(?<!\[[a-zA-Z])n(?!\])", "N", new01)
    new03 = re.sub(r"\[n-\]", "[N-]", new02)
    new04 = re.sub(r"\[n+\]", "[N+]", new03)

    processed = new04
    return processed


def saturate_oxygen(input_string):
    """provide saturation of oxygen atoms

    The approach copies the one introduced on carbon, confer vide supra."""
    processed = ""
    new01 = re.sub(r"\[o\]", "O", input_string)  # `[o]` -> `O`
    new02 = re.sub(r"(?<!\[[a-zA-Z])o(?!\])", "O", new01)
    new03 = re.sub(r"\[o-\]", "[O-]", new02)
    new04 = re.sub(r"\[o+\]", "[O+]", new03)

    processed = new04
    return processed


def saturate_phosphorus(input_string):
    """provide saturation of phosphorus atoms

    The approach copies the one introduced on carbon, confer vide supra."""
    processed = ""
    new01 = re.sub(r"\[p\]", "P", input_string)  # `[p]` -> `P`
    new02 = re.sub(r"(?<!\[[a-zA-Z])p(?!\])", "P", new01)
    new03 = re.sub(r"\[p-\]", "[P-]", new02)
    new04 = re.sub(r"\[p+\]", "[P+]", new03)

    processed = new04
    return processed


def saturate_sulfur(input_string):
    """provide saturation of sulfur atoms

    The approach copies the one introduced on carbon, confer vide supra."""
    processed = ""
    new01 = re.sub(r"\[s\]", "S", input_string)  # `[s]` -> `S`
    new02 = re.sub(r"(?<!\[[a-zA-Z])s(?!\])", "S", new01)
    new03 = re.sub(r"\[s-\]", "[S-]", new02)
    new04 = re.sub(r"\[s+\]", "[S+]", new03)

    processed = new04
    return processed


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


def process_smiles(smiles):
    """sequentially pass a SMILES string to reduction"""
    only_single_bonds = saturator(smiles)
    on_carbon = saturate_carbon(only_single_bonds)
    on_nitrogen = saturate_nitrogen(on_carbon)
    on_oxygen = saturate_oxygen(on_nitrogen)
    on_phosphorus = saturate_phosphorus(on_oxygen)
    on_sulfur = saturate_sulfur(on_phosphorus)
    result = on_sulfur

    print(f"{result}")


def process_input_files(input_files):
    """sequentially process input files with lists of SMILES strings"""
    for file in input_files:
        try:
            with open (file, mode="r", encoding="utf-8") as source:
                for line in source:
                    smiles = str(line).strip()
                    process_smiles(smiles)
        except:
            print(f"file {file} is not accessible")


def main():
    """Join the functions."""
    args = get_args()

    smiles_strings = [arg for arg in args.inputs if not os.path.isfile(arg)]
    if smiles_strings:
        for smiles in smiles_strings:
            process_smiles(smiles)

    input_files = [arg for arg in args.inputs if os.path.isfile(arg)]
    if input_files:
        process_input_files(input_files)


if __name__ == "__main__":
    main()
