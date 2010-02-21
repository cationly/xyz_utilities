#!/usr/bin/env python

###################################################
# Nicolas Poilvert, October 2009                  #
# This little program takes an xyz formatted file #
# and translates the atomic positions in  a given #
# direction (x,y,z) given by the user             #
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
  parser.add_option('-x', '--translation_in_x',
                    dest    = 'tran_x',
                    default = 0.0,
                    type    = 'float',
                    help    = 'translation in x direction')
  parser.add_option('-y', '--translation_in_y',
                    dest    = 'tran_y',
                    default = 0.0,
                    type    = 'float',
                    help    = 'translation in y direction')
  parser.add_option('-z', '--translation_in_z',
                    dest    = 'tran_z',
                    default = 0.0,
                    type    = 'float',
                    help    = 'translation in z direction')
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
  # checking if the translation vectors can be converted to floats
  try:
    tran_x = float(options.tran_x)
    tran_y = float(options.tran_y)
    tran_z = float(options.tran_z)
  except:
    print "                                                    "
    print " One of the translation could not be converted to a "
    print " floating point number.                             "
    print "                                                    "
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
  # now creating the output file with the properly
  # translated atomic positions
  outfile = open(options.xyz_file+'_translated','w')
  outfile.write(lines[0])
  outfile.write(lines[1])
  for atom in atoms:
    outfile.write('%s  %10.6f  %10.6f  %10.6f \n' %(atom[0],
                                                    atom[1]+tran_x,
                                                    atom[2]+tran_y,
                                                    atom[3]+tran_z))
  outfile.close()

  return

if __name__=='__main__':
  main()

