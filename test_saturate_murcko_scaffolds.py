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
with Python 3.12.6, and Pytest 8.3.3 as fetched from PyPi.org.

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

SCRIPT = "saturate_murcko_scaffolds.py"


def test_program_exists():
    """Check for the presence of saturate_murcko_scaffolds.py"""

    assert os.path.isfile(SCRIPT)


def test_explicit_double_bonds():
    """Check the saturation of explicit double bonds, e.g. in
    esters, or non-aromatic dienes.

    Submitted are three tests: (E)-hexene, (Z)-hexene both to yield
    hexane (two entries); and 2-pyridone to yield 2-piperidinol.

    The explicit indication of (E)/(Z)-isomerism of the double bonds
    with forward and backward slash may yield a deprecation warning
    issued by Python; so far, without effect to this test's results.

    Since SMILES strings may contain forward and backward slashes, it
    is safer to submit them as r-strings."""

    probe_smiles = [
        (r"CCC/C=C/C", "CCCCCC"),
        (r"CCC/C=C\C", "CCCCCC"),
        (r"O=C1NC=CC=C1", "OC1NCCCC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_explicit_triple_bonds():
    """Check the saturation of explicit triple bonds, e.g. in alkynes,
    nitriles, or isonitriles.

    Submitted are four tests: 1-hexine, 2-hexine both to yield hexane
    (two entries), benzonitrile to cyclohexylmethylamine, and
    tert-butyl isocyanide to N-tert-butyl methylamine."""

    probe_smiles = [
        (r"CCCCC#C", "CCCCCC"),
        (r"CCCC#CC", "CCCCCC"),
        (r"N#Cc1ccccc1", "NCC1CCCCC1"),
        (r"CC(C)(C)N#C", "CC(C)(C)NC")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_benzene_to_cyclohexane():
    """Check the complete saturation of benzene to cyclohexane"""

    probe_smiles = [
        (r"Cc1ccccc1", "C1CCCCC1"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_cyclopentadiene_to_cyclopentane():
    """Check the saturation of cyclohexadiene to cyclohexane"""

    probe_smiles = [
        (r"C1=CC=CC1", "C1CCCC1"),
        (r"c1cCcc1", "C1CCCC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_pyrrole_to_pyrrolidine():
    """Check the saturation for a N-heterocycle"""

    probe_smiles = [
        (r"1c[nH]cc1", "C1C[NH]CC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_furane_to_tetrahydrofurane():
    """Check the saturation for an O-heterocycle"""

    probe_smiles = [
        (r"c1cocc1", "C1COCC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_phosporine_to_phosphinane():
    """Check the saturation for an P-heterocycle, 1/2"""

    probe_smiles = [
        (r"C1=CC=PC=C1", "C1CCPCC1"),
        (r"c1cpccc1", "C1CPCCC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_phosphole_to_phospholane():
    """Check the saturation for an P-heterocycle, 2/2."""

    probe_smiles = [
        (r"P1C=CC=C1", "P1CCCC1"),
        (r"c1ccc[pH]1", "C1CCC[PH]1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_thiophene_to_thiolene():
    """Check the saturation for a S-heterocycle"""

    probe_smiles = [
        (r"c1cscc1", "C1CSCC1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_stannole_to_stannolane():
    """Prevent the not sensible reduction of [sn] to [SN].

    While `[sn]` is valid for an atom of tin (implicitly) considered aromatic
    and `[Sn]` one which is not, the saturation must not yield `[SN]`.  There
    is not such an element symbol, and except single hydrogen `H`, the presence
    of a second element enclosed in the square brackets -- here reading like
    sulfur and nitrogen -- is not sensible."""

    probe_smiles = [
        (r"c1c[Sn]cc1", "C1C[Sn]CC1"),
        (r"c1[sn]ccc1", "C1[Sn]CCC1"),
        (r"C1=CC=C[Sn]1", "C1CCC[Sn]1")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_preserve_stereogenic_centers():
    """Do not remove, nor newly assign (R)/(S) indicators.

    Test compounds are the prochiral methyl ethylketone,
    (2R)-butanol, and (2S)-butanol."""

    probe_smiles = [
        (r"CCC(C)=O", "CCC(C)O"),
        (r"nCC[C@@H](C)O", "NCC[C@@H](C)O"),
        (r"CC[C@H](C)O", "CC[C@H](C)O")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_preserve_structure_concatenation():
    """Retain the concatenation by the period sign.

    There is no reason to exclude _a priori_ SMILES strings describing
    more than exactly one molecule each.  This allows the submission
    of e.g., SMILES about co-crystals, solvates, etc.  The entry of
    the test indeed is about 1,4-benzoquinone and hydroquinone."""

    probe_smiles = [
        (r"C1=CC(=O)C=CC1=O.c1cc(ccc1O)O", "C1CC(O)CCC1O.C1CC(CCC1O)O")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_preserve_assigned_charges():
    """Do not alter a charged assigned to an atom.

    By current limitations (only one pair of squared brackets per SMILES),
    the maximum number of charged atoms per SMILES string equates to one.
    Because this conventionally is enclosed in squared brackets, the
    remainder of the molecule must not contain an additional instance of
    square brackets.  Thus, the tests describe phenolate (two versions)
    and N,N,N-trimethylbenzenaminium, intentionally lacking the counter
    ion for charge compensation."""

    probe_smiles = [
        (r"[O-]c1ccccc1", "[O-]C1CCCCC1"),
        (r"C[N+](c1ccccc1)(C)C", "C[N+](C1CCCCC1)(C)C")
    ]
    for smiles_in, smiles_out in probe_smiles:
        print(smiles_in)
        assert smiles_out


def test_pass_input_file_to_cli():
    """saturate multiple SMILES from a file, report to the CLI"""
    molecules = ["c1ccncc1", "[O-]c1ccccc1", "c1c[Sn]cc1", "nCC[C@@H](C)O"]

    with open(file="checker.smi", mode="wt", encoding="utf-8") as newfile:
        for molecule in molecules:
            newfile.write(molecule + "\n")

    command = str("python3 saturate_murcko_scaffolds.py checker.smi")
    sub.call(command, shell=True)

    assert str(
        """
C1CCNCC1
[O-]C1CCCCC1
C1C[Sn]CC1
NCC[C@@H](C)O
"""
)

    os.remove("checker.smi")


# END
