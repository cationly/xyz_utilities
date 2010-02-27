#!/usr/bin/env python

####################################################
# Nicolas Poilvert, July 2009                      #
# A little program that reads a file that contains #
# atomic positions in xyz format and then asks the #
# user how to duplicate those atomic positions     #
# The format of the xyz file is :                  #
# <number of atoms> on 1st line                    #
# <some comments> on the 2nd line                  #
# <atomic symbol> x y z for all the other lines    #
####################################################

import os
import sys
import optparse
from os import path

def main():
  # parsing command line arguments
  parser = optparse.OptionParser()
  parser.add_option('-f', '--filename',
                    dest    = 'xyz_file',
                    default = 'file.xyz',
                    type    = 'str',
                    help    = 'name of the xyz file')
  options, remainder = parser.parse_args()
  # if the program is called without options it prints the help menu
  if len(sys.argv[1:])==0:
    parser.print_help()
    sys.exit(0)
  # now  that  we have  the command line arguments
  # we can call the duplicate() function to create
  # the needed supercell
  duplicate(options.xyz_file)

  return

def duplicate(input):
  """
  Takes an input file, reads  the atomic symbols
  and coordinates and duplicate according to the
  user's wish.
  """
  # checking that the input file exists
  if not path.exists(input):
    print '                                '
    print ' The input file "%s"  is either ' %(input,)
    print ' not existing or not present in '
    print ' the current directory.         '
    print '                                '
    sys.exit(0)
  # now reading in the input and creating the output
  data  = open(input,'r')
  lines = data.readlines()
  first_line  = lines[0]
  second_line = lines[1]
  lines.pop(0)
  lines.pop(0)
  out   = open(input+'_duplicated','w')
  cell_atoms = []
  for line in lines:
    try:
      line_strings = line.split()
      symbol       = line_strings[0]
      x            = float(line_strings[1])
      y            = float(line_strings[2])
      z            = float(line_strings[3])
      cell_atoms.append([symbol,x,y,z])
    except:
      print '                                 '
      print ' There must be some format error '
      print ' in  the input file. The program '
      print ' expects something like :        '
      print '                                 '
      print ' C 0.253 2.345 9.456             '
      print ' F 23.45 3.467 0.564             '
      print ' etc ...                         '
      print '                                 '
      sys.exit(0)
  data.close()
  # building the supercell structure
  print ''
  dim = int( raw_input(" 1D, 2D or 3D duplicate ? ") )
  print ''
  directions = [] # list of direction(s) in which to duplicate the cell
  lengths    = [] # list of periodicity length(s)
  copies     = [] # list of the number of duplicated cell(s)
  # Case of one-dimensional duplicates
  if dim==1:
    first_dir  = str( raw_input(  " direction in which to duplicate ? (x,y or z) : ") )
    first_len  = float( raw_input(" periodicity length in '%s' ? (in Ang)         : " %(first_dir,)) )
    first_copy = int( raw_input(  " number of duplicate in '%s' ?                 : " %(first_dir,)) )
    print ''
    directions.append(first_dir)
    lengths.append(first_len)
    copies.append(first_copy)
  # Case of two-dimensional duplicates
  elif dim==2:
    first_dir  = str( raw_input(  " first  direction in which to duplicate ? (x,y or z) : ") )
    first_len  = float( raw_input(" periodicity length in '%s' ? (in Ang)                : " %(first_dir,)) )
    first_copy = int( raw_input(  " number of duplicate in '%s' ?                        : " %(first_dir,)) )
    second_dir = str( raw_input(  " second direction in which to duplicate ? (x,y or z) : ") )
    second_len = float( raw_input(" periodicity length in '%s' ? (in Ang)                : " %(second_dir,)) )
    second_copy= int( raw_input(  " number of duplicate in '%s' ?                        : " %(second_dir,)) )
    print ''
    directions.append(first_dir)
    lengths.append(first_len)
    copies.append(first_copy)
    directions.append(second_dir)
    lengths.append(second_len)
    copies.append(second_copy)
  # Case of three-dimensional duplicates
  elif dim==3:
    first_dir  = str( raw_input(  " first  direction in which to duplicate ? (x,y or z) : ") )
    first_len  = float( raw_input(" periodicity length in '%s' ? (in Ang)                : " %(first_dir,)) )
    first_copy = int( raw_input(  " number of duplicate in '%s' ?                        : " %(first_dir,)) )
    second_dir = str( raw_input(  " second direction in which to duplicate ? (x,y or z) : ") )
    second_len = float( raw_input(" periodicity length in '%s' ? (in Ang)                : " %(second_dir,)) )
    second_copy= int( raw_input(  " number of duplicate in '%s' ?                        : " %(second_dir,)) )
    third_dir  = str( raw_input(  " third  direction in which to duplicate ? (x,y or z) : ") )
    third_len  = float( raw_input(" periodicity length in '%s' ? (in Ang)                : " %(third_dir,)) )
    third_copy = int( raw_input(  " number of duplicate in '%s' ?                        : " %(third_dir,)) )
    print ''
    directions.append(first_dir)
    lengths.append(first_len)
    copies.append(first_copy)
    directions.append(second_dir)
    lengths.append(second_len)
    copies.append(second_copy)
    directions.append(third_dir)
    lengths.append(third_len)
    copies.append(third_copy)
  # beyond three-dimensional duplicates the program doesn't know what to do
  else:
    print '                                       '
    print ' Wrong duplication dimensionality "%s" ' %(dim,)
    print ' must be either 1, 2 or 3              '
    print '                                       '
    sys.exit(0)
  # some checks to see if the program understands the informations given by the user
  for direction in directions:
    if direction not in ['x','y','z']:
      print '                               '
      print ' direction "%s" not recognized ' %(direction,)
      print '                               '
      sys.exit(0)
  # determining the total number of atoms
  if dim==1:
    total_number_of_atoms = copies[0]*len(cell_atoms)
    out.write('%6i \n' %(total_number_of_atoms,))
    out.write(' # 1D system duplicated %4i times in the %s direction \n'
                                                     %(copies[0],directions[0]))
  elif dim==2:
    total_number_of_atoms = copies[0]*copies[1]*len(cell_atoms)
    out.write('%6i \n' %(total_number_of_atoms,))
    out.write(' # 2D system duplicated %4i times in the %s direction and %4i times in the %s direction \n' 
                                                     %(copies[0],directions[0],
                                                       copies[1],directions[1]))
  else:
    total_number_of_atoms = copies[0]*copies[1]*copies[2]*len(cell_atoms)
    out.write('%6i \n' %(total_number_of_atoms,))
    out.write(' # 3D system duplicated %4i times in the %s direction, %4i times in the %s direction and %4i times in the %s direction \n'
                                                     %(copies[0],directions[0],
                                                       copies[1],directions[1],
                                                       copies[2],directions[2]))
  # Actually building the structure :
  #
  # Case of one-dimensional duplicates
  if dim==1:
    if directions[0]=='x':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+i*lengths[0],atom[2],atom[3]))
    elif directions[0]=='y':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1],atom[2]+i*lengths[0],atom[3]))
    elif directions[0]=='z':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1],atom[2],atom[3]+i*lengths[0]))
  # Case of two-dimensional duplicates
  elif dim==2:
    if directions[0]=='x' and directions[1]=='y':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+i*lengths[0],atom[2]+j*lengths[1],atom[3]))
    elif directions[0]=='y' and directions[1]=='x':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+j*lengths[1],atom[2]+i*lengths[0],atom[3]))
    elif directions[0]=='x' and directions[1]=='z':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+i*lengths[0],atom[2],atom[3]+j*lengths[1]))
    elif directions[0]=='z' and directions[1]=='x':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+j*lengths[1],atom[2],atom[3]+i*lengths[0]))
    elif directions[0]=='y' and directions[1]=='z':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1],atom[2]+i*lengths[0],atom[3]+j*lengths[1]))
    elif directions[0]=='z' and directions[1]=='y':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1],atom[2]+j*lengths[1],atom[3]+i*lengths[0]))
  # Case of three-dimensional duplicates
  elif dim==3:
    if directions[0]=='x' and directions[1]=='y' and directions[2]=='z':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+i*lengths[0],atom[2]+j*lengths[1],atom[3]+k*lengths[2]))
    elif directions[0]=='x' and directions[1]=='z' and directions[2]=='y':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+i*lengths[0],atom[2]+k*lengths[2],atom[3]+j*lengths[1]))
    elif directions[0]=='y' and directions[1]=='x' and directions[2]=='z':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+j*lengths[1],atom[2]+i*lengths[0],atom[3]+k*lengths[2]))
    elif directions[0]=='y' and directions[1]=='z' and directions[2]=='x':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+k*lengths[2],atom[2]+i*lengths[0],atom[3]+j*lengths[1]))
    elif directions[0]=='z' and directions[1]=='x' and directions[2]=='y':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+j*lengths[1],atom[2]+k*lengths[2],atom[3]+i*lengths[0]))
    elif directions[0]=='z' and directions[1]=='y' and directions[2]=='x':
      for atom in cell_atoms:
        for i in xrange(0,copies[0]):
          for j in xrange(0,copies[1]):
            for k in xrange(0,copies[2]):
              out.write('%s  %10.6f %10.6f %10.6f \n' %(atom[0],atom[1]+k*lengths[2],atom[2]+j*lengths[1],atom[3]+i*lengths[0]))
  # closing the output file
  out.close()

  return

if __name__ == '__main__':
	main()

