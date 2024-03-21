#!/usr/bin/python3
# name:    test_series.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-04-26 (YYYY-MM-DD)
# edit:    2021-04-27 (YYYY-MM-DD)
#
"""
Python script generating the test series' visualizations.

Background: Script saturated_murcko_scaffolds.py 'saturates' Murcko
scaffolds identified by DataWarrior.  The present script uses files
test_input.smi and test_input_sat.smi -- representing molecules prior
and after this processing -- as input to visualize the structures with
OpenBabel.


Usage: The script is written for the CLI of Python 3, invoked by

python test_series.py

in presence of test_input.smi and test_input_sat.smi.  The script is
known to work with OpenBabel 3.1.0 and Python 3.9.2 as provided from
the repositories of Linux Debian 11 / bullseye, branch testing.  This
script equally works with legacy Python 2.7.18, too.


Design principle: This script relays instructions to OpenBabel like
those one could type one the CLI.

+ The color scheme applied is OpenBabel's default.  By "addinindex"
  (instead of "addindex") the entries are numbered in consecution of
  their appearance in the .smi in a grid of 10 entries per line and
  12 lines per page.
  The input follows the pattern of:

  obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex

  For the representation in black and white:

  obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex -xu

+ The default width of the .png per motif equates to 300 dpi.  To
  maintain the grid already introduced, the page-width is explicitly
  defined as the tenfold multiple.  The input follow the pattern of:

  obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000

  Inter alia, for the representation in black and white:

  obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000 -xu

The script intends to serve as proof-of-principle."""

import subprocess as sub

register = [
    "obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex",
    "obabel -ismi test_input_sat.smi -O test_input_color_sat.svg -xc10 -xr12 -xl --addinindex",
    "obabel -ismi test_input.smi -O test_input_bw.svg -xc10 -xr12 -xl --addinindex -xu",
    "obabel -ismi test_input_sat.smi -O test_input_bw_sat.svg -xc10 -xr12 -xl --addinindex -xu",

    "obabel -ismi test_input.smi -O test_input_color.png -xc10 -xr12 -xl --addinindex -xp 3000",
    "obabel -ismi test_input_sat.smi -O test_input_color_sat.png -xc10 -xr12 -xl --addinindex -xp 3000",
    "obabel -ismi test_input.smi -O test_input_bw.png -xc10 -xr12 -xl --addinindex -xp 3000 -xu",
    "obabel -ismi test_input_sat.smi -O test_input_bw_sat.png -xc10 -xr12 -xl --addinindex -xp 3000 -xu"
]

for entry in register:
    try:
        print("Work on ", entry)
        sub.call(entry, shell=True)
    except OSError:
        print("Passing entry ", entry)

print("\nLoop completed.")
