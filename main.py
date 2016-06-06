import sys
import os
from os.path import isfile
from src.tool import check_int
from src.method_one import algo

"""
    Entry point.
"""

# args = sys.stdin.readline().split(" ")
args = "../data/test.dyn 0 9999999999".split(" ")

if len(args) <= 2:
    print "Usage:  filename  vertex_id (>0)  time (>0)"
    sys.exit(-1)

if (not isfile(args[0])) or (not os.access(args[0], os.R_OK)):
    print "File '" + args[0] + "' doesn't exist or locked."
    sys.exit(-1)

if (not check_int(args[1])) or (not check_int(args[2].strip())):
    print "Positive int are expected for vertex_id and time."
    sys.exit(-1)

filename = args[0]
vertex_id = int(args[1])
time = int(args[2].strip())

# test(filename) #, vertex_id, time)
# test_time(filename, 98277034)
print "(nb_in, nb_out)[" + str(vertex_id) + "][" + str(time) + "] = " + str(algo(filename, vertex_id, time))
