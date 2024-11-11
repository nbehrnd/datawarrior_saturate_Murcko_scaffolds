#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:   test_saturate_murcko_scaffolds.py
# author: nbehrnd@yahoo.com
# date:   [2021-02-04 Tue]
# edit:   [2024-11-11 Mon]
#
"""tests for saturate_murcko_scaffolds.py

This script tests results by script `saturate_murcko_scaffolds.py`.
The scope of the tests implemented could be incomplete.

To trigger the tests,

- clone the project into a local folder
- create a virtual environment
- activate the virtual environment
- run the tests from the top level of the cloned project

In an instance of Linux Debian, this would require the sequence of
the following commands:

```shell
git clone https://github.com/nbehrnd/datawarrior_saturate_Murcko_scaffolds.git
cd ./datawarrior_saturate_Murcko_scaffolds
python -m venv sup
source ./sup/bin/activate
pip install pytest
python -m pytest
```

This approach was tested and run successfully in Linux Debian 13/trixie
with Python 3.11.8, and Pytest 8.1.1 as fetched from PyPi.org.

The SMILES used in the tests were checked with the visual output as .png
provided by OpenBabel.[1]

There are additional SMILES in sub folder `test_data` used e.g., to
generate an illustration on the project's landing page.  These were
exported by DataWarrior.[2]

[1]  OpenBabel (http://www.openbabel.org) as version 3.1.1 for Linux
     Debian 12 / bookworm, branch testing (Jan 4, 2023), was used.

[2]  Sander T, Freyss J, von Korff M, Rufener C, J. Chem. Inf. Model.
     2015, 55, 460-473, (https://pubs.acs.org/doi/10.1021/ci500588j).
     The program, (c) 2002--2021 by Idorsia Pharmaceuticals Ltd., is
     freely available under http://www.openmolecules.org (source code
     at https://github.com/thsa/datawarrior).  The native Linux
     version 5.5.0 (April 2021) was used.
"""

import os
import subprocess as sub

SCRIPT = "./saturate_murcko_scaffolds.py"


# --------------------------------------------------
def test_program_exists():
    """Check for the presence of saturate_murcko_scaffolds.py"""

    assert os.path.isfile(SCRIPT)


