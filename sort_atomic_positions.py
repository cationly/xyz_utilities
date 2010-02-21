#!/usr/bin/env python

###################################################
# Nicolas Poilvert, October 2009                  #
# This little program takes an xyz formatted file #
# and sorts the atomic positions in a given direc #
# tion 'x', 'y' or 'z'.                           #
# The format of the xyz file is :                 #
# <number of atoms> on 1st line                   #
# <some comments> on the 2nd line                 #
# <atomic symbol> x y z for all the other lines   #
###################################################

import os
import sys
import numpy
import optparse

def main():
  # parsing the command-line arguments
  parser = optparse.OptionParser()
  parser.add_option('-f', '--filename',
                    dest    = 'xyz_file',
                    default = 'file.xyz',
                    type    = 'str',
                    help    = 'name of the xyz file')
  parser.add_option('-d', '--direction',
                    dest    = 'sorting_direction',
                    default = 'z',
                    type    = 'str',
                    help    = 'direction for sorting : x, y or z')
  options, remainder = parser.parse_args()
  # if the program is called without options it prints the help menu
  if len(sys.argv[1:])==0:
    parser.print_help()
    sys.exit(0)
  # checking if the file exists and is actually a file
  if not os.path.isfile(options.xyz_file):
    print "                                      "
    print " The object '%s' is either not a file " %(options.xyz_file,)
    print " or does not exist.                   "
    print "                                      "
    sys.exit(0)
  # checking if the sorting direction is understandable
  if options.sorting_direction not in ['x','y','z']:
    print "                                       "
    print " The sorting direction  '%s' could not " %(options.sorting_direction,)
    print " be understood. Please use 'x', 'y' or "
    print " 'z'.                                  "
    print "                                       "
    sys.exit(0)
  # reading in the file
  datafile = open(options.xyz_file,'r')
  lines = datafile.readlines()
  atoms = []
  for i in xrange(2,len(lines)):
    symbol = lines[i].split()[0]
    x      = float(lines[i].split()[1])
    y      = float(lines[i].split()[2])
    z      = float(lines[i].split()[3])
    atoms.append([symbol,x,y,z])
  datafile.close()
  # now computing the array of sorted indexes
  dummy_array = []
  if options.sorting_direction=='x':
    sort_dir = 1
  elif options.sorting_direction=='y':
    sort_dir = 2
  else:
    sort_dir = 3
  for i in xrange(len(atoms)):
    dummy_array.append(atoms[i][sort_dir])
  dummy_array    = numpy.array(dummy_array)
  sorted_indexes = numpy.argsort(dummy_array)
  # using the sorted indexes for creating the file or sorted positions
  outfile = open(options.xyz_file+'_sorted','w')
  outfile.write(lines[0])
  outfile.write(lines[1])
  for index in sorted_indexes:
    outfile.write('%s  %10.6f  %10.6f  %10.6f \n' %(atoms[index][0],
                                                    atoms[index][1],
                                                    atoms[index][2],
                                                    atoms[index][3]))
  outfile.close()

  return

if __name__=='__main__':
  main()

