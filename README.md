

# Background

The Bemis-Murcko scaffold<sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup> provided by
`DataWarrior`<sup><a id="fnr.2" class="footref" href="#fn.2">2</a></sup> retains information about bond order
and chirality.  Sometimes, however, it suffices to retain only
which atoms are connected with each other, equivalent to the
assumption «there are only single bonds».  Note `DataWarrior`
equally offers the export of Bemis-Murcko skeleton, however this
simplifies e.g. the scaffold about an imidazole into one of
cyclopentane.

![img](./pattern.png)


# Typical use

The script runs in the CLI of Python. File `listing_file.txt`
contains the SMILES to work with:

    python saturate_MurckoScaffolds.py [listing_file.txt]

This generates `saturated_Murcko_scaffold_sat.smi` as permanent
record, which shares the file name with the input file *with the
addition of `_sat` (like saturated)*.  Regardless of the
three-character file extension of the input, the plain ASCII-list
of SMILES is recorded in a file of extension `.smi`, accepted
recognized e.g., by `openbabel` to contain this specific
information.

While intended to work with the current branch of Python 3.6+, the
script equally works well with the deprecated, legacy branch of
Python 2, e.g., Python 2.7.16.


# Example

For a collection of organic materials, the Bemis-Murcko scaffolds
was extracted with `DataWarrior` (then release 5.0.0 for Linux,
January 2019) as listing `test_input.smi.txt` including higher bond
orders (see folder `test_data`).  The «artificial saturation» was
triggered by

    1  python saturate_MurckoScaffolds.py test_input.smi

to yield `test_input_sat.smi`.  The effect of this operation is
easy to recognize while comparing the scaffold lists
(fig. [8](#org0b94602)) in a difference view of the two `.smi` files.

![img](./2020-04-26_kdiff3.png "Difference view of the SMILES strings of a Murcko scaffold *prior* (left hand column) and *after* an «artificial saturation» (right hand column).  Note the removal of explicit bond order indicators, e.g. double bond (equality sign), triple bond bond (octohorpe), or about implicit aromatization (lower case &rarr; upper case for atoms of carbon, nitrogen, oxygen (depicted); or sulfur (not depicted).  At the same time, stereochemical indicators are removed, too (e.g., slashes in lines #018 and #019, @-signs line #025).")

Subsequently, `openbabel`<sup><a id="fnr.3" class="footref" href="#fn.3">3</a></sup> was used to illustrate the
work performed.  While eventually automated (cf. script
`test_series.py`, deposit in folder `test_data`), instructions
delivered to `openbabel` on the command line follow the pattern of

    2  obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex

to generate a `.svg` file (vector representation), or

    3  obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000

to generate a bitmap `.png`.  The instructions share the definition
of data input (`-ismi`) &#x2013; eventually *a list of SMILES*, rather
than only one SMILES string &#x2013; and the definition of the output
format based on the extension of the file to be written (`.svg`, or
`.png`).  Both put the entries into an array of 10 columns and
12 rows (`-xc`, `xr`) and label them in the consecution of their
appearance in the input files (`--addinindex`) as inner index.
Contrasting to the vector output, in case of `.png`, an explicit
scaling by a factor of 10 (`-xp` parameter) was required to yield
an intelligible illustration.

It is remarkable how well `openbabel`'s algorithm displays the
molecular structures with advanced motifs (e.g., the scaffold of
cyclophane [entry #33 in the synopses, `test_data` folder],
sparteine [#38], or adamantane [#50]), some equally depicted in the
first illustration of this guide.


# License

Norwid Behrnd, 2020, GPLv3.


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> Bemis GW, Murcko MA *J. Med. Chem.* 1996, ****39****,
2887-2893, [doi 10.1021/jm9602928](https://pubs.acs.org/doi/10.1021/jm9602928)

<sup><a id="fn.2" href="#fnr.2">2</a></sup> Sander T, Freyss J, von Korff M, Rufener C,
*J. Chem. Inf. Model.* 2015, ****55****, 460-473, [doi
10.1021/ci500588j](https://pubs.acs.org/doi/10.1021/ci500588j).  The program, (c) 2002&#x2013;2019 by Idorsia
Pharmaceuticals Ltd., is freely available under
<http://www.openmolecules.org>.

<sup><a id="fn.3" href="#fnr.3">3</a></sup> [www.openbabel.org](http://www.openbabel.org).  The script initially was developed
for and tested with openbabel (release 2.4.1; Nov 12, 2018) and
Python 2.7.17 provided by Linux Xubuntu 18.04.2 LTS.  It equally works
with Python 3.8.2 (recommended current branch, released April 1, 2020)
and openbabel (release 3.0.0 by April 6, 2020) as provided in
Debian 10.
