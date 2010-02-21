#!/usr/bin/env python

###################################################
# Nicolas Poilvert, October 2009                  #
# This little program takes an xyz formatted file #
# and  rotates  the  atomic positions in  a given #
# direction (x,y,z) given by the user along  with #
# with a point belonging to the axis of rotation. #
# The format of the xyz file is :                 #
# <number of atoms> on 1st line                   #
# <some comments> on the 2nd line                 #
# <atomic symbol> x y z for all the other lines   #
###################################################

import os
import sys
import numpy
from numpy.linalg import norm as norm
from numpy import dot as dot
from numpy import cross as cross
from math import cos as cos
from math import sin as sin
import optparse

def main():
  # parsing the command-line arguments
  parser = optparse.OptionParser()
  parser.add_option('-f', '--filename',
                    dest    = 'xyz_file',
                    default = 'file.xyz',
                    type    = 'str',
                    help    = 'name of the xyz file')
  parser.add_option('--nx',
                    dest    = 'nx',
                    default = 0.0,
                    type    = 'float',
                    help    = 'x coordinate of a vector in the direction of the rotation axis')
  parser.add_option('--ny', 
                    dest    = 'ny',
                    default = 0.0,
                    type    = 'float',
                    help    = 'y coordinate of a vector in the direction of the rotation axis')
  parser.add_option('--nz', 
                    dest    = 'nz',
                    default = 1.0,
                    type    = 'float',
                    help    = 'z coordinate of a vector in the direction of the rotation axis')
  parser.add_option('-a', '--angle',
                    dest    = 'theta',
                    default = 0.0,
                    type    = 'float',
                    help    = 'angle of rotation')
  parser.add_option('-x', 
                    dest    = 'x',
                    default = 0.0,
                    type    = 'float',
                    help    = 'x coordinate of a point on the rotation axis')
  parser.add_option('-y',
                    dest    = 'y',
                    default = 0.0,
                    type    = 'float',
                    help    = 'y coordinate of a point on the rotation axis')
  parser.add_option('-z',
                    dest    = 'z',
                    default = 0.0,
                    type    = 'float',
                    help    = 'z coordinate of a point on the rotation axis')
  options, remainder = parser.parse_args()
  # if the program is called without options it prints the help menu
  if len(sys.argv[1:])==0:
    parser.print_help()
    sys.exit(0)
  # normalizing the vector on the axis of rotation
  n    = numpy.zeros(3,dtype='float')
  n[0] = options.nx
  n[1] = options.ny
  n[2] = options.nz
  n    = n * (1.0 / norm(n))
  # opening the position file
  if not os.path.isfile(options.xyz_file):
    print "                                                     "
    print " '%s' is either not in the current working directory " %(options.xyz_file,)
    print " or does not exist.                                  "
    print "                                                     "
    sys.exit(0)
  datafile = open(options.xyz_file,'r')
  lines = datafile.readlines()
  datafile.close()
  # creating the output file
  outfile = open(options.xyz_file+'_rotated','w')
  outfile.write(lines[0])
  outfile.write(lines[1])
  # computing the offset to be added
  offset = numpy.array([options.x,options.y,options.z])
  for i in xrange(2,len(lines)):
    # extracting the datas from the line
    symbol = lines[i].split()[0]
    x      = float(lines[i].split()[1])
    y      = float(lines[i].split()[2])
    z      = float(lines[i].split()[3])
    # computing the relative vector v_rel
    v_rel = numpy.array([x,y,z]) - offset
    # here's the rotated vector
    v_rot = dot(v_rel,n)*n + cos(options.theta)*(v_rel - dot(v_rel,n)*n) - sin(options.theta)*cross(v_rel,n)
    # adding back the offset vector
    v_rot = v_rot + offset
    # printing to the output file
    outfile.write('%s  %10.6f  %10.6f  %10.6f \n' %(symbol,v_rot[0],v_rot[1],v_rot[2]))
  outfile.close()
  return

if __name__=='__main__':
  main()

