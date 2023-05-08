#!/usr/bin/env python3
# name:   test.py
# author: nbehrnd@yahoo.com
# date:   [2021-02-04 Tue]
# edit:   [2023-05-08 Mon]
#
"""tests for saturate_murcko_scaffolds.py

This script is written to check if edits in the script
saturate_murcko_scaffolds.py affect scope and content of the output.

The scope of the tests is incomplete.

To trigger the tests, either launch

pytest test.py

or

pytest-3 test.py

Initially written for pytest 4.6.1 (Python 2.7.18) and pytest 4.6.11
(Python 3.9.1), this version of the script is known to work well with
pytest 7.2.1 (Python 3.11.2) as provided by Linux Debian 12/bookworm,
branch testing.  The test sequence equally may launched by a Makefile
(and GNU Make 4.3) provided; here pytest-3 is invoked.  The SMILES
used in the tests were checked with the visual output as .png provided
by OpenBabel.[1]

There are additional SMILES in sub folder `test_data` used e.g., to
generate an illustration on the project's landing page.  These were
exported by DataWarrior.[1]

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

SCRIPT = './saturate_murcko_scaffolds.py'


# --------------------------------------------------
def test_program_exists():
    """Check for the presence of saturate_murcko_scaffolds.py"""

    assert os.path.isfile(SCRIPT)


## --------------------------------------------------
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

    with open("dienes.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write(str("CCC/C=C/C\nCCC/C=C\C\nO=C1NC=CC=C1"))

    command = str("python3 saturate_murcko_scaffolds.py dienes.smi")
    sub.call(command, shell=True)

    with open("dienes_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("CCCCCC\nCCCCCC\nOC1NCCCC1")

    os.remove("dienes.smi")
    os.remove("dienes_sat.smi")


## --------------------------------------------------
def test_explicit_triple_bonds():
    """Check the saturation of explicit triple bonds, e.g. in alkynes,
    nitriles, or isonitriles.

    Submitted are four tests: 1-hexine, 2-hexine both to yield hexane
    (two entries), benzonitrile to cyclohexylmethylamine, and
    tert-butyl isocyanide to N-tert-butyl methylamine."""

    with open("triple_bond.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("CCCCC#C\nCCCC#CC\nN#Cc1ccccc1\nCC(C)(C)N#C")

    command = str("python3 saturate_murcko_scaffolds.py triple_bond.smi")
    sub.call(command, shell=True)

    with open("triple_bond_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str(
            "CCCCCC\nCCCCCC\nNCC1CCCCC1\nCC(C)(C)NC")

    os.remove("triple_bond.smi")
    os.remove("triple_bond_sat.smi")


## --------------------------------------------------
def test_benzene_to_cyclohexane():
    """Check the complete saturation of benzene to cyclohexane"""

    with open("benzene.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1ccccc1")

    command = str("python3 saturate_murcko_scaffolds.py benzene.smi")
    sub.call(command, shell=True)

    with open("benzene_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCCC1")

    os.remove('benzene.smi')
    os.remove('benzene_sat.smi')


## --------------------------------------------------
def test_cyclopentadiene_to_cyclopentane():
    """Check the saturation of cyclohexadiene to cyclohexane"""

    with open("cyclopentadiene.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC=CC1\nc1cCcc1")

    command = str("python3 saturate_murcko_scaffolds.py cyclopentadiene.smi")
    sub.call(command, shell=True)

    with open("cyclopentadiene_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCC1\nC1CCCC1")

    os.remove('cyclopentadiene.smi')
    os.remove('cyclopentadiene_sat.smi')


## --------------------------------------------------
def test_pyrrole_to_pyrrolidine():
    """Check the saturation for a N-heterocycle"""

    with open("pyrrole.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1c[nH]cc1")

    command = str("python3 saturate_murcko_scaffolds.py pyrrole.smi")
    sub.call(command, shell=True)

    with open("pyrrole_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1C[NH]CC1")

    os.remove('pyrrole.smi')
    os.remove('pyrrole_sat.smi')


## --------------------------------------------------
def test_furane_to_tetrahydrofurane():
    """Check the saturation for an O-heterocycle"""

    with open("furane.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1cocc1")

    command = str("python3 saturate_murcko_scaffolds.py furane.smi")
    sub.call(command, shell=True)

    with open("furane_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1COCC1")

    os.remove('furane.smi')
    os.remove('furane_sat.smi')


## --------------------------------------------------
def test_phosporine_to_phosphinane():
    """Check the saturation for an P-heterocycle, 1/2"""

    with open("phosporine.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC=PC=C1\nc1cpccc1")

    command = str("python3 saturate_murcko_scaffolds.py phosporine.smi")
    sub.call(command, shell=True)

    with open("phosporine_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCPCC1\nC1CPCCC1")

    os.remove('phosporine.smi')
    os.remove('phosporine_sat.smi')


## --------------------------------------------------
def test_phosphole_to_phospholane():
    """Check the saturation for an P-heterocycle, 2/2."""

    with open("phosphole.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("P1C=CC=C1\nc1ccc[pH]1")

    command = str("python3 saturate_murcko_scaffolds.py phosphole.smi")
    sub.call(command, shell=True)

    with open("phosphole_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("P1CCCC1\nC1CCC[PH]1")

    os.remove('phosphole.smi')
    os.remove('phosphole_sat.smi')


## --------------------------------------------------
def test_thiophene_to_thiolene():
    """Check the saturation for a S-heterocycle"""

    with open("thiophene.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1cscc1")

    command = str("python3 saturate_murcko_scaffolds.py thiophene.smi")
    sub.call(command, shell=True)

    with open("thiophene_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1CSCC1")

    os.remove('thiophene.smi')
    os.remove('thiophene_sat.smi')


## --------------------------------------------------
def test_stannole_to_stannolane():
    """Prevent the not sensible reduction of [sn] to [SN].

    While `[sn]` is valid for an atom of tin (implicitly) considered aromatic
    and `[Sn]` one which is not, the saturation must not yield `[SN]`.  There
    is not such an element symbol, and except single hydrogen `H`, the presence
    of a second element enclosed in the square brackets -- here reading like
    sulfur and nitrogen -- is not sensible."""
    with open("stannole.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("c1c[Sn]cc1\nc1[sn]ccc1\nC1=CC=C[Sn]1")

    command = str("python3 saturate_murcko_scaffolds.py stannole.smi")
    sub.call(command, shell=True)

    with open("stannole_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output).strip() == str("C1C[Sn]CC1\nC1[Sn]CCC1\nC1CCC[Sn]1")

    os.remove("stannole.smi")
    os.remove("stannole_sat.smi")


## --------------------------------------------------
def test_preserve_stereogenic_centers():
    """Do not remove, nor newly assign (R)/(S) indicators.

    Test compounds are the prochiral methyl ethylketone,
    (2R)-butanol, and (2S)-butanol."""

    with open("rs_test.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("CCC(C)=O\nnCC[C@@H](C)O\nCC[C@H](C)O")

    command = str("python3 saturate_murcko_scaffolds.py rs_test.smi")
    sub.call(command, shell=True)

    with open("rs_test_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("CCC(C)O\nNCC[C@@H](C)O\nCC[C@H](C)O\n")

    os.remove("rs_test.smi")
    os.remove("rs_test_sat.smi")


### --------------------------------------------------
def test_preserve_structure_concatenation():
    """Retain the concatenation by the period sign.

    There is no reason to exclude _a priori_ SMILES strings describing
    more than exactly one molecule each.  This allows the submission
    of e.g., SMILES about co-crystals, solvates, etc.  The entry of
    the test indeed is about 1,4-benzoquinone and hydroquinone."""

    with open("cocrystal.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("C1=CC(=O)C=CC1=O.c1cc(ccc1O)O")

    command = str("python3 saturate_murcko_scaffolds.py cocrystal.smi")
    sub.call(command, shell=True)

    with open("cocrystal_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str("C1CC(O)CCC1O.C1CC(CCC1O)O\n")

    os.remove("cocrystal.smi")
    os.remove("cocrystal_sat.smi")


## --------------------------------------------------
def test_preserve_assigned_charges():
    """Do not alter a charged assigned to an atom.

    By current limitations (only one pair of squared brackets per SMILES),
    the maximum number of charged atoms per SMILES string equates to one.
    Because this conventionally is enclosed in squared brackets, the
    remainder of the molecule must not contain an additional instance of
    square brackets.  Thus, the tests describe phenolate (two versions)
    and N,N,N-trimethylbenzenaminium, intentionally lacking the counter
    ion for charge compensation."""

    with open("charges.smi", mode="w", encoding="utf-8") as newfile:
        newfile.write("[O-]c1ccccc1\nC[N+](c1ccccc1)(C)C")

    command = str("python3 saturate_murcko_scaffolds.py charges.smi")
    sub.call(command, shell=True)

    with open("charges_sat.smi", mode="r", encoding="utf-8") as source:
        output = source.read()
        assert str(output) == str(
            "[O-]C1CCCCC1\nC[N+](C1CCCCC1)(C)C\n")

    os.remove("charges.smi")
    os.remove("charges_sat.smi")


# END