# --------------------------------------------------
def test_explicit_double_bonds():
    """Check the saturation of explicit double bonds, e.g. in
    esters, or non-aromatic dienes.

    Submitted are three tests: (E)-hexene, (Z)-hexene both to yield
    hexane (two entries); and 2-pyridone to yield 2-piperidinol.

    The explicit indication of (E)/(Z)-isomerism of the double bonds
    with forward and backward slash may yield a deprecation warning
    issued by Python; so far, without effect to this test's results.

    Because the test string includes `\C` pylint (2.16.2) suggests either
    the escape of the backslash as in `\\C`, or to prepend a `r` -- as in
    `str(r"\C")`.  The former renders the SMILES string invalid, to use
    `r` breaks the the test; hence, this issue is left unchanged."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write(str("CCC/C=C/C\nCCC/C=C\C\nO=C1NC=CC=C1"))

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("CCCCCC\nCCCCCC\nOC1NCCCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_explicit_triple_bonds():
    """Check the saturation of explicit triple bonds, e.g. in alkynes,
    nitriles, or isonitriles.

    Submitted are four tests: 1-hexine, 2-hexine both to yield hexane
    (two entries), benzonitrile to cyclohexylmethylamine, and
    tert-butyl isocyanide to N-tert-butyl methylamine."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("CCCCC#C\nCCCC#CC\nN#Cc1ccccc1\nCC(C)(C)N#C")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("CCCCCC\nCCCCCC\nNCC1CCCCC1\nCC(C)(C)NC")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_benzene_to_cyclohexane():
    """Check the complete saturation of benzene to cyclohexane"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1ccccc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_cyclopentadiene_to_cyclopentane():
    """Check the saturation of cyclohexadiene to cyclohexane"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC=CC1\nc1cCcc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCC1\nC1CCCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_pyrrole_to_pyrrolidine():
    """Check the saturation for a N-heterocycle"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1c[nH]cc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1C[NH]CC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_furane_to_tetrahydrofurane():
    """Check the saturation for an O-heterocycle"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1cocc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1COCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_phosporine_to_phosphinane():
    """Check the saturation for an P-heterocycle, 1/2"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC=PC=C1\nc1cpccc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCPCC1\nC1CPCCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_phosphole_to_phospholane():
    """Check the saturation for an P-heterocycle, 2/2."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("P1C=CC=C1\nc1ccc[pH]1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("P1CCCC1\nC1CCC[PH]1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_thiophene_to_thiolene():
    """Check the saturation for a S-heterocycle"""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1cscc1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CSCC1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_stannole_to_stannolane():
    """Prevent the not sensible reduction of [sn] to [SN].

    While `[sn]` is valid for an atom of tin (implicitly) considered aromatic
    and `[Sn]` one which is not, the saturation must not yield `[SN]`.  There
    is not such an element symbol, and except single hydrogen `H`, the presence
    of a second element enclosed in the square brackets -- here reading like
    sulfur and nitrogen -- is not sensible."""
    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1c[Sn]cc1\nc1[sn]ccc1\nC1=CC=C[Sn]1")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1C[Sn]CC1\nC1[Sn]CCC1\nC1CCC[Sn]1")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_preserve_stereogenic_centers():
    """Do not remove, nor newly assign (R)/(S) indicators.

    Test compounds are the prochiral methyl ethylketone,
    (2R)-butanol, and (2S)-butanol."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("CCC(C)=O\nnCC[C@@H](C)O\nCC[C@H](C)O")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("CCC(C)O\nNCC[C@@H](C)O\nCC[C@H](C)O\n")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_preserve_structure_concatenation():
    """Retain the concatenation by the period sign.

    There is no reason to exclude _a priori_ SMILES strings describing
    more than exactly one molecule each.  This allows the submission
    of e.g., SMILES about co-crystals, solvates, etc.  The entry of
    the test indeed is about 1,4-benzoquinone and hydroquinone."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC(=O)C=CC1=O.c1cc(ccc1O)O")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("C1CC(O)CCC1O.C1CC(CCC1O)O\n")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_preserve_assigned_charges():
    """Do not alter a charged assigned to an atom.

    By current limitations (only one pair of squared brackets per SMILES),
    the maximum number of charged atoms per SMILES string equates to one.
    Because this conventionally is enclosed in squared brackets, the
    remainder of the molecule must not contain an additional instance of
    square brackets.  Thus, the tests describe phenolate (two versions)
    and N,N,N-trimethylbenzenaminium, intentionally lacking the counter
    ion for charge compensation."""

    with open("test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("[O-]c1ccccc1\nC[N+](c1ccccc1)(C)C")

    command = str("python3 saturate_murcko_scaffolds.py test.smi -o output.smi")
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("[O-]C1CCCCC1\nC[N+](C1CCCCC1)(C)C\n")

    os.remove("test.smi")
    os.remove("output.smi")


# --------------------------------------------------
def test_pass_input_from_cli_to_file():
    """with pyridine, check the saturation from the CLI"""

    command = str('python3 saturate_murcko_scaffolds.py "c1ccncc1" -o output.smi')
    sub.call(command, shell=True)

    with open("output.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("C1CCNCC1\n")

    os.remove("output.smi")


# --------------------------------------------------
def test_pass_input_from_cli_to_cli():
    """with pyridine, check the saturation from the CLI"""

    command = str('python3 saturate_murcko_scaffolds.py "c1ccncc1"')
    sub.call(command, shell=True)

    assert str("C1CCNCC1\n")


# --------------------------------------------------
def test_pass_input_file_to_cli():
    """saturate multiple SMILES from a file, report to the CLI"""
    molecules = ["c1ccncc1", "[O-]c1ccccc1", "c1c[Sn]cc1", "nCC[C@@H](C)O"]

    with open(file="test.smi", mode="wt", encoding="utf-8") as newfile:
        for molecule in molecules:
            newfile.write(molecule + "\n")

    command = str("python3 saturate_murcko_scaffolds.py test.smi")
    sub.call(command, shell=True)
    assert str(
        """
C1CCNCC1
[O-]C1CCCCC1
C1C[Sn]CC1
NCC[C@@H](C)O
"""
    )

    os.remove("test.smi")


# END
