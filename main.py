import sys
import os
from os.path import isfile, realpath
from src.tool import check_int
from src.method_one import algo

"""
    Entry point.
"""

args = sys.stdin.readline().split(" ")


if len(args) <= 2:
    print "Usage:  filename  vertex_id (>0)  time (>0)"
    sys.exit(-1)

if (not isfile(args[0])) or (not os.access(args[0], os.R_OK)):
    print "File '" + args[0] + "' doesn't exist or locked."
    sys.exit(-1)

if (not check_int(args[1])) or (not check_int(args[2])):
    print "Positive int are expected for vertex_id and time."
    sys.exit(-1)

filename  = args[0]
vertex_id = args[1]
time      = args[2]

algo(filename, vertex_id, time)

