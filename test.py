#!/usr/bin/env python3
# name:   test.py
# author: nbehrnd@yahoo.com
# date:   2021-02-04 (YYYY-MM-DD)
# edit:   2021-04-28 (YYYY-MM-DD)
#
"""tests for saturate_murcko_scaffolds.py

This script is written to check if edits in the script
saturate_MurckoScaffolds.py affect scope and content of the output.

The scope of the tests is incomplete.

To trigger the tests, either launch

pytest test.py

or

pytest-3 test.py

The script test.py works for either pytest 6.2.1 and Python 3.9.1, or
legacy pytest 4.6.11 and Python 2.7.18.  The test sequence equally may
be triggered with the Makefile (and GNU Make 4.3); here pytest-3 is
invoked."""

import os
import subprocess as sub

SCRIPT = './saturate_murcko_scaffolds.py'


# --------------------------------------------------
def test_program_exists():
    """Check for the presence of saturate_murcko_scaffolds.py"""

    assert os.path.isfile(SCRIPT)


## --------------------------------------------------
def test_benzene_to_cyclohexane():
    """Check the complete saturation of benzene to cyclohexane"""

    with open("benzene.smi", mode="w") as newfile:
        newfile.write("c1ccccc1")

    command = str("python3 saturate_murcko_scaffolds.py benzene.smi")
    sub.call(command, shell=True)

    with open("benzene_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCCC1")

    os.remove('benzene.smi')
    os.remove('benzene_sat.smi')


## --------------------------------------------------
def test_cyclopentadiene_to_cyclopentane():
    """Check the saturation of cyclohexadiene to cyclohexane"""

    with open("cyclopentadiene.smi", mode="w") as newfile:
        newfile.write("c1cccc1")

    command = str("python3 saturate_murcko_scaffolds.py cyclopentadiene.smi")
    sub.call(command, shell=True)

    with open("cyclopentadiene_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("C1CCCC1")

    os.remove('cyclopentadiene.smi')
    os.remove('cyclopentadiene_sat.smi')


## --------------------------------------------------
def test_pyrrole_to_pyrrolidine():
    """Check the saturation for a N-heterocycle"""

    with open("pyrrole.smi", mode="w") as newfile:
        newfile.write("c1cncc1")

    command = str("python3 saturate_murcko_scaffolds.py pyrrole.smi")
    sub.call(command, shell=True)

    with open("pyrrole_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("C1CNCC1")

    os.remove('pyrrole.smi')
    os.remove('pyrrole_sat.smi')


## --------------------------------------------------
def test_furane_to_tetrahydrofurane():
    """Check the saturation for an O-heterocycle"""

    with open("furane.smi", mode="w") as newfile:
        newfile.write("c1cocc1")

    command = str("python3 saturate_murcko_scaffolds.py furane.smi")
    sub.call(command, shell=True)

    with open("furane_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("C1COCC1")

    os.remove('furane.smi')
    os.remove('furane_sat.smi')


## --------------------------------------------------
def test_thiophene_to_thiolene():
    """Check the saturation for a S-heterocycle"""

    with open("thiophene.smi", mode="w") as newfile:
        newfile.write("c1cscc1")

    command = str("python3 saturate_murcko_scaffolds.py thiophene.smi")
    sub.call(command, shell=True)

    with open("thiophene_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("C1CSCC1")

    os.remove('thiophene.smi')
    os.remove('thiophene_sat.smi')


## --------------------------------------------------
def test_explicit_double_bonds():
    """Check the saturation of explicit double bonds, e.g. in
    esters, or non-aromatic dienes.

    Submitted are three tests in one: (E)-hexene, (Z)-hexene both to
    yield hexane; 2-pyridone to yield 2-piperidinol.

    The explicit indication of (E)/(Z)-isomerism of the double bonds
    with forward and backward slash may yield a deprecation warning
    issued by Python; so far, without effect to this test's results."""

    with open("dienes.smi", mode="w") as newfile:
        newfile.write(str("CCC/C=C/C\nCCC/C=C\C\nO=C1NC=CC=C1"))

    command = str("python3 saturate_murcko_scaffolds.py dienes.smi")
    sub.call(command, shell=True)

    with open("dienes_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str("CCCCCC\nCCCCCC\nOC1NCCCC1")

    os.remove("dienes.smi")
    os.remove("dienes_sat.smi")


## --------------------------------------------------
def test_explicit_triple_bonds():
    """Check the saturation of explicit triple bonds, e.g. in alkynes,
    nitriles, or isonitriles.

    Submitted are four tests in one: 1-hexine, 2-hexine both to yield
    hexane, benzonitrile to cyclohexylmethylamine, and tert-butyl
    isocyanide to N-tert-butyl methylamine."""

    with open("triple_bond.smi", mode="w") as newfile:
        newfile.write("CCCCC#C\nCCCC#CC\nN#Cc1ccccc1\nCC(C)(C)N#C")

    command = str("python3 saturate_murcko_scaffolds.py triple_bond.smi")
    sub.call(command, shell=True)

    with open("triple_bond_sat.smi", mode="r") as source:
        output = source.read()
        assert str(output).strip() == str(
            "CCCCCC\nCCCCCC\nNCC1CCCCC1\nCC(C)(C)NC")

    os.remove("triple_bond.smi")
    os.remove("triple_bond_sat.smi")


## --------------------------------------------------
# END
