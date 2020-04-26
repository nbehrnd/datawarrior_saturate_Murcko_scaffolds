# name:    test_series.py
# author:  nbehrnd@yahoo.com
# license: MIT, 2020
# date:    2020-04-26 (YYYY-MM-DD)
# edit:
#
"""
Python script generating the test series' visualizations.

Script saturated_MurckoScaffolds.py provides a mean to 'artifically
saturate' Murcko scaffolds identified by DataWarrior.  To generate the
synoptic visualizations of the SMILES prior and after the artificial
saturation, openbabel is used from the CLI with these instructions:

+ prior or after the artificial saturation, .svg with openbabel color
  scheme.  Using "addinindex" instead of "addindex" to yield the entries
  numbered in consecution of their appearance in the SMI is not an error.
  The input follows the pattern of:

  obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex

  and, lacking the colors:

  obabel -ismi test_input.smi -O test_input_color.svg -xc10 -xr12 -xl --addinindex -xu

+ prior or after the artificial saturation, .png with openbabel color
  scheme.  The default width of the .png equates 300 dpi, thus, calling
  again for the generation of an array of 10 columns, the default width
  explicitly was defined as the tenfold multiple.  The input follows
  the pattern of:

  obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000

  and, lacking the colors:

  obabel -ismi test_input_sat.smi -O test_input_sat_color.png -xc10 -xr12 -xl --addinindex -xp 3000 -xu

The script is written for the CLI of Python 3, working by

python test_series.py

to yield .svg and .png in openbabel's color scheme as well as in black
and white the synoptic visualizations for file test_input.smi (prior
the saturation) and file test_input_sat.smi (past the saturation). """

import subprocess as sub
import sys

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
    except:
        print("Passing entry ", entry)

print("\nLoop completed.")

sys.exit()
