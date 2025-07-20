#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:   test_blackbox.py
# author: nbehrnd@yahoo.com
# date:   [2025-07-17 Thu]
# edit:   [2025-07-20 Sun]
#
"""tests for saturate_murcko_scaffolds.py with function imports

This file provides pytest checks for script `saturate_murcko_scaffolds.py`.
Complementary to the ones in `test_blackbox.py`, this script imports and
checks the script's functions individually."""
import os
import shlex

import pytest

from saturate_murcko_scaffolds.saturate_murcko_scaffolds import (
    saturate_bonds,
    saturate_carbon,
    saturate_nitrogen,
    saturate_oxygen,
    saturate_phosphorus,
    saturate_sulfur,
    process_smiles,
    get_args,
    process_input_files,
)


@pytest.mark.imported
def test_butene() -> None:
    """Test the reduction of 1-butene."""
    input_smiles = r"C=CCC"
    output_smiles = r"CCCC"
    assert saturate_bonds(input_smiles) == output_smiles


@pytest.mark.imported
def test_2e_butene() -> None:
    """Test the reduction of (2E)-butene, (trans) isomer."""
    input_smiles = r"C/C=C/C"
    output_smiles = r"CCCC"
    assert saturate_bonds(input_smiles) == output_smiles


@pytest.mark.imported
def test_2z_butene() -> None:
    """Test the reduction of (2Z)-butene, (cis)-isomer."""
    input_smiles = r"C/C=C\C"
    output_smiles = r"CCCC"
    assert saturate_bonds(input_smiles) == output_smiles


@pytest.mark.imported
def test_butine() -> None:
    """Test the reduction of 1-butine for its C-C triple bond."""
    input_smiles = r"C#CCC"
    output_smiles = r"CCCC"
    assert saturate_bonds(input_smiles) == output_smiles


@pytest.mark.imported
def test_benzene() -> None:
    """Test the reduction of benzene (aromaticity)."""
    input_smiles = r"c1ccccc1"
    output_smiles = r"C1CCCCC1"
    assert saturate_carbon(input_smiles) == output_smiles


@pytest.mark.imported
def test_pyridine() -> None:
    """Test the reduction of pyridine (aromaticity)."""
    input_smiles = r"c1ccncc1"
    output_smiles = r"C1CCNCC1"
    assert saturate_nitrogen(saturate_carbon(input_smiles)) == output_smiles
    assert saturate_carbon(saturate_nitrogen(input_smiles)) == output_smiles


@pytest.mark.imported
def test_furane() -> None:
    """Test the reduction of furane (aromaticity)."""
    input_smiles = r"c1ccoc1"
    output_smiles = r"C1CCOC1"
    assert saturate_oxygen(saturate_carbon(input_smiles)) == output_smiles
    assert saturate_carbon(saturate_oxygen(input_smiles)) == output_smiles


@pytest.mark.imported
def test_phosphole() -> None:
    """Test the reduction on phosphole (aromaticity)."""
    input_smiles = r"c1ccc[pH]1"
    output_smiles = r"C1CCC[PH]1"
    assert saturate_phosphorus(saturate_carbon(input_smiles)) == output_smiles
    assert saturate_carbon(saturate_phosphorus(input_smiles)) == output_smiles


@pytest.mark.imported
def test_thiophene() -> None:
    """Test the reduction of thiophene (aromaticity)."""
    input_smiles = r"c1ccsc1"
    output_smiles = r"C1CCSC1"
    assert saturate_sulfur(saturate_carbon(input_smiles)) == output_smiles
    assert saturate_carbon(saturate_sulfur(input_smiles)) == output_smiles


@pytest.mark.imported
def test_furfual() -> None:
    """Test reduction of furfural (aromaticity and carbonyl group)."""
    input_smiles = r"c1cc(oc1)C=O"
    output_smiles = r"C1CC(OC1)CO"
    assert process_smiles(input_smiles) == output_smiles


@pytest.mark.imported
def test_tetrabutyltinhydride() -> None:
    """Test Sn is not accidentally 'reduced' to SN."""
    input_smiles = r"CCCC[SnH](CCCC)CCCC"
    output_smiles = r"CCCC[SnH](CCCC)CCCC"
    assert process_smiles(input_smiles) == output_smiles


@pytest.mark.imported
def test_selfcheck_shlex() -> None:
    """Check if `shlex` works well."""
    command = "C#CCC c1ccncc1"
    split_into_list = ["C#CCC", "c1ccncc1"]
    assert shlex.split(command) == split_into_list


@pytest.mark.parametrize(
    "inputs, reference_smiles",
    [(r"C#CCC", r"C#CCC"), (r"C#CCC c1ccncc1", r"C#CCC c1ccncc1")],
)
@pytest.mark.imported
def test_read_smiles_from_cli(inputs, reference_smiles):
    args = get_args(shlex.split(inputs))
    assert inputs == reference_smiles


@pytest.mark.imported
def test_read_smiles_from_a_file(capsys) -> None:
    """Check if a file present and mentioned in a list of files is read."""

    with open("example.smi", mode="w", encoding="utf-8") as new:
        new.write("C#CCC")
    list_of_files = ["example.smi"]
    process_input_files(list_of_files)
    output = capsys.readouterr().out.rstrip()

    assert output == "CCCC"
    os.remove("example.smi")
