
# Background

The Bemis-Murcko scaffold[^1] provided by DataWarrior[^2] retains
information about bond order and chirality. Sometimes, however, it
suffices to retain only atom connectivity, like an assumption «there are
only single bonds». Note, DataWarrior equally offers the export of
Bemis-Murcko skeleton, however this simplifies e.g. the scaffold about
an imidazole into one of cyclopentane.

<img src="./pattern.png" title="showcase" style="width:75.0%" />

# Typical use

Running from the command line, the script processes one, or multiple
SMILES strings listed in an input file (symbolized by `text` below) to
report the processed SMILES strings back to the command line:

``` shell
python saturate_murcko_scaffolds.py [-h] [-o] text
```

Instead of an input file, individual SMILES strings equally may be
processed; to prevent their misinterpretation by the shell, enclose them
by either single, or double quotes. Either approach elected, the result
may be redirected into a permanent record with a user defined file name
(flag `--outfile`, or shorter `-o`). Only modules the standard library
of Python 3 provides (e.g., version 3.11.2) are used.

# Example

For a collection of organic materials, the Bemis-Murcko scaffolds were
extracted with DataWarrior (then release 5.0.0 for Linux, January 2019)
as listing `test_input.smi` including higher bond orders (see folder
`test_data`). The effect of the «artificial saturation» is easy to
recognize while comparing the scaffold lists
(fig. <span class="spurious-link" target="file_diff">*file_diff*</span>)
in a difference view of the two `.smi` files.

<figure width="75%">
<img src="./diffview.png" title="file_diff" />
<figcaption>Difference view of the SMILES strings of a Murcko scaffold
<em>prior</em> (left hand column) and <em>after</em> an «artificial
saturation» (right hand column). The processing affects explicit bond
order indicators, e.g. double bond (equality sign, e.g., line #14),
triple bond bond (number sign <code>#</code>, not shown); or about
implicit aromatization (lower case to upper case) for atoms of carbon,
nitrogen, oxygen (depicted); or phosphorus, sulfur (not depicted).
Stereochemical indicators about double bonds will be removed (e.g.,
slashes in lines #18 and #19). Descriptors of stereogenic centers
(<code>@</code>-signs, e.g., line #25) and charges (not shown) are
copied verbatim.</figcaption>
</figure>

The work can be illustrated by OpenBabel[^3] with instructions to the
command line in the pattern of

``` shell
obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex
```

to generate a `.svg` file (vector representation), or

``` shell
obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000
```

to generate a bitmap `.png` with structure formulae depicted in a grid
of 10 columns by 12 rows.

It is remarkable how well OpenBabel's displays the molecular structures
with advanced motifs. In addition to those shown in the first
illustration of this guide, see sub-folder `test_data` for a more
extensive survey (e.g., the scaffold of cyclophane \[entry \#33\],
sparteine \[#38\], or adamantane \[#50\]).

# Known peculiarities

The script provides «saturation» by dropping explicit information
related to double and triple bonds which SMILES encode (`=`, `#`
regarding bond order; `/` (forward slash), `\` (backward slash)
regarding (*cis*)-(*trans*) relationship around double bonds). While
processing double bonds of e.g., ketones to yield secondary alcohols,
the script refrains from the assignment of new CIP priorities and a
corresponding label. It then depends on the program used for a
visualization, if an explicit wedge is used (e.g., OpenBabel), or the
absence of information is highlighted (e.g., as question mark in
DataWarrior, or the project of CDK depict[^4]) as ambiguous. Absolute
configuration of stereogenic centers (indicated in SMILES with the `@`
sign) already assigned in the input however is retained.

For a selection of elements (C, N, O, P, S), the implicit description of
aromatic systems (e.g., as `c1ccncc1` in pyridine, `c1c[nH]cc1` in
pyrrol) is recognized. To offer a «saturation», these characters
returned as upper case characters to yield e.g., piperidine (`C1CCNCC1`)
and pyrrolidine (`C1C[NH]CC1`).

The script equally preserves up to one single negative, or single
positive charge of these five elements (e.g., `[O-]c1ccccc1` about the
phenolate anion, and `C[N+](c1ccccc1)(C)C` about
*N,N,N*-trimethylbenzenaminium cation). Here, it can be sensible to
«sanitize» the results this script provides by other libraries as e.g.
RDKit.[^5]

The capitalization of the five characters is constrained to prevent non
sensible transformations of e.g., an (implicitly) aromatic atom of tin
`[sn]` into the invalid form `[SN]`. Though the script is going to write
tin as `[Sn]`, an adjustment of valence for elements written with two
characters is beyond the current scope of the script.

A SMILES string may describe more than one molecule. Thus, the
concatenation with "`.`" (period character) as seen for example in
descriptions of co-crystals like about 1,4-benzoquinone and
hydroquinone, `C1=CC(=O)C=CC1=O.c1cc(ccc1O)O`, is retained. The example
is resolved as `C1CC(O)CCC1O.C1CC(CCC1O)O`.

# License

Norwid Behrnd, 2019–23, GPLv3.

# Footnotes

[^1]: Bemis, G. W.; Murcko, M. A. The Properties of Known Drugs. 1.
    Molecular Frameworks. *J. Med. Chem.* **1996**, *39*, 2887–2893
    (<https://doi.org/10.1021/jm9602928>).

[^2]: Sander, T.; Freyss, J.; Von Korff, M.; Rufener, 1. DataWarrior:
    An Open-Source Program For Chemistry Aware Data
    Visualization And Analysis. *J. Chem. Inf. Model.* **2015**, *55*,
    460–473 (<https://doi.org/10.1021/ci500588j>). The program, (c)
    2002–2023 by Idorsia Pharmaceuticals Ltd., is freely available under
    <http://www.openmolecules.org>. For the source code (GPLv3), see
    <https://github.com/thsa/datawarrior>.

[^3]: [www.openbabel.org](http://www.openbabel.org) For the most recent
    documentation, see
    <https://open-babel.readthedocs.io/en/latest/ReleaseNotes/ob310.html>

[^4]: <https://www.simolecule.com/cdkdepict/depict.html> For the
    mentioned annotation of CIP labels, change `No Annotation` (second
    pull down menu from the left) to `CIP Stereo Label`.

[^5]: For an overview about the freely available RDKit library, see
    [www.rdkit.org](https://www.rdkit.org/). An introduction into the
    topic of «molecular sanitization» is provided in the section of this
    very title in the on-line
    [RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html).
