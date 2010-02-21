Introduction :
==============

This directory contains a set of utility Python programs for easy manipulation
of "xyz" formatted files.

The XYZ format :
================

It is used in Quantum Chemistry to represent the structure of molecules in 3D.
For more details, see : http://en.wikipedia.org/wiki/XYZ_file_format

details of the format :
|-------------------------------------------------------------|
|<number of atoms> (N for example)                            | <- line 1
|Any comment you want                                         | <- line 2
|atom_symbol_1  x_coordinate_1  y_coordinate_1  z_coordinate_1| <- line 3 and
|atom_symbol_2  x_coordinate_2  y_coordinate_2  z_coordinate_2|    beyond
|...                                                          |
|atom_symbol_N  x_coordinate_N  y_coordinate_N  z_coordinate_N|
|-------------------------------------------------------------|

The atomic coordinates are generally given in Angstroms.

Content of the directory :
==========================

- rotate_atomic_positions.py
- translate_atomic_positions.py
- sort_atomic_positions.py

The names of the programs are pretty self-explanatory. Each program reads an xy
z  formatted file, and then manipulates the atomic coordinates according to the
type of operation selected (translation, rotation, sorting). When all the coord
inates have been updated, an output file is created with the first 2 lines mat-
ching perfectly the ones in the original file, and the subsequent lines contai-
ning the updated coordinates.

The ouput file names are respectively :
- <seedname>_sorted     for "sort_atomic_positions.py"
- <seedname>_translated for "translate_atomic_positions.py"
- <seedname>_rotated    for "rotate_atomic_positions.py"
where seedname is the original name of the file the program is reading.

All the programs use a set of command line options. For details just type :
|$my_prompt> python <name_of_the_program.py> [ENTER]
This will print the "help" menu of the program.

