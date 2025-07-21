#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:   test_blackbox.py
# author: nbehrnd@yahoo.com
# date:   [2021-02-04 Tue]
# edit:   [2025-07-21 Mon]
#
"""tests for saturate_murcko_scaffolds.py

This script checks results by script `saturate_murcko_scaffolds.py` with
pytest.  The coverage is incomplete, already because checks currently don't
import individual functions, i.e. only black box-tests (`pytest -k blackbox`)
are run.

There are additional SMILES in sub folder `demo` which serve for a more
extended demonstration of the script's working rather than (pytest based)
checks if the script works correctly.
"""

import os
import subprocess as sub

import pytest

SCRIPT = os.path.join(
    "src", "saturate_murcko_scaffolds", "saturate_murcko_scaffolds.py"
)


def test_program_exists():
    """Check for the presence of saturate_murcko_scaffolds.py."""

    assert os.path.isfile(SCRIPT)


@pytest.mark.blackbox
def test_explicit_double_bonds():
    """Check the saturation of explicit double bonds.

    Submitted are three tests: (E)-hexene, (Z)-hexene both to yield
    hexane (two entries); and 2-pyridone to yield 2-piperidinol.

    For a safe transmission of (E)/(Z)-isomerism on double bonds
    with forward and backward slashes, the SMILES are submitted as
    r-strings."""

    probe_smiles = [
        (r"CCC/C=C/C", "CCCCCC"),
        (r"CCC/C=C\C", "CCCCCC"),
        (r"O=C1NC=CC=C1", "OC1NCCCC1"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_explicit_triple_bonds():
    """Check the saturation of explicit triple bonds.

    Submitted are four tests: 1-hexine, 2-hexine both to yield hexane
    (two entries), benzonitrile to cyclohexylmethylamine, and
    tert-butyl isocyanide to N-tert-butyl methylamine."""

    probe_smiles = [
        (r"CCCCC#C", "CCCCCC"),
        (r"CCCC#CC", "CCCCCC"),
        (r"N#Cc1ccccc1", "NCC1CCCCC1"),
        (r"CC(C)(C)N#C", "CC(C)(C)NC"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_toluene_to_methylcyclohexane():
    """Check the saturation of toluene to methylcyclohexane."""

    probe_smiles = [
        (r"Cc1ccccc1", "CC1CCCCC1"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_cyclopentadiene_to_cyclopentane():
    """Check the saturation of cyclohexadiene to cyclohexane."""

    probe_smiles = [(r"C1=CC=CC1", "C1CCCC1"), (r"c1cCcc1", "C1CCCC1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_pyrrole_to_pyrrolidine():
    """Check the saturation of a N-heterocycle."""

    probe_smiles = [(r"c1c[nH]cc1", "C1C[NH]CC1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_furane_to_tetrahydrofurane():
    """Check the saturation of a O-heterocycle."""

    probe_smiles = [(r"c1cocc1", "C1COCC1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_phosporine_to_phosphinane():
    """Check the saturation for an P-heterocycle, 1/2."""

    probe_smiles = [(r"C1=CC=PC=C1", "C1CCPCC1"), (r"c1cpccc1", "C1CPCCC1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_phosphole_to_phospholane():
    """Check the saturation for an P-heterocycle, 2/2."""

    probe_smiles = [(r"P1C=CC=C1", "P1CCCC1"), (r"c1ccc[pH]1", "C1CCC[PH]1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_thiophene_to_thiolene():
    """Check the saturation for a S-heterocycle."""

    probe_smiles = [(r"c1cscc1", "C1CSCC1")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
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
        (r"C1=CC=C[Sn]1", "C1CCC[Sn]1"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_preserve_stereogenic_centers():
    """Do not remove, nor newly assign (R)/(S) indicators.

    Test compounds are the prochiral methyl ethylketone,
    (2R)-butanol, and (2S)-butanol."""

    probe_smiles = [
        (r"CCC(C)=O", "CCC(C)O"),
        (r"nCC[C@@H](C)O", "NCC[C@@H](C)O"),
        (r"CC[C@H](C)O", "CC[C@H](C)O"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_preserve_structure_concatenation():
    """Retain the concatenation by the period sign.

    There is no reason to exclude _a priori_ SMILES strings describing
    more than exactly one molecule each.  This allows the submission
    of e.g., SMILES about co-crystals, solvates, etc.  The entry of
    the test indeed is about 1,4-benzoquinone and hydroquinone."""

    probe_smiles = [(r"C1=CC(=O)C=CC1=O.c1cc(ccc1O)O", "C1CC(O)CCC1O.C1CC(CCC1O)O")]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
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
        (r"C[N+](c1ccccc1)(C)C", "C[N+](C1CCCCC1)(C)C"),
    ]
    for smiles_in, smiles_out in probe_smiles:
        result = sub.run(["python", SCRIPT, smiles_in], capture_output=True, text=True)
        output = result.stdout.strip()

        assert output == smiles_out, f"Expected {smiles_out}, but got {output}"


@pytest.mark.blackbox
def test_pass_input_file_to_cli():
    """saturate multiple SMILES from a file, report to the CLI"""
    molecules = ["c1ccncc1", "[O-]c1ccccc1", "c1c[Sn]cc1", "nCC[C@@H](C)O"]

    with open(file="checker.smi", mode="wt", encoding="utf-8") as newfile:
        for molecule in molecules:
            newfile.write(molecule + "\n")

    command = ["python", SCRIPT, "checker.smi"]
    result = sub.run(command, capture_output=True, text=True)
    output = result.stdout.strip()

    expected_output = """
C1CCNCC1
[O-]C1CCCCC1
C1C[Sn]CC1
NCC[C@@H](C)O
""".strip()

    assert output == expected_output, f"Expected {expected_output}, but got {output}"

    os.remove("checker.smi")


# END
